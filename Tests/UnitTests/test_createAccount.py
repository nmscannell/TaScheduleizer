from django.test import TestCase
from Main.models import Account
import Commands
from django.test import Client


class TestCreateAccount(TestCase):

    def setUp(self):

        self.c = Client()
        # Set up for createAccount Testing
        Account.objects.create(userName="janewayk123", firstName="Kathryn", lastName="Janeway", password="123456",
                               email="janewayk@uwm.com", title=2,
                               address="14 Voyager Drive", city="Delta", state="Quadrant", zipCode="00000",
                               officeNumber="456", officePhone="555-555-5555", officeDays="TR",
                               officeHoursStart="1300", officeHoursEnd="1400", currentUser=False)

        Account.objects.create(userName="picard304", firstName="Jean Luc", lastName="Picard", password="90456",
                               email="picardj@uwm.com", title=1, address="87 Enterprise Avenue",
                               city="Alpha", state="Quadrant", zipCode="11111", officeNumber="54",
                               officePhone="777-777-7777", officeDays="W", officeHoursStart="0900",
                               officeHoursEnd="1000", currentUser=False)

        Account.objects.create(userName="kirkj22", firstName="James", lastName="Kirk", password="678543",
                               email="kirkj22@uwm.com", title=4, address="789 Enterprise Avenue",
                               city="Alpha", state="Quadrant", zipCode="89765", officeNumber="987",
                               officePhone="897-654-398", officeDays="MW", officeHoursStart="1500",
                               officeHoursEnd="1600", currentUser=False)



    def test_account_successfully_created(self):
        self.assertEqual(Commands.createAccount("Data", "Noonien Soong", "data33", "instructor", "data33@uwm.edu"),
                        "Account successfully created.  Temporary password is: data33456")
        self.assertEqual(Commands.createAccount("S'chn T'gai", "Spock", "spock29", "instructor", "spock29@uwm.edu"),
                        "Account successfully created.  Temporary password is: spock29456")
        self.assertEqual(Commands.createAccount("Trip", "Tucker", "tuckert90", "TA", "tuckert90@uwm.edu"),
                        "Account successfully created.  Temporary password is: tuckert90456")

        A = Account.objects.get(userName="data33")
        self.assertEqual(A.firstName, "Data")
        self.assertEqual(A.lastName, "Noonien Soong")
        self.assertEqual(A.userName, "data33")
        self.assertEqual(A.email, "data33@uwm.edu")
        self.assertEqual(A.title, 2)

        B = Account.objects.get(userName="spock29")
        self.assertEqual(B.firstName, "S'chn T'gai")
        self.assertEqual(B.lastName, "Spock")
        self.assertEqual(B.userName, "spock29")
        self.assertEqual(B.email, "spock29@uwm.edu")
        self.assertEqual(B.title, 2)

        C = Account.objects.get(userName="tuckert90")
        self.assertEqual(C.firstName, "Trip")
        self.assertEqual(C.lastName, "Tucker")
        self.assertEqual(C.userName, "tuckert90")
        self.assertEqual(C.email, "tuckert90@uwm.edu")
        self.assertEqual(C.title, 1)

    def test_success_post(self):
        response = self.c.post('/createaccount/', {'firstname': 'Wesley', 'lastname': 'Crusher',
                                                   'username': 'crusher31', 'title': 'TA',
                                                   'email': 'crusher31@uwm.edu'})
        self.assertEqual(response.context['message'],
                         "Account successfully created.  Temporary password is: crusher31456")
        A = Account.objects.get(userName="crusher31")
        self.assertEqual(A.firstName, "Wesley")
        self.assertEqual(A.lastName, "Crusher")
        self.assertEqual(A.email, "crusher31@uwm.edu")
        self.assertEqual(A.title, 1)


    def test_account_already_exist(self):
        self.assertEqual(Commands.createAccount("Jean Luc", "Picard", "picard304", "TA", "picardj@uwm.edu"),
                         "Account already exists")
        self.assertEqual(Commands.createAccount( "Kathryn", "Janeway", "janewayk123", "instructor", "janewayk@uwm.edu"),
                         "Account already exists")

    def test_account_already_exists_post(self):
        response = self.c.post('/createaccount/', {'firstname': 'Kathryn', 'lastname': 'Janeway',
                                                   'username': 'janewayk123', 'title': 'Instructor',
                                                   'email':'janewayk123@uwm.edu'})
        self.assertEqual(response.context['message'], "Account already exists")

    def test_invalid_email(self):
        self.assertEqual(Commands.createAccount("Wesley", "Crusher", "crusherw31", "TA", "crusher@hotmail.com"),
                         "The email address you have entered in not valid.  Please make sure you are using a uwm "
                         "email address in the correct format.")
        self.assertEqual(Commands.createAccount( "Wesley", "Crusher", "crusher31", "TA", "crusher"),
                         "The email address you have entered in not valid.  Please make sure you are using a uwm "
                         "email address in the correct format.")

    def test_invalid_email_post(self):
        response = self.c.post('/createaccount/', {'firstname': 'Beverly', 'lastname': 'Crusher',
                                        'username': 'bcrusher', 'title': 'Instructor',
                                        'email': 'bcrusher@starfleet.edu'})
        self.assertEqual(response.context['message'], "The email address you have entered in not valid.  "
                                            "Please make sure you are using a uwm email address in the correct format.")

    def test_invalid_title(self):
        self.assertEqual(Commands.createAccount("Wesley", "Crusher", "crusher31", "student", "crusher31@uwm.edu"),
                         "Invalid title, account not created")

    def test_invalid_title_post(self):
        response = self.c.post('/createaccount/', {'firstname': 'Beverly', 'lastname': 'Crusher',
                                                   'username': 'bcrusher', 'title': 'Doctor',
                                                   'email': 'bcrusher@uwm.edu'})
