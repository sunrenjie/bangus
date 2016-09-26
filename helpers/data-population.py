from authentication.serializers import AccountSerializer
from authentication.models import Account

Account.objects.create_superuser(username='admin', email='admin@g.cn', password='admin')
account = Account.objects.latest('created_at')
serialized_account = AccountSerializer(account)
print(serialized_account.data)
