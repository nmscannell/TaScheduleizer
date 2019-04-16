

class Command():

    def __init__(self, opcode, arguments, function):
        self.opcode = opcode
        self.arguments = arguments
        self.function = function


    def login(self, userName, password):
        pass

    def logout(self):
        pass

    def createAccount(self, firstName, lastName, userName, email, title):
        pass

    def deleteAccount(self, userName):
        pass

    def createCourse(self, name, number, online, days, start, end):
        pass

    def createSection(self, courseNumber, type, sectionNumber, days, start, end):
        pass

    def assignAccCourse(self, userName, courseNumber):
        pass

    def assignAccSection(self, userName, courseNumber, sectionNumber):
        pass

    def viewCourseAssign(self, userName):
        pass


    def getCommands(self):
        commandList = [Command("login", 2, self.login), Command("logout", 0, self.logout),
                       Command("createAccount", 5, self.createAccount), Command("deleteAccount", 1, self.deleteAccount),
                       Command("createCourse", 6, self.createCourse), Command("createSection", 6, self.createSection),
                       Command("assignAccCourse", 2, self.assignAccCourse),
                       Command("assignAccSection", 3, self.assignAccSection),
                       Command("viewCourseAssign", 1, self.viewCourseAssign)]