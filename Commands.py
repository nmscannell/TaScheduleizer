from Main.models import Account, Course, Section, AccountSection
from AccountCourse.models import AccountCourse
import CurrentUserHelper
import re
from itertools import chain


class Command():

    def __init__(self, opcode, arguments, function):
        self.opcode = opcode
        self.arguments = arguments
        self.function = function


def login(userName, password):

    try:
        CurrentUser = Account.objects.get(userName=userName)
        if CurrentUser.password != password:
            raise Exception("Incorrect password")
        CurrentUser.currentUser = True
    except Account.DoesNotExist:
        raise Exception("Account Not Found")

    return CurrentUser


def logout(user):
    try:
        user.currentUser = False
        user.save()
        return "Successfully logged out"
    except Account.DoesNotExist:
        return "Please log in First"
    except Account.MultipleObjectsReturned:
        return "Multiple account Logged in, Something went terribly wrong"


def checkValidEmail(email):
    str = email.split('@', 1)
    if len(str) == 1 or str[1] != "uwm.edu":
        return False
    return True


def containsOnlyDigits(argument):
    if not re.match('^[0-9]*$', argument):
        return False
    return True


def checkValidTimes(time):
    return re.match('^[0-1][0-9][0-5][0-9]$', time) or re.match('^[2][0-3][0-5][0-9]', time)
    ###if the first digit is 2, only 0-3 is allowed for the second digit


def checkValidDays(days):
    daysnospaces = days.replace(" ", "")
    for i in daysnospaces:
        if i not in 'MTWRFN':
            return False
    return True


# Creating an Account
def createAccount(firstName, lastName, userName, title, email):

    # Check that the account trying to be created does not already exist
    if Account.objects.filter(userName=userName).exists():
        return "Account already exists"

    # Make sure the account is trying to be created with a UWM email address
    if not checkValidEmail(email):
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


def deleteAccountCom(userName):

    try:
        a = Account.objects.get(userName=userName)
    except Exception as e:
        return "Account does not exist"
    a.delete()
    return "Account successfully deleted"


def createCourse(name, number, online):
    # Check that the command has the appropriate number of arguments

    # Course number checks
    if not re.match('^[0-9]{3}$', number):
        return "Course number must be numeric and three digits long"

    # Check that the course does not already exist
    if Course.objects.filter(number=number).exists():
        return "Course already exists"
    if Course.objects.filter(name=name).exists():
        return "A course with this name already exists"
    # Location checks
    if online.lower() != "online" and online.lower() != "campus":
        return "Location is invalid, please enter campus or online."

    # Else the course is ok to be created
    else:
        c = Course()
        c.name = name
        c.number = number
        if online.lower() == "online":
            c.onCampus = False
        else:
            c.onCampus = True
        c.save()
        return "Course successfully created"


def createSection(courseNumber, type, sectionNumber, days, start, end):
    # Course number checks

    if not re.match('^[0-9]{3}$', courseNumber):
        return "Course number must be numeric and three digits long"

    # Make sure course that the lab is being created for exists ok
    try:
        c = Course.objects.get(number=courseNumber)
    except Course.DoesNotExist:
        return "The course does not exist."

    if type != "0" and type != "1":
        return "Invalid section type."

    # Section number checks

    if type == "0" and not re.match('^2[0-9]{2}$', sectionNumber):
        return "Lab section number must be 200 level, numeric, and three digits long."

    if type == "1" and not re.match('^4[0-9]{2}$', sectionNumber):
        return "Lecture section number must be 400 level, numeric, and three digits long."

    # Make sure the course is not online
    if not c.onCampus and type == "0":
        return "You cannot create a lab section for an online course."

    days = days.upper()

    # Days check
    for i in days:
        if i not in 'MTWRF':
            return "Invalid days of the week, please enter days in the format: MWTRF"

    # Time checks
    if not checkValidTimes(start) or not checkValidTimes(end):
        return "Invalid start or end time, please use a 4 digit military time representation"
    if end <= start:
        return "End time must be after start time."

    # Make sure the lab does not already exist
    if Section.objects.filter(course=c, number=sectionNumber).exists():
        return "Section already exists; section not added."

    l = Section()
    l.course = c
    l.type = type
    l.number = sectionNumber
    if c.onCampus:
        l.meetingDays = days
        l.startTime = start
        l.endTime = end
    else:
        l.meetingDays = ""
        l.startTime = 0000
        l.endTime = 0000
    l.save()
    return "Section successfully created."


def assignAccCourse(userName, courseName):
    # Check if the course is valid
    if not Course.objects.filter(name=courseName).exists():
        return "Course does not exist"
    # Check if the user name is valid
    if not Account.objects.filter(userName=userName).exists():
        return "Invalid user name"

    instructor = Account.objects.get(userName=userName)
    course = Course.objects.get(number=Course.objects.get(name=courseName).number)

    if AccountCourse.objects.filter(Account=instructor, Course=course).exists():
        return "User already assigned to course"
    # title represented as an integer where 4=supervisor 3=administrator
    # 2=Instructor 1=TA. 0=No current User
    # Check if the account is an instructor
    # Check if the course is already assigned
    # Otherwise(if there are no errors found), an instructor can be assigned to a course
    if instructor.title > 2:
        return "User is not an instructor or TA"
    a = AccountCourse()
    a.Account = instructor
    a.Course = course
    a.save()
    return "User was successfully assigned to course"


