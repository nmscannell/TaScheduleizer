from django.test import TestCase
from django.test import Client
from Main.models import Account, Course, Section


class Test_web(TestCase):

    def setUp(self):

        self.c = Client()

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

        # Set up for Course testing
        Course.objects.create(name="DataStructures", number=351, onCampus=True, classDays="TR",
                              classHoursStart=1200, classHoursEnd=1300)

        Course.objects.create(name="ComputerArchitecture", number=458, onCampus=True, classDays="MW",
                              classHoursStart=1230, classHoursEnd=1345)

        Section.objects.create(course=Course.objects.get(number="351"), sectionNumber=804)

        Section.objects.create(course=Course.objects.get(number="458"), sectionNumber=804)



    """
    login
    """
    def test_login_success(self):
        response = self.c.post('/login/', {'username': 'jack23', 'password': '!@iamjack'})
        self.assertEqual(response.context['message'],
                         "")

    def test_login_wrong_password(self):
        response = self.c.post('/login/', {'username': 'jack23', 'password': '********'})
        self.assertEqual(response.context['message'],
                         "Incorrect password")

    def test_login_username_not_existed(self):
        response = self.c.post('/login/', {'username': 'ariana02', 'password': '0192pg'})
        self.assertEqual(response.context['message'],
                         "Account Not Found")


    """
    createAccount 
    """

    def test_createAccount_success(self):
        response = self.c.post('/createaccount/', {'firstname': 'Miles', 'lastname': 'OBrien',
                                                   'username': 'obrien31', 'title': 'TA',
                                                   'email': 'obrien31@uwm.edu'})
        self.assertEqual(response.context['message'],
                         "Account successfully created.  Temporary password is: obrien31456")

    def test_createAccount_alreadyexists(self):
        response = self.c.post('/createaccount/', {'firstname': 'Jean Luc', 'lastname': 'Picard',
                                                   'username': 'picard304', 'title': 'TA',
                                                   'email': 'picardj@uwm.edu'})
        self.assertEqual(response.context['message'], "Account already exists")

    def test_createAccount_invalid_email(self):
        response = self.c.post('/createaccount/', {'firstname': 'Harry', 'lastname': 'Kim',
                                                   'username': 'kim4', 'title': 'Instructor',
                                                   'email': 'kim4@starfleet.com'})
        self.assertEqual(response.context['message'], "The email address you have entered in not valid.  "
                                    "Please make sure you are using a uwm email address in the correct format.")

    def test_createAccount_invalid_title(self):
        response = self.c.post('/createaccount/', {'firstname': 'Harry', 'lastname': 'Kim',
                                                   'username': 'kim4', 'title': 'Engineer',
                                                   'email': 'kim4@uwm.edu'})
        self.assertEqual(response.context['message'], "Invalid title, account not created")


    """
    createCourse
    """

    def test_createCourse_success(self):
        response = self.c.post('/createcourse/', {'name': 'ComputerNetwork', 'number': 520,
                                                  'onCampus': True, 'classDays': 'TR',
                                                  'classHoursStart': 1400, 'classHoursEnd': '1600'})
        self.assertEqual(response.context['message'],
                         "Course successfully created")

    def test_createCourse_invalidNumber(self):
        response = self.c.post('/createcourse/', {'name': 'ComputerNetwork', 'number': 1024,
                                                  'onCampus': True, 'classDays': 'TR',
                                                  'classHoursStart': 1400, 'classHoursEnd': '1600'})
        self.assertEqual(response.context['message'],
                         "Course number must be numeric and three digits long")

    def test_createCourse_course_exists(self):
        response = self.c.post('/createcourse/', {'name': 'ComputerSecurity', 'number': 469,
                                                  'onCampus': True, 'classDays': 'MW',
                                                  'classHoursStart': 1200, 'classHoursEnd': '1400'})
        self.assertEqual(response.context['message'],
                         "Course already exists")

    def test_createCourse_invalid_days(self):

        response = self.c.post('/createcourse/', {'name': 'ComputerSecurity', 'number': 469,
                                                  'onCampus': True, 'classDays': 'S',
                                                  'classHoursStart': 1200, 'classHoursEnd': '1400'})
        self.assertEqual(response.context['message'],
                         "Invalid days of the week, please enter days in the format: MWTRF or NN for online")

    def test_createCourse_invalid_times(self):
        response = self.c.post('/createcourse/', {'name': 'Server Side Web Programming', 'number': 452,
                                                  'onCampus': True, 'classDays': 'TR',
                                                  'classHoursStart': '15:00', 'classHoursEnd': '17:00'})
        self.assertEqual(response.context['message'],
                         "Invalid start or end time, please use a 4 digit military time representation")

    def test_createCourse_invalid_locations(self):
        response = self.c.post('/createcourse/', {'name': 'Server Side Web Programming', 'number': 452,
                                                  'onCampus': 'hybrid', 'classDays': 'TR',
                                                  'classHoursStart': '1500', 'classHoursEnd': '1700'})
        self.assertEqual(response.context['message'],
                         "Location is invalid, please enter campus or online")

    """
    deleteAccount
    
    """

    def test_deleteAccount_success(self):
        response = self.c.post('/deleteaccount/', {'username': 'kim4'})
        self.assertEqual(response.context['message'],
                         "Account successfully deleted")

    def test_createAccount_doesnotexists(self):
        response = self.c.post('/deleteaccount/', {'username': 'henry42'})
        self.assertEqual(response.context['message'], "Account does not exist")
