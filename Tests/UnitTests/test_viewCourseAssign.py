from django.test import TestCase
from Commands import viewCourseAssign
from Main.models import Account, Course, Section, AccountSection, AccountCourse


class TestViewCourseAssign(TestCase):

    def setUp(self):
            self.account1 = Account.objects.create(userName='instructor', title='2', firstName="Chip", lastName="Whitley")
            self.account2 = Account.objects.create(userName='taman', title='1', firstName="Rob", lastName="Buzzsaw")
            self.account3 = Account.objects.create(userName='joe', title='1', firstName="Joe", lastName="Cool")
            self.account4 = Account.objects.create(userName='admin', title='3', firstName="Jedediah", lastName="Longtree")
            self.course1 = Course.objects.create(number='361', name='IntroSoftwareEngineering')
            self.course2 = Course.objects.create(number='101', name='English')
            self.course3 = Course.objects.create(name='History', number='101')
            self.lab1 = Section.objects.create(number='801', course=self.course1)
            AccountCourse.objects.create(Account=self.account1, Course=self.course1)
            AccountCourse.objects.create(Account=self.account1, Course=self.course2)
            AccountCourse.objects.create(Account=self.account2, Course=self.course1)
            AccountSection.objects.create(Account=self.account2, Section=self.lab1)

    def test_viewCourseAssign_accountNotFound(self):
        self.assertEqual(viewCourseAssign("homer"), "Account not found")

    def test_viewCourseAssign_noAssignments(self):
        self.assertEqual(viewCourseAssign("joe"), "joe does not have any assignments")

    def test_viewCourseAssign_Instructor_1Course(self):
        AccountCourse.objects.get(Account=self.account1, Course=self.course2).delete()

        self.assertEqual(viewCourseAssign("instructor"), "Chip Whitley is assigned to: IntroSoftwareEngineering")

    def test_viewCourseAssign_Instructor_2Course(self):

        self.assertEqual(viewCourseAssign("instructor"), "Chip Whitley is assigned to: IntroSoftwareEngineering, English")

    def test_viewCourseAssign_TA_CourseLab(self):

        self.assertEqual(viewCourseAssign("taman"), "Rob Buzzsaw is assigned to: LAB 801")

    def test_viewCourseAssign_Ta_2CourseLab(self):
        self.lab2 = Section.objects.create(number='801', course=self.course2)
        AccountSection.objects.create(Account=self.account2, Section=self.lab2)

        self.assertEqual(viewCourseAssign("taman"),
                         "Rob Buzzsaw is assigned to: IntroSoftwareEngineering section 801, English section 801")

    def test_viewCourseAssign_Ta_2CourseLab_1Course(self):
        self.lab2 = Section.objects.create(number='801', course=self.course2)
        AccountSection.objects.create(Account=self.account2, Section=self.lab2)
        AccountCourse.objects.create(Account=self.account2, Course=self.course3)

        self.assertEqual(viewCourseAssign("taman"),
                         "taman is assigned to: IntroSoftwareEngineering section 801, English section 801, History")

    def test_viewCourseAssign_TA_noLabs(self):
        AccountSection.objects.get(Account=self.account2).delete()

        self.assertEqual(viewCourseAssign("taman"), "Rob Buzzsaw is assigned to: IntroSoftwareEngineering")

    def test_viewCourseAssign_Ta_1CourseLab_1Course(self):
        AccountCourse.objects.create(Account=self.account2, Course=self.course2)

        self.assertEqual(viewCourseAssign("taman"), "Rob Buzzsaw is assigned to: LAB 801, English")
