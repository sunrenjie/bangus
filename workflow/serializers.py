from django.db import IntegrityError
from django.db.models import Q

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.serializers import AccountSerializer

from .models import Project, Order, OrderVM


class ProjectSerializer(serializers.ModelSerializer):
    owner = AccountSerializer(read_only=True, required=False)

    class Meta:
        model = Project
        fields = ('id', 'owner', 'name')
        # NOTICE if 'name' is added to read_only_fields, the name column of the POST data will not be available in
        # validated_data, and hence not available to serializer.save(). We shall at least have some unique fields
        # ('name' here) excluded from read_only_fields and force user to specify; otherwise we cannot tell whether
        # an object POST'ed by the user is an existing one (yes, the deep reason is that we are implementing a
        # tolerant version of create/POST).
        read_only_fields = ('id', 'owner')

    def get_validation_exclusions(self, *args, **kargs):
        exclusions = super(ProjectSerializer, self).get_validation_exclusions()
        return exclusions + ['owner']

    def create(self, validated_data):
        project, _ = Project.objects.get_or_create(**validated_data)
        return project


class OrderVMSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderVM
        fields = ('id', 'name', 'sockets', 'cpus_per_socket', 'memory_GB', 'nics')
        read_only_fields = ()

    def get_validation_exclusions(self, *args, **kargs):
        exclusions = super(OrderVMSerializer, self).get_validation_exclusions()
        return exclusions + []


class OrderSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    VMs = OrderVMSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ('id', 'project', 'is_active', 'created_at', 'updated_at', 'VMs')
        read_only_fields = ('created_at', 'updated_at')

    def get_validation_exclusions(self, *args, **kargs):
        exclusions = super(OrderSerializer, self).get_validation_exclusions()
        return exclusions + ['project', 'VMs']

    def create(self, validated_data):
        # The validators ensures existence of the data element for us, therefore calls to pop() needs no default values.
        VMs_data = validated_data.pop('VMs')
        project_data = validated_data.pop('project')
        is_active = validated_data.pop('is_active')
        owner = validated_data.pop('owner')
        # The project may or may not exist, create a one if necessary
        project, _ = Project.objects.get_or_create(owner=owner, **project_data)

        # TODO thread-safety
        vm_names = [d['name'] for d in VMs_data]
        vms = OrderVM.objects.filter(Q(project__exact=project) & Q(name__in=vm_names))
        if vms:
            raise ValidationError("VMs with the name(s) %s already exist in the project '%s'" %(
                ', '.join(["'%s'" % vm.name for vm in vms]), project.name))

        # There is really nothing unique about an order, just create().
        order = Order.objects.create(project=project, is_active=is_active, **validated_data)
        for d in VMs_data:
            OrderVM.objects.create(project=project, order=order, **d)
        return order

    def update(self, instance, validated_data):
        # The validators ensures existence of the data element for us, therefore calls to pop() needs no default values.
        project_data = validated_data.pop('project')
        is_active = validated_data.pop('is_active')
        owner = validated_data.pop('owner')
        VMs_data = validated_data.pop('VMs')

        try:
            project = Project.objects.get(owner=owner, **project_data)
            if project != instance.project:
                raise ValidationError('the project of the order cannot be mutated')
        except Project.DoesNotExist:
            raise ValidationError('the project of the order cannot be mutated (to an nonexisting one)')

        names = [d['name'] for d in VMs_data]
        all_vms = OrderVM.objects.filter(Q(project__exact=project) & Q(name__in=names))
        for d in VMs_data:
            name = d.pop('name')
            # shall contain at most one element, due to uniqueness of (project, name)
            vms = all_vms.filter(Q(name__exact=name))
            if not vms:
                OrderVM.objects.create(project=project, order=instance, name=name, **d)
            elif len(vms) == 1:
                vm = vms[0]
                if vm.order != instance:
                    raise ValidationError(
                        "the VM with name '%s' within project '%s' is already defined in another order '%s" % (
                            name, project.id, vm.order.id))
                else:
                    for attr, value in d.items():
                        setattr(vm, attr, value)
                    vm.save()
            else:
                raise

        instance.is_active = is_active
        instance.save()
        return instance
