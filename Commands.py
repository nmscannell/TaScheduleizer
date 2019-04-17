from Main.models import Account, Course, Section, AccountSection, AccountCourse
import re


class Command():

    def __init__(self, opcode, arguments, function):
        self.opcode = opcode
        self.arguments = arguments
        self.function = function


def login(userName, password):
    test = Account.objects.filter(currentUser=True)
    if len(test) > 0:
        return "A user is already logged in"


    try:
        CurrentUser = Account.objects.get(userName=userName)
        if CurrentUser.password != password:
            return "Incorrect password"

    except Account.DoesNotExist:
        return "Account Not Found"

    CurrentUser.currentUser = True
    CurrentUser.save()
    return "Logged in as " + userName


def logout():
    try:
        CurrentUser = Account.objects.get(currentUser=True)
        CurrentUser.currentUser = False
        CurrentUser.save()
        return "Successfully logged out"
    except Account.DoesNotExist:
        return "Please log in First"
    except Account.MultipleObjectsReturned:
        return "Multiple account Logged in, Something went terribly wrong"


def createAccount(firstName, lastName, userName, email, title):
    # Check that the command has the correct number of arguments

    # Check that the account trying to be created does not already exist
    if Account.objects.filter(userName=userName).exists():
        return "Account already exists"

    # Make sure the account is trying to be created with a UWM email address
    str = email.split('@', 1)
    if len(str) == 1:
        return "The email address you have entered in not valid.  " \
               "Please make sure you are using a uwm email address in the correct format."
    if str[1] != "uwm.edu":
        return "The email address you have entered in not valid.  " \
               "Please make sure you are using a uwm email address in the correct format."

    # If we get here the account is safe to be created.
    else:
        A = Account()
        A.userName = userName
        A.email = email
        if title.lower() == "ta":
            A.title = 1
        elif title.lower() == "instructor":
            A.title = 2
        else:
            return "Invalid title, account not created"
        A.firstName = firstName
        A.lastName = lastName
        # Make a temporary password for the newly created user
        A.password = A.userName + "456"
        A.save()

        return "Account successfully created.  Temporary password is: " + A.userName + "456"


def deleteAccount(userName):
    pass


def createCourse(name, number, online, days, start, end):
    # Check that the command has the appropriate number of arguments

    # Course number checks
    if not re.match('^[0-9]*$', number):
        return "Course number must be numeric and three digits long"
    if len(number) != 3:
        return "Course number must be numeric and three digits long"
    # Check that the course does not already exist
    if Course.objects.filter(number=number).exists():
        return "Course already exists"
    # Location checks
    if online.lower() != "online" and online.lower() != "campus":
        return "Location is invalid, please enter campus or online."
    # Days check
    for i in days:
        if i not in 'MTWRFN':
            return "Invalid days of the week, please enter days in the format: MWTRF or NN for online"
    # Check times
    startTime = start
    endTime = end
    if len(startTime) != 4 or len(endTime) != 4:
        return "Invalid start or end time, please use a 4 digit military time representation"
    if not re.match('^[0-2]*$', startTime[0]) or not re.match('^[0-1]*$', endTime[0]):
        return "Invalid start or end time, please use a 4 digit military time representation"
    for i in range(1, 3):
        if not (re.match('^[0-9]*$', startTime[i])) or not (re.match('^[0-9]*$', endTime[i])):
            return "Invalid start or end time, please use a 4 digit military time representation"

    # Else the course is ok to be created
    else:
        c = Course(name=name, number=number)
        if online.lower() == "online":
            c.onCampus = False
        else:
            c.onCampus = True
            c.classDays = days
            c.classHoursStart = start
            c.classHoursEnd = end
        c.save()
        return "Course successfully created"


def createSection(courseNumber, type, sectionNumber, days, start, end):
    pass


def assignAccCourse(userName, courseNumber):
    pass


def assignAccSection(userName, courseNumber, sectionNumber):
    pass


def viewCourseAssign(userName):
    pass


def getCommands():
    commandList = [Command("login", 2, login), Command("logout", 0, logout),
                   Command("createAccount", 5, createAccount), Command("deleteAccount", 1, deleteAccount),
                   Command("createCourse", 6, createCourse), Command("createSection", 6, createSection),
                   Command("assignAccCourse", 2, assignAccCourse),
                   Command("assignAccSection", 3, assignAccSection),
                   Command("viewCourseAssign", 1, viewCourseAssign)]
    return commandList
