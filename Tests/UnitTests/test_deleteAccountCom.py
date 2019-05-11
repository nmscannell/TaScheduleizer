from django.test import TestCase
from Commands import deleteAccountCom
from Main.models import Account


class TestDeleteAccountCom(TestCase):

    def setUp(self):
        Account.objects.create(userName="cwhitley")

    def test_deleteAccountCom_success(self):
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(deleteAccountCom("cwhitley"), "Account successfully deleted")
        self.assertEqual(Account.objects.count(), 0)

    def test_deleteAccountCom_notFound(self):
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(deleteAccountCom("jlongtree"), "Account does not exist")
        self.assertEqual(Account.objects.count(), 1)
