from django.db import models

# Create your models here.


class Account(models.Model):
    userName = models.CharField(max_length=20, default=" ")
    firstName = models.CharField(max_length=20, default=" ")
    lastName = models.CharField(max_length=20, default=" ")
    password = models.CharField(max_length=20, default="password")
    email = models.EmailField(default="")
    title = models.IntegerField(default=0)
    address = models.CharField(max_length=30, default=" ")
    city = models.CharField(max_length=20, default=" ")
    state = models.CharField(max_length=20, default=" ")
    zipCode = models.IntegerField(default=00000)
    officeNumber = models.IntegerField(default=000)
    officePhone = models.CharField(max_length=12, default="000-000-0000")
    officeDays = models.CharField(max_length=10, default=" ")
    officeHoursStart = models.IntegerField(default=0000)
    officeHoursEnd = models.IntegerField(default=0000)
    currentUser = models.BooleanField(default=False)

    def __str__(self):
        return self.userName


class Course(models.Model):
    name = models.CharField(max_length=20, default=" ")
    number = models.IntegerField(default=000)
    onCampus = models.BooleanField(default=True)
    classDays = models.CharField(max_length=10, default=" ")
    classHoursStart = models.IntegerField(default=0000)
    classHoursEnd = models.IntegerField(default=0000)

    def __str__(self):
        return self.name


class AccountCourse(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Instructor) + " " + str(self.Course)


class Section(models.Model):

    course = models.ForeignKey(Course, default=None, on_delete=models.CASCADE)
    type = models.IntegerField()
    number = models.IntegerField(default=000)
    meetingDays = models.CharField(max_length=10, default=" ")
    startTime = models.IntegerField(default=0000)
    endTime = models.IntegerField(default=0000)

    def __str__(self):
        return str(self.course) + " section " + str(self.sectionNumber)


class AccountSection(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.TA) + " " + str(self.Lab)


