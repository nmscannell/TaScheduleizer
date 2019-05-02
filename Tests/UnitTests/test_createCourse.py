from django.test import TestCase
import Commands
from Main.models import Course


class Test_CreateCourse(TestCase):

    def setUp(self):
        Course.objects.create(name="TemporalMechanics", number=784, onCampus=True)

        Course.objects.create(name="WarpTheory", number=633, onCampus=False)

    def test_course_successfully_created(self):
        self.assertEqual(Commands.createCourse("NebulaStudies", "432", "Campus"),
                         "Course successfully created")
        self.assertEqual(Commands.createCourse("StarshipDesign", "275", "Online"),
                         "Course successfully created")

        A = Course.objects.get(name="NebulaStudies")
        self.assertEqual(A.name, "NebulaStudies")
        self.assertEqual(A.number, 432)
        self.assertEqual(A.onCampus, True)
        #self.assertEqual(A.classDays, "MW")
        #self.assertEqual(A.classHoursStart, 1300)
        #self.assertEqual(A.classHoursEnd, 1400)

        B = Course.objects.get(name="StarshipDesign")
        self.assertEqual(B.name, "StarshipDesign")
        self.assertEqual(B.number, 275)
        self.assertEqual(B.onCampus, False)
        #self.assertEqual(B.classDays, " ")
        #self.assertEqual(B.classHoursStart, 0000)
        #self.assertEqual(B.classHoursEnd, 0000)

    def test_create_course_already_exists(self):
        self.assertEqual(Commands.createCourse("TemporalMechanics", "784", "Campus"),
                         "Course already exists")

    def test_create_course_invalid_courseNum(self):
        self.assertEqual(Commands.createCourse("DilithiumHarvesting", "abc", "Campus",),
                         "Course number must be numeric and three digits long")
        self.assertEqual(Commands.createCourse("DilithiumHarvesting", "1op", "Campus"),
                         "Course number must be numeric and three digits long")
        self.assertEqual(Commands.createCourse("DilithiumHarvesting", "1u9", "Campus"),
                         "Course number must be numeric and three digits long")

    def test_invalid_location(self):
        self.assertEqual(Commands.createCourse("DilithiumHarvesting", "450", "Mars"),
                         "Location is invalid, please enter campus or online.")

    #def test_invalid_days(self):
    #    self.assertEqual(Commands.createCourse("InterspeciesEthics", "307", "Online", "q", "1200", "1300"),
    #                     "Invalid days of the week, please enter days in the format: MWTRF or NN for online")
    #    self.assertEqual(Commands.createCourse("InterspeciesEthics", "307", "Online", "123", "1200", "1300"),
    #                     "Invalid days of the week, please enter days in the format: MWTRF or NN for online")
    #    self.assertEqual(Commands.createCourse("InterspeciesEthics", "307", "Online", "My", "1200", "1300"),
    #                     "Invalid days of the week, please enter days in the format: MWTRF or NN for online")

    #def test_invalid_times(self):
    #    self.assertEqual(Commands.createCourse( "InterspeciesEthics", "207", "Campus", "M", "abcd", "1400"),
    #                     "Invalid start or end time, please use a 4 digit military time representation")
    #    self.assertEqual(Commands.createCourse("InterspeciesEthics", "207", "Campus", "M", "1300", "abcd"),
    #                     "Invalid start or end time, please use a 4 digit military time representation")
    #    self.assertEqual(Commands.createCourse("InterspeciesEthics", "207", "Campus", "M", "9000", "1200"),
    #                     "Invalid start or end time, please use a 4 digit military time representation")
    #    self.assertEqual(Commands.createCourse("InterspeciesEthics", "207", "Campus", "M", "1200", "6079"),
    #                     "Invalid start or end time, please use a 4 digit military time representation")

    #def test_times_out_of_order(self):
    #    self.assertEqual(Commands.createCourse("InterspeciesEthics", "207", "Campus", "M", "1200", "0900"),
    #                     "The course end time must be after the course start time")
    #    self.assertEqual(Commands.createCourse("InterspeciesEthics", "207", "Campus", "M", "1400", "1200"),
    #                     "The course end time must be after the course start time")

    def test_course_with_name_exists(self):
        self.assertEqual(Commands.createCourse("WarpTheory", "207", "Campus"),
                         "A course with this name already exists")

