from django.core.exceptions import PermissionDenied
from django.forms.models import modelform_factory, inlineformset_factory
from django.views import generic
from django.shortcuts import render, redirect
from viewflow.flow import flow_start_view
from viewflow.flow.views import FlowViewMixin, get_next_task_url

from rest_framework import permissions, viewsets
from rest_framework import status
from rest_framework.response import Response

from .models import Project, Order, OrderVM
from .serializers import ProjectSerializer, OrderSerializer, OrderVMSerializer
from .permissions import IsOwnerOfProject, IsSuperPowerfulUser, IsOwnerOfOrder


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.order_by('name')
    serializer_class = ProjectSerializer

    def get_permissions(self):
        # The idea here is that projects are private to owners, yet they
        # cannot delete their own project; super powerful users rule the
        # universe.
        perms = [IsSuperPowerfulUser()]
        if self.request.method != 'DELETE':
            perms += [permissions.IsAuthenticated(), IsOwnerOfProject()]
        return tuple(perms)

    def perform_create(self, serializer):
        # TODO we should have needed to specify name here.
        serializer.save(owner=self.request.user)
        return super(ProjectViewSet, self).perform_create(serializer)

    def list(self, request, *args, **kargs):
        queryset = self.queryset.filter(owner=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kargs):
        return Response(status=status.HTTP_204_NO_CONTENT)


class OwnerProjectsViewSet(viewsets.ViewSet):
    queryset = Project.objects.select_related('owner').all()
    serializer_class = ProjectSerializer

    def list(self, request, owner=None):
        queryset = self.queryset.filter(owner__username=owner)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.order_by('id')
    serializer_class = OrderSerializer

    def get_permissions(self):
        return (permissions.IsAuthenticated(), IsOwnerOfOrder(),)

    def list(self, request, *args, **kargs):
        queryset = self.queryset.filter(project__owner=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


@flow_start_view
def start_view(request):
    form_class = modelform_factory(Project, fields=[
        'name',
    ])

    formset_class = inlineformset_factory(Project, OrderVM, fields=[
        'name', 'sockets', 'cpu_per_sockets', 'memory_GB', 'disks', 'nics'
    ])

    if not request.activation.has_perm(request.user):
        raise PermissionDenied

    request.activation.prepare(request.POST or None, user=request.user)

    form = form_class(request.POST or None)
    formset = formset_class(request.POST or None)

    is_valid = all([form.is_valid(), formset.is_valid()])
    if is_valid:
        project = form.save()
        request.process.project = project
        order = Order(prject=project)
        request.process.order = order
        for item in formset.save(commit=False):
            item.project = project
            item.order = order
            item.save()
            request.activation.done()
            return redirect(get_next_task_url(request, request.process))
    return render(request, 'viewflow/complete_project_start.html', {
        'activation': request.activation,
        'form': form,
        'formset': formset,
    })


class OrderCompleteProjectView(FlowViewMixin, generic.UpdateView):
    def get_object(self):
        return self.activation.process.order

