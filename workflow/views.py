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
