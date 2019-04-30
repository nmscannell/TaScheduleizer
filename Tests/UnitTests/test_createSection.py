from django.test import TestCase
from Commands import createSection
from Main.models import Section, Course


class TestCreateSection(TestCase):

    def setUp(self):
        self.c1 = Course.objects.create(name="TemporalMechanics", number=784, onCampus=True, classDays="MW",
                              classHoursStart=1000, classHoursEnd=1100)

        self.c2 = Course.objects.create(name="WarpTheory", number=633, onCampus=True, classDays="TR", classHoursStart=1200,
                              classHoursEnd=1250)

        self.c3 = Course.objects.create(name="QuantumMechanics", number=709, onCampus=True, classDays="MWF",
                              classHoursStart=1030, classHoursEnd=1145)

        self.c4 = Course.objects.create(name="Linguistics", number=564, onCampus=False, classDays="TR",
                              classHoursStart=1800, classHoursEnd=1930)

        Section.objects.create(course=self.c1, type=1, number=401, meetingDays="W", startTime=1000, endTime=1200)
        Section.objects.create(course=self.c1, type=1, number=402, meetingDays="F", startTime=1400, endTime=1700)
        Section.objects.create(course=self.c1, type=0, number=203, meetingDays="T", startTime=1000, endTime=1200)

    def test_createSection_success(self):
        self.assertEqual(createSection("633", "1", "404", "W", "1300", "1500"), "Section successfully created.")
        self.assertEqual(createSection("633", "0", "204", "W", "1300", "1500"), "Section successfully created.")

    def test_createSection_invalid_course(self):
        self.assertEqual(createSection("M3", "1", "404", "W", "1300", "1500"), "Course number must be numeric and three digits long")
        self.assertEqual(createSection("2008", "1", "404", "W", "1300", "1500"),
                         "Course number must be numeric and three digits long")
        self.assertEqual(createSection("38", "1", "404", "W", "1300", "1500"),
                         "Course number must be numeric and three digits long")

    def test_createSection_courseDNE(self):
        self.assertEqual(createSection("975", "1", "404", "W", "1300", "1500"), "The course does not exist.")

    def test_createSection_invalidType(self):
        self.assertEqual(createSection("633", "-1", "404", "W", "1300", "1500"), "Invalid section type.")
        self.assertEqual(createSection("633", "2", "404", "W", "1300", "1500"), "Invalid section type.")

    def test_createSection_onlineLab_fail(self):
        self.assertEqual(createSection("564", "0", "206", "W", "1300", "1500"), "You cannot create a lab section for an online course.")
        self.assertEqual(createSection("564", "0", "205", "W", "1300", "1500"),
                         "You cannot create a lab section for an online course.")

    def test_createSection_onlineLecture_success(self):
        self.assertEqual(createSection("564", "1", "404", "W", "1300", "1500"), "Section successfully created.")
        self.assertEqual(createSection("564", "1", "408", "W", "1300", "1500"), "Section successfully created.")

    def test_createSection_invalid_sectionNumber(self):
        self.assertEqual(createSection("564", "0", "408", "W", "1300", "1500"), "Lab section number must be 200 level, numeric, and three digits long.")
        self.assertEqual(createSection("564", "0", "2508", "W", "1300", "1500"), "Lab section number must be 200 level, numeric, and three digits long.")
        self.assertEqual(createSection("564", "0", "2m8", "W", "1300", "1500"), "Lab section number must be 200 level, numeric, and three digits long.")
        self.assertEqual(createSection("564", "1", "208", "W", "1300", "1500"), "Lecture section number must be 400 level, numeric, and three digits long.")
        self.assertEqual(createSection("564", "1", "48", "W", "1300", "1500"), "Lecture section number must be 400 level, numeric, and three digits long.")
        self.assertEqual(createSection("564", "1", "40i8", "W", "1300", "1500"), "Lecture section number must be 400 level, numeric, and three digits long.")

    def test_createSection_alreadyExists(self):
        self.assertEqual(createSection("784", "1", "401", "W", "1300", "1500"), "Section already exists; section not added.")
        self.assertEqual(createSection("784", "1", "402", "W", "1300", "1500"), "Section already exists; section not added.")
        self.assertEqual(createSection("784", "0", "203", "W", "1300", "1500"), "Section already exists; section not added.")

    def test_createSection_invalidTimes(self):
        self.assertEqual(createSection("784", "1", "401", "W", "130", "1500"), "Invalid start or end time, please use a 4 digit military time representation")
        self.assertEqual(createSection("784", "1", "401", "W", "13m0", "1500"), "Invalid start or end time, please use a 4 digit military time representation")
        self.assertEqual(createSection("784", "1", "401", "W", "8300", "1500"), "Invalid start or end time, please use a 4 digit military time representation")
        self.assertEqual(createSection("784", "1", "401", "W", "1300", "3500"), "Invalid start or end time, please use a 4 digit military time representation")
        self.assertEqual(createSection("784", "1", "401", "W", "1300", "1100"), "End time must be after start time.")
