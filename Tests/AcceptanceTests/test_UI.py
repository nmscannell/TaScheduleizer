from django.test import TestCase
from UserInterface import UI
from Main.models import Account

class TestUI(TestCase):

    def setUp(self):
        self.UI = UI()

        Account.objects.create(userName="janewayk123", firstName="Kathryn", lastName="Janeway", password="123456",
                               email="janewayk@uwm.edu", title=2,
                               address="14 Voyager Drive", city="Delta", state="Quadrant", zipCode="00000",
                               officeNumber="456", officePhone="555-555-5555", officeDays="TR",
                               officeHoursStart="1300", officeHoursEnd="1400", currentUser=False)

    def test_command(self):
        self.fail()

    def test_login_success(self):
        self.assertEqual(self.UI.command("login janewayk123 123456"), "Logged in as janewayk123")

    def test_command_login_success_whitespace(self):
        self.assertEqual(self.UI.command("  login     janewayk123   123456     "), "Logged in as janewayk123")

    def test_command_login_incorrect_password(self):
        self.assertEqual(self.UI.command("login janewayk123 aaaaaaa"), "Incorrect password")

    def test_command_login_account_does_not_exist(self):
        self.assertEqual(self.UI.command("login neelix45 123456"), "Account Not Found")

    def test_command_login_missing_args(self):
        self.assertEqual(self.UI.command("login janewayk123"), "login requires 2 arguments")
