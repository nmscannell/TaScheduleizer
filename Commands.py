from Main.models import Account

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


def getCommands():
    commandList = [Command("login", 2, login), Command("logout", 0, logout),
                   Command("createAccount", 5, createAccount), Command("deleteAccount", 1, deleteAccount),
                   Command("createCourse", 6, createCourse), Command("createSection", 6, createSection),
                   Command("assignAccCourse", 2, assignAccCourse),
                   Command("assignAccSection", 3, assignAccSection),
                   Command("viewCourseAssign", 1, viewCourseAssign)]
    return commandList
