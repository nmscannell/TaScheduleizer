from django.test import TestCase
from Main.models import Account, Course, AccountCourse
from Commands import assignAccCourse

class TestAssignAccCourse(TestCase):
    def setUp(self):
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
        Account.objects.create(userName="bones837", firstName="Leonard", lastName="McCoy", password="851468",
                               email="bones837@uwm.com", title=3, address="789 Enterprise Avenue",
                               city="Alpha", state="Quadrant", zipCode="89765", officeNumber="987",
                               officePhone="897-654-398", officeDays="MW", officeHoursStart="1500",
                               officeHoursEnd="1600", currentUser=False)
        Course.objects.create(name="Temporal Mechanics", number="581", onCampus=True)
        Course.objects.create(name="Warp Theory", number="468", onCampus=True)
        Course.objects.create(name="Political Turmoil in the Klingon Empire", number="492", onCampus=False)

    def test_assign_success(self):
        self.assertEqual(assignAccCourse("janewayk123", "Temporal Mechanics"), "User was successfully assigned to course")
        self.assertEqual(assignAccCourse("picard304", "Warp Theory"), "User was successfully assigned to course")
        self.assertEqual(assignAccCourse("janewayk123", "Political Turmoil in the Klingon Empire"), "User was successfully assigned to course")
        self.assertEqual(assignAccCourse("picard304", "Political Turmoil in the Klingon Empire"), "User was successfully assigned to course")

    def test_assign_invalid_course(self):
        self.assertEqual(assignAccCourse("janewayk123", "Ethics of the Prime Directive"), "Course does not exist")
        self.assertEqual(assignAccCourse("picard304", "How to Deal with Children"), "Course does not exist")

    def test_assign_nonexistent_acct(self):
        self.assertEqual(assignAccCourse("tuvix009", "Temporal Mechanics"), "Invalid user name")
        self.assertEqual(assignAccCourse("SevenOf9", "Warp Theory"), "Invalid user name")
        self.assertEqual(assignAccCourse("Mudd847", "Warp Theory"), "Invalid user name")

    def test_assign_invalid_title(self):
        self.assertEqual(assignAccCourse("kirkj22", "Temporal Mechanics"), "User is not an instructor or TA")
        self.assertEqual(assignAccCourse("bones837", "Temporal Mechanics"), "User is not an instructor or TA")
