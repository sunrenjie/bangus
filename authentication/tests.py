from django.test import TestCase

from .models import Account
from .serializers import AccountSerializer


class AccountBehaviorTests(TestCase):

    def test_has_default_role_of_user(self):
        account = Account(username='admin', email='admin@g.cn', password='admin')
        serialized_account = AccountSerializer(account)
        self.assertEqual(serialized_account.data.get('role'), Account.ROLE_USER)
