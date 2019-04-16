from django.shortcuts import render
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