def assignAccSection(userName, courseNumber, sectionNumber):
    if not Account.objects.filter(userName=userName).exists():
        return "Invalid user name"

    account = Account.objects.get(userName=userName)

    if account.title > 2:
        return "User is not an instructor or TA"

    if not Course.objects.filter(number=courseNumber).exists():
        return "Invalid course number"

    course = Course.objects.get(number=courseNumber)

    if not AccountCourse.objects.filter(Account=account, Course=Course.objects.get(number=courseNumber)).exists():
        return "User must be assigned to the course first"

    if not Section.objects.filter(number=sectionNumber, course=course).exists():
        return "Invalid lab section"

    if account.title == 2:
        if not re.match('^4[0-9]{2}$', sectionNumber):
            return "Instructors must be assigned to 400 level sections."

    if account.title == 1 and not re.match('^2[0-9]{2}$', sectionNumber):
        return "TAs must be assigned to 200 level sections."

    lab = Section.objects.get(number=sectionNumber, course=course)

    if AccountSection.objects.filter(Section=lab).exists():
        return "Course section already assigned"

    p = AccountSection()
    p.Account = account
    p.Section = lab
    p.save()

    return "User successfully assigned to course section"


def displayAllCourseAssign():
    lst = Course.objects.all()
    courseList = []

    for a in lst:
        courseList.append(displayCourseAssign(a.number))

    return courseList


def displayCourseAssign(courseNumber):
    course = Course.objects.get(number=courseNumber)

    response = course.name + " CS" + str(course.number) + "\n"

    lst = AccountCourse.objects.filter(Course=course)
    instructorList = []

    for a in lst:
        if a.Account.title == 2:
            instructorList.append(str(a.Account))

    response += "Instructors: "
    if not instructorList:
        response += "None"
    else:
        response += ", ".join(instructorList)


    response += "\nTeaching Assistants: "

    taList = []

    for a in lst:
        if a.Account.title == 1:
            taList.append(str(a.Account))

    if not taList:
        response += "None"
    else:
        response += ", ".join(taList)
    response += "\n"
    lecSectionList = Section.objects.filter(course=course, type=1)
    labSectionList = Section.objects.filter(course=course, type=0)
    if not lecSectionList and not labSectionList:
        response += "No sections found"
        return response
    else:
        for a in lecSectionList:
            p = AccountSection.objects.filter(Section=a)
            if not p:
                response += str(a) + ": None\n"
            else:
                for q in p:
                    response += str(q.Section) + ": " + str(q.Account) + "\n"
        for a in labSectionList:
            p = AccountSection.objects.filter(Section=a)
            if not p:
                response += str(a) + ": None\n"
            else:
                for q in p:
                    response += str(q.Section) + ": " + str(q.Account) + "\n"

    return response


def viewCourseAssign(userName): # secret message
    if not Account.objects.filter(userName=userName).exists():
        return "Account not found"

    account = Account.objects.get(userName=userName)

    if not AccountCourse.objects.filter(Account=account).exists():
        return str(account) + " does not have any assignments"

    labAssignments = AccountSection.objects.filter(Account=account)

    response = str(account) + " is assigned to: "
    labList = []
    checkList = []
    for a in labAssignments:
        labList.append(str(a.Section))
        checkList.append(a.Section.course)

    response += ", ".join(labList)

    courseAssignments = AccountCourse.objects.filter(Account=account)

    courseList = []
    first = True
    for a in courseAssignments:
        if a.Course not in checkList:
            if first and len(labAssignments) != 0:# all this does is puts a comma after lab sections if present
                response += ", "
                first = False
            courseList.append(str(a.Course))

    response += ", ".join(courseList)

    return response


def getPublicDataList():
    instructorList = Account.objects.filter(title=2)
    taList = Account.objects.filter(title=1)
    staffList = instructorList | taList
    directory = []

    for i in staffList:
        directory.append(i.displayPublic())

    directory.sort()
    return directory


def getPrivateDataList():
    instructorList = Account.objects.filter(title=2)
    taList = Account.objects.filter(title='1')
    staffList = instructorList | taList
    directory = []

    for i in staffList:
        directory.append(i.displayPrivate())

    directory.sort()
    return directory


