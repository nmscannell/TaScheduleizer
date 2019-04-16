from django.shortcuts import render, redirect
from django.views import View
from UserInterface import UI
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
        return render(request, 'loginscreen.html', {"message": ""})

    def post(self, request):
        username = str(request.POST["username"])
        password = str(request.POST["password"])
        username = username.strip()

        try:
            check = LH.login(command)

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
