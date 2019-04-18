from django.shortcuts import render, redirect
from django.views import View
from UserInterface import UI
from Commands import login, displayAllCourseAssign
from CurrentUserHelper import CurrentUser
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


class adminPage(View):

    def get(self, request):
        CU = CurrentUser()
        currentuser = CU.getCurrentUser(request)

        if not currentuser:
            return render(request, 'errorPage.html', {"message": "Only admins may view this page"})
        return render(request, 'Accounts/AdminHome.html')


class supervisorPage(View):

    def get(self, request):
        return render(request, 'Accounts/SupervisorHome.html')


class instructorPage(View):

    def get(self, request):
        CU = CurrentUser()
        account = CU.getCurrentUser(request)
        return render(request, 'Accounts/InstructorHome.html', {"account": account})


class taPage(View):

    def get(self, request):
        CU = CurrentUser()
        account = CU.getCurrentUser(request)
        return render(request, 'Accounts/TaHome.html', {"account": account})


class createAccountView(View):

    def get(self, request):
        #accountList = list(Account.objects.all())
        return render(request, 'createAccount.html')

    def post(self, request):
        #self.CA = Account()
        userName = str(request.POST["username"])
        firstName = str(request.POST["firstname"])
        lastName = str(request.POST["lastname"])
        #email = str(request.POST["email"])
        #title = str(request.POST["title"])
        return render(request, 'createAccount.html')
        #command = [userName, title, email, firstName, lastName]

        #try:
            #message = Account.createAccountModels(self.CA, command)
            #return render(request, 'createAccount.html', {"message": message})
        #except Exception as e:
            #return render(request, 'createAccount.html', {"message": str(e)})


class courseAssignmentsList(View):

    def get(self, request):
        courses = displayAllCourseAssign()
        return render(request, 'courseAssignmentList.html', {"courseList": courses})


class deleteAccount(View):
    def get(self, request):
        return render(request, 'deleteAccount.html')
    def post(self, request):
       pass

class instructorCourse(View):
    def get(self, request):
        return render(request, 'assignInstructor.html')
    def post(self, request):
        pass
