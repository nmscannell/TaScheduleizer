from Main.models import Account


class CurrentUser:

    def setCurrentUser(self, account, request):
        request.session["currentUser"] = account.userName

    def removeCurrentUser(self, request):
        request.session["currentUser"] = 0

    def getCurrentUser(self, request):
        account = request.session.get("currentUser", 0)
        try:
            CurrentUser = Account.objects.get(userName=account)
            return CurrentUser
        except Account.DoesNotExist:
            return 0

    def getCurrentUserTitle(self, request):

        currentUser = self.getCurrentUser(request)

        if currentUser is 0:
            return 0
        else:
            return currentUser.title
