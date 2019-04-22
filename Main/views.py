from django.shortcuts import render, redirect
from django.views import View
from UserInterface import UI
from Commands import login, logout, displayAllCourseAssign, deleteAccountCom, createAccount, getPrivateDataList, getPublicDataList, editPubInfo, assignAccCourse
from CurrentUserHelper import CurrentUser
from Main.models import Account, Course, Section, AccountCourse, AccountSection

# Create your views here.


class commandLine(View):
    def get(self, request):
        return render(request, 'commandline.html')

    def post(self, request):
        yourInstance = UI()
        commandInput = request.POST["command"]
        if commandInput:
            response = yourInstance.command(commandInput)
        else:
            response = ""
        return render(request, 'commandline.html', {"message": response})


def redirect_login(request):
    return redirect('/login/')


class loginPage(View):

    def get(self, request):
        CU = CurrentUser()
        CU.removeCurrentUser(request)
        return render(request, 'loginscreen.html', {"message": ""})

    def post(self, request):
        CU = CurrentUser()
        username = str(request.POST["username"])
        password = str(request.POST["password"])

        try:
            currentUser = login(username, password)
            CU.setCurrentUser(currentUser, request)

            check = CU.getCurrentUserTitle(request)

            if check == 1:
                return redirect('/ta/')
            if check == 2:
                return redirect('/instructor/')
            if check == 3:
                return redirect('/administrator/')
            if check == 4:
                return redirect('/supervisor/')

        except Exception as e:
            return render(request, 'loginscreen.html', {"message": str(e)})


class logoutView(View):
    def get(self, request):
        CU = CurrentUser()
        message = logout(CU.getCurrentUser(request))
        CU.removeCurrentUser(request)
        return render(request, "logout.html", {"message": message})


class adminPage(View):

    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)

        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle != 3:
            return render(request, 'errorPage.html', {"message": "Only admins may view this page"})
        return render(request, 'Accounts/AdminHome.html')


class supervisorPage(View):

    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)

        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle != 4:
            return render(request, 'errorPage.html', {"message": "Only supervisors may view this page"})
        return render(request, 'Accounts/SupervisorHome.html')


class instructorPage(View):

    def get(self, request):
        CU = CurrentUser()
        account = CU.getCurrentUser(request)
        currentusertitle = CU.getCurrentUserTitle(request)

        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle != 2:
            return render(request, 'errorPage.html', {"message": "Only instructors may view this page"})
        return render(request, 'Accounts/InstructorHome.html', {"account": account})


class taPage(View):
    def get(self, request):
        CU = CurrentUser()
        account = CU.getCurrentUser(request)
        currentusertitle = CU.getCurrentUserTitle(request)

        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle != 1:
            return render(request, 'errorPage.html', {"message": "Only Teaching Assistants may view this page"})
        return render(request, 'Accounts/TaHome.html', {"account": account})


class createAccountView(View):

    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        user = CU.getCurrentUser(request)

        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle < 3:
            return render(request, 'errorPage.html', {"message": "You do not have permission to View this page"})

        return render(request, 'createAccount.html', {"i": user})

    def post(self, request):
        CU = CurrentUser()
        user = CU.getCurrentUser(request)
        userName = str(request.POST["username"])
        firstName = str(request.POST["firstname"])
        lastName = str(request.POST["lastname"])
        email = str(request.POST["email"])
        title = str(request.POST["title"])
        #try:
        message = createAccount(userName=userName, firstName=firstName,
                                lastName=lastName, email=email, title=title)

        return render(request, 'createAccount.html', {"message": message, "i": user})
        #except Exception as e:
         #   return render(request, 'createAccount.html', {"message": str(e)})


class courseAssignmentsList(View):

    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        courses = displayAllCourseAssign()
        return render(request, 'courseAssignmentList.html', {"courseList": courses})


class deleteAccount(View):
    def get(self, request):
        CU = CurrentUser()
        user = CU.getCurrentUser(request)
        instructorList = Account.objects.filter(title=2)
        taList = Account.objects.filter(title='1')
        staffList = instructorList | taList
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle < 3:
            return render(request, 'errorPage.html', {"message": "You do not have permission to view this page"})
        return render(request, 'deleteAccount.html', {"stafflist": staffList, "i":user})

    def post(self, request):
        CU = CurrentUser()
        user = CU.getCurrentUser(request)
        username = str(request.POST["username"])
        message = deleteAccountCom(username)
        instructorList = Account.objects.filter(title=2)
        taList = Account.objects.filter(title='1')
        staffList = instructorList | taList

        return render(request, 'deleteAccount.html', {"message": message, "stafflist": staffList, "i":user})


