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

        Section.objects.create(course=self.c1, type=1, number=201, meetingDays="W", startTime=1000, endTime=1200)
        Section.objects.create(course=self.c1, type=1, number=202, meetingDays="F", startTime=1400, endTime=1700)
        Section.objects.create(course=self.c1, type=1, number=203, meetingDays="T", startTime=1000, endTime=1200)

    def test_createSection_success(self):
        self.assertEqual(createSection("633", "1", "604", "W", "1300", "1500"), "Lab successfully created")
