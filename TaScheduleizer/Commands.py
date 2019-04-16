from Main.models import Account

class Command():

    def __init__(self, opcode, arguments, function):
        self.opcode = opcode
        self.arguments = arguments
        self.function = function


def login(self, userName, password):
    test = Account.objects.filter(currentUser=True)
    # Accessing the login page will automatically log out previous user. This shouldn't ever happen but ill leave it.
    if len(test) > 0:
        raise Exception("A user is already logged in")

    try:
        CurrentUser = Account.objects.get(userName=userName)
        if CurrentUser.password != password:
            raise Exception("Incorrect password")

    except Account.DoesNotExist:
        raise Exception("Account Not Found")

    CurrentUser.currentUser = True
    CurrentUser.save()
    return CurrentUser.title


def logout(self):
    pass


def createAccount(firstName, lastName, userName, email, title):
    pass


def deleteAccount(userName):
    pass


def createCourse(name, number, online, days, start, end):
    pass


def createSection(courseNumber, type, sectionNumber, days, start, end):
    pass


def assignAccCourse(userName, courseNumber):
    pass


def assignAccSection(userName, courseNumber, sectionNumber):
    pass


def viewCourseAssign(userName):
    pass


def getCommands(self):
    commandList = [Command("login", 2, login), Command("logout", 0, logout),
                   Command("createAccount", 5, createAccount), Command("deleteAccount", 1, deleteAccount),
                   Command("createCourse", 6, createCourse), Command("createSection", 6, createSection),
                   Command("assignAccCourse", 2, assignAccCourse),
                   Command("assignAccSection", 3, assignAccSection),
                   Command("viewCourseAssign", 1, viewCourseAssign)]
    return commandList