class instructorCourse(View):
    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle != 4:
            return render(request, 'errorPage.html', {"message": "You do not have permission to view this page"})
        instructorList = Account.objects.filter(title=2)
        courseList = Course.objects.all()
        return render(request, 'assignInstructor.html', {"instList": instructorList, "courseList": courseList})

    def post(self, request):
        username = str(request.POST["username"])
        course = str(request.POST["course"])
        num = Course.objects.get(name=course).number
        message = assignAccCourse(userName=username, courseNumber=num)
        return render(request, 'assignInstructor.html', {"message": message})


class taCourse(View):
    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        if currentusertitle != 4:
            return render(request, 'errorPage.html', {"message": "You do not have permission to view this page"})
        taList = Account.objects.filter(title=1)
        courseList = Course.objects.all()
        return render(request, 'assignTACourse.html', {"taList": taList, "courseList": courseList})

    def post(self, request):
        username = str(request.POST["username"])
        course = str(request.POST["course"])
        num = Course.objects.get(name=course).number
        message = assignAccCourse(userName=username, courseNumber=num)
        return render(request, 'assignTACourse.html', {"message": message})

"""  

This one will be a bit challenging. Supervisor can assign any TA for any course to a certain section. Instructors can
only assign TAs for courses they are assigned to. Need to select a course to be able to choose a TA and section.


class taSection(View):
    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        if currentusertitle != 4 or currentusertitle != 2:
            return render(request, 'errorPage.html', {"message": "You do not have permission to view this page"})
        courseList = []
        if currentusertitle == 4:
            courseList = Course.objects.all()
        else:
            courseAssigns = AccountCourse.objects.filter(Account=CU.getCurrentUser(request))
            for a in courseAssigns:
                courseList.append(str(a.Course))

        return render(request, 'assignTASection.html', {"courseList": courseList})

    def post(self, request):
        course = str(request.POST["course"])
        

    def post(self, request):
        username = str(request.POST["username"])
        account = Account.objects.get(userName=username)
        courseAssigns = AccountCourse.objects.filter(Account=account)
        courseList = []
        for a in courseAssigns:
            courseList.append(a.Course.name)
        return render(request, 'assignTASection.html', {"courseList": courseList})


        section = str(request.POST["section"])
        num = Section.objects.get(name=section).number
        message = assignAccCourse(userName=username, courseNumber=num)
        return render(request, 'assignTASection.html', {"message": message})
 """

class directoryView(View):

    def get(self, request):
        CU = CurrentUser()
        title = CU.getCurrentUserTitle(request)

        if title == 0:
            return render(request, 'errorPage.html', {"message": "You Must log in to View this page"})
        if title == 1 or title == 2:
            directory = getPublicDataList()
        else:
            directory = getPrivateDataList()

        return render(request, 'Directory.html', {"directory": directory})


class editPubInfoView(View):

    def get(self, request):
        CU = CurrentUser()
        user = CU.getCurrentUser(request)
        return render(request, 'editPubInfo.html', {'i': user})

    def post(self, request):
        dict = {
            'firstName': str(request.POST.get("firstname")),
            'lastName': str(request.POST.get('lastname')),
            'email': str(request.POST.get('email')),
            'password': str(request.POST.get('password')),
            'homephone': str(request.POST.get("homephone")),
            'address': str(request.POST.get('address')),
            'city': str(request.POST.get('city')),
            'state': str(request.POST.get('state')),
            'zipcode': str(request.POST.get('zipcode')),
            'officenumber': str(request.POST.get('officenumber')),
            'officephone': str(request.POST.get('officephone')),
            'officedays': str(request.POST.get('officedays')),
            'officestart': str(request.POST.get('officestart')),
            'officeend': str(request.POST.get('officeend'))}
        CU = CurrentUser()
        user = CU.getCurrentUser(request)
        message = editPubInfo(user, dict)
        info = makeUserDictionary(user)
        return render(request, 'editPubInfo_success.html', {"message": message, "i": user, "info": info})


def makeUserDictionary(user):
    dict = {
        'First Name': user.firstName,
        'Last Name': user.lastName,
        'Email': user.email,
        'Password': user.password,
        'Home phone': user.homePhone,
        'Address': user.address,
        'City': user.city,
        'State': user.state,
        'Zipcode': user.zipCode,
        'Office number': user.officeNumber,
        'Office phone': user.officePhone,
        'Office days': user.officeDays,
        'Office hours start': user.officeHoursStart,
        'Office hours end': user.officeHoursEnd }
    return dict