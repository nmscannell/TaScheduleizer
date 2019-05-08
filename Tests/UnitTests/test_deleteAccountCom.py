from django.test import TestCase
from Main.models import Course
from Commands import deleteCourseCom


class TestDeleteAccountCom(TestCase):

    def setUp(self):
        Course.objects.create(name="Dance")

    def test_deleteAccountCom_success(self):
        self.assertEqual(Course.objects.count(), 1)
        message = deleteCourseCom("Dance")
        self.assertEqual(message, "Course successfully deleted")
        self.assertEqual(Course.objects.count(), 0)

    def test_deleteCourseCom_notfound(self):
        self.assertEqual(Course.objects.count(), 1)
        message = deleteCourseCom("Lunch")
        self.assertEqual(message, "Course does not exist")
        self.assertEqual(Course.objects.count(), 1)