def editPubInfo(user, dict):
    startdefault = Account._meta.get_field('officeHoursStart').get_default()
    enddefault = Account._meta.get_field('officeHoursEnd').get_default()
    daysdefault = Account._meta.get_field('officeDays').get_default()
    officeHoursStart = dict['officestart']
    officeHoursEnd = dict['officeend']

    firstName = dict['firstName']
    if firstName != user.firstName:
        if not firstName.replace(" ", "").isalpha():
            return "First Name can only contain letters"
        user.firstName = firstName
        user.save()


    lastName = dict['lastName']
    if lastName != user.lastName:
        if not lastName.replace(" ", "").isalpha():
            return "Last name can only contain letters"
        user.lastName = lastName
        user.save()


    # Email
    email = dict['email']
    if email != user.email:
        if checkValidEmail(email) == False:
            return "The email address you have entered in not valid.  " \
                "Please make sure you are using a uwm email address in the correct format."
        else:
            user.email = email
            user.save()

    # Password
    password = dict['password']
    if password != user.password:
        user.password = password
        user.save()

    # Home phone
    homePhone = dict['homephone']
    if homePhone != str(user.homePhone):
        if containsOnlyDigits(homePhone.replace("-", "")) == False:
            return "Home Phone can only contain numbers"
        else:
            user.homePhone = homePhone
            user.save()

    # Address
    address = dict['address']
    if address != user.address:
        user.address = address
        user.save()

    # City
    city = dict['city']
    if city != user.city:
        if not city.replace(" ", "").isalpha():
            return "City must contain only letters"
        user.city = city
        user.save()

    # State
    state = dict['state']
    if state != user.state:
        if not state.replace(" ", "").isalpha():
            return "State must contain only letters"
        user.state = state
        user.save()

    # Zip Code
    zipCode = dict['zipcode']
    if zipCode != str(user.zipCode):
        if containsOnlyDigits(zipCode) == False:
            return "ZipCode my be only numeric"
        else:
            user.zipCode = zipCode
            user.save()

    # Office Number
    officeNumber = dict['officenumber']
    if officeNumber != str(user.officeNumber):
        if containsOnlyDigits(officeNumber) == False:
            return "Office Number must be numeric"
        else:
            user.officeNumber = officeNumber
            user.save()

    # Office phone
    officePhone = dict['officephone']
    if officePhone != str(user.officePhone):
        if containsOnlyDigits(officePhone.replace("-", "")) == False:
            return "Office Phone can only contain numbers"
        else:
            user.officePhone = officePhone
            user.save()

    # Office days
    officeDays = dict['officedays']
    if officeDays != user.officeDays:
        if not checkValidDays(officeDays):
            return "Invalid days of the week, please enter days in the format: MWTRF or NN for online"

    # Start Time and End Time
    # Enter a start time but not an end time
    if officeHoursStart != str(startdefault) and (officeHoursEnd == str(enddefault) or officeHoursEnd == ""):
        user.officeHoursStart = startdefault
        user.save()
        return "You must enter both a start and end time for office hours"

    # Enter an end time but not a start time.
    if officeHoursEnd != str(startdefault) and (officeHoursStart == str(startdefault) or officeHoursStart == ""):
        user.officeHoursEnd = enddefault
        user.save()
        return "You must enter both a start and end time for office hours"

    # Enter a start time and an end time, but not days
    if officeHoursEnd != str(enddefault) and officeHoursStart != str(startdefault) and \
            (officeDays == str(daysdefault) or officeDays == ""):
        user.officeHoursEnd = enddefault
        user.officeHoursStart = startdefault
        user.save()
        return "You must enter office days if you enter office hours"

    #Enter office days, but not a start time or an end time
    if officeDays != str(daysdefault) and (officeHoursStart == str(startdefault) or officeHoursEnd == str(enddefault)
                                           or officeHoursStart == "" or officeHoursEnd == ""):
        user.officeDays = daysdefault
        user.officeHoursStart = startdefault
        user.officeHoursEnd = enddefault
        user.save()
        return "You must enter office hours if you enter office days"

    #Check start time is valid
    if (officeHoursStart != str(user.officeHoursStart) and officeHoursStart != ""):
        if not checkValidTimes(officeHoursStart):
            user.officeHoursEnd = enddefault
            user.officeHoursStart = startdefault
            user.save()
            return "Invalid start or end time, please use a 4 digit military time representation"
        else:
            user.officeHoursStart = officeHoursStart

    # Check end time is valid
    if (officeHoursEnd != str(user.officeHoursEnd) and officeHoursEnd != ""):
        if not checkValidTimes(officeHoursEnd):
            user.officeHoursEnd = enddefault
            user.officeHoursStart = startdefault
            user.save()
            return "Invalid start or end time, please use a 4 digit military time representation"
        else:
            user.officeHoursEnd = officeHoursEnd
    user.officeDays = officeDays
    user.save()


    return "Fields successfully updated"


def getCommands():
    return [Command("login", 2, login), Command("logout", 0, logout),
            Command("createaccount", 5, createAccount), Command("deleteaccount", 1, deleteAccountCom),
            Command("createcourse", 6, createCourse), Command("createsection", 6, createSection),
            Command("assignacccourse", 2, assignAccCourse),
            Command("assignaccsection", 3, assignAccSection),
            Command("viewcourseassign", 1, viewCourseAssign)]




