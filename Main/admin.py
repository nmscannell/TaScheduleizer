from django.contrib import admin
from Main.models import Account, Course, AccountSection, Section
from AccountCourse.models import AccountCourse
# Register your models here.

admin.site.register(Account)
admin.site.register(Course)
admin.site.register(AccountCourse)
admin.site.register(AccountSection)
admin.site.register(Section)
