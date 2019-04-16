from django.contrib import admin
from Main.models import Account, Course, AccountCourse, AccountSection, Section
# Register your models here.

admin.site.register(Account)
admin.site.register(Course)
admin.site.register(AccountCourse)
admin.site.register(AccountSection)
admin.site.register(Section)
