from django.db import models
from Main.models import Account, Course


class AccountCourse(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Account) + " " + str(self.Course)