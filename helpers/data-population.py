from authentication.serializers import AccountSerializer
from authentication.models import Account
from workflow.models import Project, Order, OrderVM

admin = Account.objects.create_superuser(username='admin', email='admin@g.cn', password='admin')
user = Account.objects.create_user(username='user', email='user@g.cn', password='user')
p1 = Project(owner=user, name='user-project-1')
p1.save()
p2 = Project(owner=admin, name='admin-project-1')
p2.save()
order = Order(project=p1, is_active=True)
order.save()
order_vm = OrderVM(
    project=order.project, order=order,
    name='vm1', sockets=1, cpus_per_socket=2, memory_GB=4, nics='192.168.1.1;172.16.0.100')
order_vm.save()
account = Account.objects.latest('created_at')
serialized_account = AccountSerializer(account)
print(serialized_account.data)
