from django.shortcuts import render, redirect
from django.views import View
from UserInterface import UI
from CurrentUserHelper import CurrentUser
from Main.models import Account, Course
from Commands import assignAccCourse


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
        base = CU.getTemplate(request)
        return render(request, 'assignInstructor.html', {"instList": instructorList, "courseList": courseList, "base": base})

    def post(self, request):
        CU = CurrentUser()
        username = str(request.POST.get("username"))
        course = str(request.POST.get("course"))
        message = assignAccCourse(username, course)
        base = CU.getTemplate(request)
        return render(request, 'assignInstructor.html', {"message": message, "base": base})


class taCourse(View):
    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        if currentusertitle != 4:
            return render(request, 'errorPage.html', {"message": "You do not have permission to view this page"})
        taList = Account.objects.filter(title=1)
        courseList = Course.objects.all()
        base = CU.getTemplate(request)
        return render(request, 'assignTACourse.html', {"taList": taList, "courseList": courseList, "base": base})

    def post(self, request):
        CU = CurrentUser()
        username = str(request.POST["username"])
        course = str(request.POST["course"])
        message = assignAccCourse(username, course)
        base = CU.getTemplate(request)
        return render(request, 'assignTACourse.html', {"message": message, "base": base})
