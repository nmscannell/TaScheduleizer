from django.test import TestCase
from Main.models import Account, Course, AccountCourse, Section, AccountSection
from Commands import displayCourseAssign


class TestDisplayCourseAssign(TestCase):

    def setUp(self):
        self.c1 = Course.objects.create(name="Intro", number=333)
        # self.account1 = Account.objects.create(userName="hsimpson", firstName="Homer", lastName="Simpson", title=2)
        # self.account2 = Account.objects.create(userName="cwhitley", firstName="Chip", lastName="Whitley", title=1)
        # AccountCourse.objects.create(Account=self.account1, Course=self.c1)
        # AccountCourse.objects.create(Account=self.account2, Course=self.c1)
        # self.section1 = Section.objects.create(course=self.c1, type=1, number='002')
        # self.section2 = Section.objects.create(course=self.c1, type=0, number=604)
        # AccountSection.objects.create(Account=self.account1, Section=self.section1)
        # AccountSection.objects.create(Account=self.account2, Section=self.section2)

    def test_displayCourseAssign_Empty(self):
        self.assertMultiLineEqual(displayCourseAssign(333), "Intro CS333\n"
                                                            "Instructors: None\n"
                                                            "Teaching Assistants: None\n"
                                                            "No sections found")

    def test_displayCourseAssign_1_Lec(self):
        self.section1 = Section.objects.create(course=self.c1, type=1, number=123)

        self.assertMultiLineEqual(displayCourseAssign(333), "Intro CS333\n"
                                                            "Instructors: None\n"
                                                            "Teaching Assistants: None\n"
                                                            "LEC 123: None\n")

    def test_displayCourseAssign_1_Lec_1_lab(self):
        self.section1 = Section.objects.create(course=self.c1, type=1, number=123)
        self.section2 = Section.objects.create(course=self.c1, type=0, number=604)

        self.assertMultiLineEqual(displayCourseAssign(333), "Intro CS333\n"
                                                            "Instructors: None\n"
                                                            "Teaching Assistants: None\n"
                                                            "LEC 123: None\n"
                                                            "LAB 604: None\n")

    def test_displayCourse_2_lec_2_Lab(self):
        self.section1 = Section.objects.create(course=self.c1, type=1, number=123)
        self.section2 = Section.objects.create(course=self.c1, type=0, number=604)
        self.section3 = Section.objects.create(course=self.c1, type=1, number=321)

        self.assertMultiLineEqual(displayCourseAssign(333), "Intro CS333\n"
                                                            "Instructors: None\n"
                                                            "Teaching Assistants: None\n"
                                                            "LEC 123: None\n"
                                                            "LAB 604: None\n")
