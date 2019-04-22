from django.db import models

# Create your models here.


class Account(models.Model):
    userName = models.CharField(max_length=20, default=" ")
    firstName = models.CharField(max_length=20, default=" ")
    lastName = models.CharField(max_length=20, default=" ")
    password = models.CharField(max_length=20, default="password")
    email = models.EmailField(default="")
    homePhone = models.CharField(max_length=12, default="")
    title = models.IntegerField(default=0)
    address = models.CharField(max_length=30, default=" ")
    city = models.CharField(max_length=20, default=" ")
    state = models.CharField(max_length=20, default=" ")
    zipCode = models.IntegerField()
    officeNumber = models.IntegerField()
    officePhone = models.CharField(max_length=12, default="")
    officeDays = models.CharField(max_length=10, default=" ")
    officeHoursStart = models.IntegerField()
    officeHoursEnd = models.IntegerField()
    currentUser = models.BooleanField(default=False)

    def __str__(self):
        return self.firstName + " " + self.lastName

    def displayPrivate(self):
        t=""
        if self.title == 1:
            t = "Teaching Assistant"
        else:
            t = "Instructor"
        return str(self.firstName) + " " + str(self.lastName) + "\n" + t + "\nHome Phone: " + str(self.homePhone) + \
            "\nEmail: " + str(self.email) + "\n" + str(self.address) + "\n" + str(self.city) + " " + str(self.state) \
            + " " + str(self.zipCode) + "\n" + "Office: " + str(self.officeNumber) + "\nOffice Phone: " + \
            str(self.officePhone) + "\nOffice Hours: " + str(self.officeDays) + " " + str(self.officeHoursStart) + " " \
            + str(self.officeHoursEnd)

    def displayPublic(self):
        t = ""
        if self.title == 1:
            t = "Teaching Assistant"
        else:
            t = "Instructor"
        return str(self.firstName) + " " + str(self.lastName) + "\n" + t + "\nEmail: " + str(self.email) + "\n" + \
            "Office: " + str(self.officeNumber) + "\nOffice Phone: " + str(self.officePhone) + "\nOffice Hours: " + \
            str(self.officeDays) + " " + str(self.officeHoursStart) + " " + str(self.officeHoursEnd)


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
        return str(self.Account) + " " + str(self.Course)


class Section(models.Model):

    course = models.ForeignKey(Course, default=None, on_delete=models.CASCADE)
    type = models.IntegerField(default=0)
    number = models.IntegerField(default=000)
    meetingDays = models.CharField(max_length=10, default=" ")
    startTime = models.IntegerField(default=0000)
    endTime = models.IntegerField(default=0000)

    def __str__(self):
        id = ""
        if self.type == 1:
            id = "LEC"
        else:
            id = "LAB"
        return id + " " + str(self.number)


class AccountSection(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Account) + " " + str(self.Section)


