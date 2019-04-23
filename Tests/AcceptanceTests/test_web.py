from django.test import TestCase
from django.test import Client
from Main.models import Account, Course, Section, AccountCourse, AccountSection


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
                               officeHoursEnd="1000", homePhone='123-456-7893', currentUser=False)

        Account.objects.create(userName="kirkj22", firstName="James", lastName="Kirk", password="678543",
                               email="kirkj22@uwm.com", title=4, address="789 Enterprise Avenue",
                               city="Alpha", state="Quadrant", zipCode="89765", officeNumber="987",
                               officePhone="897-654-398", officeDays="MW", officeHoursStart="1500",
                               officeHoursEnd="1600", currentUser=False)

        Account.objects.create(userName="jerry2", firstName="Jerry", lastName="Smith")
        # Set up for Course testing
        Course.objects.create(name="DataStructures", number=351, onCampus=True, classDays="TR",
                              classHoursStart=1200, classHoursEnd=1300)

        Course.objects.create(name="ComputerArchitecture", number=458, onCampus=True, classDays="MW",
                              classHoursStart=1230, classHoursEnd=1345)

        Section.objects.create(course=Course.objects.get(number="351"), number=804)

        Section.objects.create(course=Course.objects.get(number="458"), number=804)

        # Set up for section testing
        Course.objects.create(name="TemporalMechanics", number=784, onCampus=True, classDays="MW",
                              classHoursStart=1000, classHoursEnd=1100)

        Course.objects.create(name="WarpTheory", number=633, onCampus=True, classDays="TR", classHoursStart=1200,
                              classHoursEnd=1250)

        Course.objects.create(name="QuantumMechanics", number=709, onCampus=True, classDays="MWF",
                              classHoursStart=1030, classHoursEnd=1145)

        Course.objects.create(name="Linguistics", number=564, onCampus=False, classDays="TR",
                              classHoursStart=1800, classHoursEnd=1930)

        self.c1 = Course.objects.get(name="TemporalMechanics")
        self.c2 = Course.objects.get(name="WarpTheory")
        self.c3 = Course.objects.get(name="QuantumMechanics")

        Section.objects.create(course=self.c1, number=201, meetingDays="W", startTime=1000, endTime=1200)
        Section.objects.create(course=self.c1, number=202, meetingDays="F", startTime=1400, endTime=1700)
        Section.objects.create(course=self.c1, number=203, meetingDays="T", startTime=1000, endTime=1200)

        # set up for AssignAccountCourses testing
        self.cheng = Account.objects.create(userName="cheng41", title="2")
        self.taman = Account.objects.create(userName="taman", title="1")
        Account.objects.create(userName="bob15", title="2")
        Course.objects.create(number="535", name="Algorithms")
        Course.objects.create(number="537")
        discreteMath = Course.objects.create(number="317", name="DiscreteMath")
        self.course1 = Course.objects.get(number="535")
        self.course2 = Course.objects.get(number="317")
        AccountCourse.objects.create(Course=self.course1, Account=self.cheng)
        AccountCourse.objects.create(Account=self.taman, Course=discreteMath)

        # set up for assign TA to Section
        self.datastructures = Course.objects.get(name="DataStructures")
        self.tamanAccount = Account.objects.get(userName="taman")

    """
    login
    """

    def test_login_wrong_password(self):
        response = self.c.post('/login/', {'username': 'janewayk123', 'password': '********'})
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
    deleteAccount

    """

    def test_deleteAccount_success(self):
        response = self.c.post('/deleteaccount/', {'username': 'jerry2'})

        self.assertEqual(response.context['message'],
                         "Account successfully deleted")

    def test_deleteAccount_doesnotexists(self):
        response = self.c.post('/deleteaccount/', {'username':'henry42'})

        self.assertEqual(response.context['message'], "Account does not exist")

    """
    createCourse
    """

    def test_createCourse_success(self):
        response = self.c.post('/createcourse/', {'name': 'ComputerNetwork', 'number': 520,
                                                  'onCampus': 'campus', 'days': 'TR',
                                                  'start': 1400, 'end': 1600})
        self.assertEqual(response.context['message'],
                         "Course successfully created")

    def test_createCourse_invalidNumber(self):
        response = self.c.post('/createcourse/', {'name': 'ComputerNetwork', 'number': 1024,
                                                  'onCampus': 'campus', 'days': 'TR',
                                                  'start': 1400, 'end': 1600})
        self.assertEqual(response.context['message'],
                         "Course number must be numeric and three digits long")

    def test_createCourse_course_exists(self):
        response = self.c.post('/createcourse/', {'name': 'ComputerSecurity', 'number': 633,
                                                  'onCampus': 'campus', 'days': 'MW',
                                                  'start': 1200, 'end': 1400})
        self.assertEqual(response.context['message'],
                         "Course already exists")

    def test_createCourse_invalid_days(self):

        response = self.c.post('/createcourse/', {'name': 'ComputerSecurity', 'number': 469,
                                                  'onCampus': 'campus', 'days': 'S',
                                                  'start': 1200, 'end': 1400})
        self.assertEqual(response.context['message'],
                         "Invalid days of the week, please enter days in the format: MWTRF or NN for online")

    def test_createCourse_invalid_times(self):
        response = self.c.post('/createcourse/', {'name': 'Server Side Web Programming', 'number': 452,
                                                  'onCampus': 'campus', 'days': 'TR',
                                                  'start': '15:00', 'end': '17:00'})
        self.assertEqual(response.context['message'],
                         "Invalid start or end time, please use a 4 digit military time representation")

    def test_createCourse_invalid_locations(self):
        response = self.c.post('/createcourse/', {'name': 'Server Side Web Programming', 'number': 452,
                                                  'onCampus': 'hybrid', 'days': 'TR',
                                                  'start': 1500, 'end': 1700})
        self.assertEqual(response.context['message'],
                         "Location is invalid, please enter campus or online.")

    """
    createSection
    type is an integer field, 1 for lecture section, 0 for lab section. 
    """
    def test_createSection_success(self):
        response = self.c.post('/createssection/', {'courseNumber': 520, 'type': False, 'sectionNumber': 403,
                                                    'classDays': 'TR', 'classHoursStart': 1400,
                                                    'classHoursEnd': 1600})
        self.assertEqual(response.context['message'],
                         "Lab successfully created")

    def test_createSection_invalidNumber(self):
        response = self.c.post('/createsection/', {'courseNumber': 5923, 'type': False, 'sectionNumber': 403,
                                                    'classDays': 'TR', 'classHoursStart': 1400,
                                                    'classHoursEnd': 1600})
        self.assertEqual(response.context['message'],
                         "Course number must be numeric and three digits long")

    def test_createSection_course_not_exists(self):
        response = self.c.post('/createsection/', {'courseNumber': 536, 'type': False, 'sectionNumber': '803',
                                                    'classDays': 'MW', 'classHoursStart': 1600,
                                                    'classHoursEnd': 1800})
        self.assertEqual(response.context['message'],
                         "The Course you are trying to create a lab for does not exist")

    def test_createSection_not_onsite_class(self):

        response = self.c.post('/createsection/', {'courseNumber': '315', 'type': True,
                                                   'sectionNumber': '802', 'classDays': 'MW',
                                                  'classHoursStart': 1200, 'classHoursEnd': 1400})
        self.assertEqual(response.context['message'],
                         "You cannot create a lab for an online course")

    def test_create_section_invalid_sectNum(self):
        response = self.c.post('/createsection/', {'courseNumber': '315', 'type': True,
                                                   'sectionNumber': 1232, 'classDays': 'MW',
                                                   'classHoursStart': 1200, 'classHoursEnd': 1400})
        self.assertEqual(response.context['message'],
                         "Section number must be numeric and three digits long")

    def test_create_section_invalid_days(self):
        response = self.c.post('/createsection/', {'courseNumber': '250', 'type': True,
                                                   'sectionNumber': '804', 'classDays': 'S',
                                                   'classHoursStart': 1300, 'classHoursEnd': 1600})
        self.assertEqual(response.context['message'],

                         "Invalid days of the week, please enter days in the format: MWTRF")

    def test_create_section_invalid_times(self):
        response = self.c.post('/createsection/', {'courseNumber': '251', 'type': True,
                                                   'sectionNumber': '802', 'classDays': 'MW',
                                                   'classHoursStart': '17:00', 'classHoursEnd': '20:00'})
        self.assertEqual(response.context['message'],
                         "Invalid start or end time, please use a 4 digit military time representation")



    """
    editPubInfo
    """

    def test_editPubInfo_firstName(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'firstname': 'James', 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Fields successfully updated")

    def test_editPubInfo_lastName(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'firstname': 'Jean Luc', 'lastname': 'Brooks', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Fields successfully updated")

    def test_editPubInfo_two_fields(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'firstname': 'Jean Luc', 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Chicago', 'state': 'Illinois',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Fields successfully updated")


    def test_editPubInfo_homephone_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'firstname': 'Jean Luc', 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                 'password': '90456', 'homephone': 'abc-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})
        self.assertEqual(response.context['message'], "Home Phone can only contain numbers")

    def test_editPubInfo_officephone_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'firstname': 'Jean Luc', 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                 'password': '90456', 'homephone': '123-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '77c-777-7777',
                                                 'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})
        self.assertEqual(response.context['message'], "Office Phone can only contain numbers")

    def test_editPubInfo_zipcode_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'firstname': 'Jean Luc', 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '1111b', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "ZipCode my be only numeric")

    def test_editPubInfo_officenum_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'firstname': 'Jean Luc', 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '5q4', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Office Number must be numeric")

    def test_editPubInfo_firstname_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'firstname': 'Jean Luc12', 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "First Name can only contain letters")

    def test_editPubInfo_lastname_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'firstname': 'Jean Luc', 'lastname': 'Picard12', 'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Last name can only contain letters")

    def test_editPubInfo_city_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'firstname': 'Jean Luc', 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha12', 'state': 'Quadrant',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "City must contain only letters")

    def test_editPubInfo_state_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'firstname': 'Jean Luc', 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant12',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "State must contain only letters")

    def test_editPubInfo_officetimes_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'firstname': 'Jean Luc', 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '9900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Invalid start or end time, please use a "
                                                      "4 digit military time representation")
        response1 = self.c.post('/editpubinfo/',
                               {'firstname': 'Jean Luc', 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '13009'})

        self.assertEqual(response1.context['message'], "Invalid start or end time, please use a "
                                                      "4 digit military time representation")



    """
    Assign Account Course tests 
    """

    def test_assignAccCourse_success(self):
        response = self.c.post('/assignacccourse/', {'userName': 'picard304', 'courseNumber':'351'})
        self.assertEqual(response.context['message'], "Instructor was successfully assigned to class")

    def test_assignAccCourse_course_does_not_exits(self):
        response = self.c.post('/assignacccourse/', {'userName':'picard304', 'courseNumber':'999'})
        self.assertEqual(response.context['message'], "Invalid course number")

    def test_assignAccCourse_user_does_not_exist(self):
        response = self.c.post('assignacccourse/', {'userName':'nothing', 'courseNumber': '351'})
        self.assertEqual(response.context['message'], "Invalid user name")


    """
    Viewing information tests
    """

    def test_viewPublicInfo_not_logged_in(self):
        response = self.c.get('/directory/')
        self.assertEqual(response.context['message'], "You Must log in to View this page")

    def test_viewPublicInfo_success(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/directory/')
