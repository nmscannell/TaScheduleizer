from django.test import TestCase
from Main.models import Account
import Commands
from django.test import Client


class Test_editPubInfo(TestCase):

    def setUp(self):

        self.c = Client()

        self.startdefault = Account._meta.get_field('officeHoursStart').get_default()
        self.enddefault = Account._meta.get_field('officeHoursEnd').get_default()
        self.daysdefault = Account._meta.get_field('officeDays').get_default()

        self.j = Account.objects.create(userName="janewayk123", firstName="Kathryn", lastName="Janeway", password="123456",
                               email="janewayk@uwm.edu", title=2, homePhone="555-555-5555",
                               address="14 Voyager Drive", city="Delta", state="Quadrant", zipCode="00000",
                               officeNumber="456", officePhone="555-555-5555", officeDays="TR",
                               officeHoursStart="1300", officeHoursEnd="1400", currentUser=False)


        self.janeway = {
            'firstName': self.j.firstName,
            'lastName': self.j.lastName,
            'email': self.j.email,
            'password': self.j.password,
            'homephone': self.j.homePhone,
            'address': self.j.address,
            'city': self.j.city,
            'state': self.j.state,
            'zipcode': self.j.zipCode,
            'officenumber': self.j.officeNumber,
            'officephone': self.j.officePhone,
            'officedays': self.j.officeDays,
            'officestart': self.j.officeHoursStart,
            'officeend': self.j.officeHoursEnd }

        Account.objects.create(userName="picard304", firstName="Jean Luc", lastName="Picard", password="90456",
                               email="picardj@uwm.edu", title=1, address="87 Enterprise Avenue",
                               city="Alpha", state="Quadrant", zipCode="11111", officeNumber="54",
                               officePhone="777-777-7777", officeDays="W", officeHoursStart="0900",
                               officeHoursEnd="1000", homePhone="444-444-4444", currentUser=False)

        Account.objects.create(userName="kirkj22", firstName="James", lastName="Kirk", password="678543",
                               email="kirkj22@uwm.edu", title=4, address="789 Enterprise Avenue",
                               city="Alpha", state="Quadrant", zipCode="89765", officeNumber="987",
                               officePhone="897-654-398", officeDays="MW", officeHoursStart="1500",
                               officeHoursEnd="1600", homePhone="222-222-2222", currentUser=False)

    def test_change_firstName_success(self):
        self.janeway["firstName"] = "Julie"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.firstName, "Julie")
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.password, "123456")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.address, "14 Voyager Drive")
        self.assertEqual(self.j.city, "Delta")
        self.assertEqual(self.j.state, "Quadrant")
        self.assertEqual(self.j.zipCode, "00000")
        self.assertEqual(self.j.officeNumber, "456")
        self.assertEqual(self.j.officePhone, "555-555-5555")
        self.assertEqual(self.j.officeDays, "TR")
        self.assertEqual(self.j.officeHoursStart, "1300")
        self.assertEqual(self.j.officeHoursEnd, "1400")


    def test_change_lastName_success(self):
        self.janeway["lastName"] = "Brooks"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.lastName, "Brooks")
        self.assertEqual(self.j.password, "123456")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.address, "14 Voyager Drive")
        self.assertEqual(self.j.city, "Delta")
        self.assertEqual(self.j.state, "Quadrant")
        self.assertEqual(self.j.zipCode, "00000")
        self.assertEqual(self.j.officeNumber, "456")
        self.assertEqual(self.j.officePhone, "555-555-5555")
        self.assertEqual(self.j.officeDays, "TR")
        self.assertEqual(self.j.officeHoursStart, "1300")
        self.assertEqual(self.j.officeHoursEnd, "1400")

    def test_change_email_success(self):
        self.janeway["email"] = "jane@uwm.edu"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.email, "jane@uwm.edu")
        self.assertEqual(self.j.password, "123456")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.address, "14 Voyager Drive")
        self.assertEqual(self.j.city, "Delta")
        self.assertEqual(self.j.state, "Quadrant")
        self.assertEqual(self.j.zipCode, "00000")
        self.assertEqual(self.j.officeNumber, "456")
        self.assertEqual(self.j.officePhone, "555-555-5555")
        self.assertEqual(self.j.officeDays, "TR")
        self.assertEqual(self.j.officeHoursStart, "1300")
        self.assertEqual(self.j.officeHoursEnd, "1400")

    def test_change_password_success(self):
        self.janeway["password"] = "voyager"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.password, "voyager")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.address, "14 Voyager Drive")
        self.assertEqual(self.j.city, "Delta")
        self.assertEqual(self.j.state, "Quadrant")
        self.assertEqual(self.j.zipCode, "00000")
        self.assertEqual(self.j.officeNumber, "456")
        self.assertEqual(self.j.officePhone, "555-555-5555")
        self.assertEqual(self.j.officeDays, "TR")
        self.assertEqual(self.j.officeHoursStart, "1300")
        self.assertEqual(self.j.officeHoursEnd, "1400")

    def test_change_homephone_success(self):
        self.janeway['homephone'] = "333-333-3333"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.password, "123456")
        self.assertEqual(self.j.homePhone, "333-333-3333")
        self.assertEqual(self.j.address, "14 Voyager Drive")
        self.assertEqual(self.j.city, "Delta")
        self.assertEqual(self.j.state, "Quadrant")
        self.assertEqual(self.j.zipCode, "00000")
        self.assertEqual(self.j.officeNumber, "456")
        self.assertEqual(self.j.officePhone, "555-555-5555")
        self.assertEqual(self.j.officeDays, "TR")
        self.assertEqual(self.j.officeHoursStart, "1300")
        self.assertEqual(self.j.officeHoursEnd, "1400")

    def test_change_address_success(self):
        self.janeway['address'] = "15 Voyager Drive"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.password, "123456")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.address, "15 Voyager Drive")
        self.assertEqual(self.j.city, "Delta")
        self.assertEqual(self.j.state, "Quadrant")
        self.assertEqual(self.j.zipCode, "00000")
        self.assertEqual(self.j.officeNumber, "456")
        self.assertEqual(self.j.officePhone, "555-555-5555")
        self.assertEqual(self.j.officeDays, "TR")
        self.assertEqual(self.j.officeHoursStart, "1300")
        self.assertEqual(self.j.officeHoursEnd, "1400")

    def test_change_city_success(self):
        self.janeway['city'] = "Chicago"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.password, "123456")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.address, "14 Voyager Drive")
        self.assertEqual(self.j.city, "Chicago")
        self.assertEqual(self.j.state, "Quadrant")
        self.assertEqual(self.j.zipCode, "00000")
        self.assertEqual(self.j.officeNumber, "456")
        self.assertEqual(self.j.officePhone, "555-555-5555")
        self.assertEqual(self.j.officeDays, "TR")
        self.assertEqual(self.j.officeHoursStart, "1300")
        self.assertEqual(self.j.officeHoursEnd, "1400")

    def test_change_state_success(self):
        self.janeway['state'] = "Wisconsin"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.password, "123456")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.address, "14 Voyager Drive")
        self.assertEqual(self.j.city, "Delta")
        self.assertEqual(self.j.state, "Wisconsin")
        self.assertEqual(self.j.zipCode, "00000")
        self.assertEqual(self.j.officeNumber, "456")
        self.assertEqual(self.j.officePhone, "555-555-5555")
        self.assertEqual(self.j.officeDays, "TR")
        self.assertEqual(self.j.officeHoursStart, "1300")
        self.assertEqual(self.j.officeHoursEnd, "1400")

    def test_change_zipcode_success(self):
        self.janeway['zipcode'] = "56748"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.password, "123456")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.address, "14 Voyager Drive")
        self.assertEqual(self.j.city, "Delta")
        self.assertEqual(self.j.state, "Quadrant")
        self.assertEqual(self.j.zipCode, "56748")
        self.assertEqual(self.j.officeNumber, "456")
        self.assertEqual(self.j.officePhone, "555-555-5555")
        self.assertEqual(self.j.officeDays, "TR")
        self.assertEqual(self.j.officeHoursStart, "1300")
        self.assertEqual(self.j.officeHoursEnd, "1400")

    def test_change_officePhone_success(self):
        self.janeway['officephone'] = "222-222-2222"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.password, "123456")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.address, "14 Voyager Drive")
        self.assertEqual(self.j.city, "Delta")
        self.assertEqual(self.j.state, "Quadrant")
        self.assertEqual(self.j.zipCode, "00000")
        self.assertEqual(self.j.officeNumber, "456")
        self.assertEqual(self.j.officePhone, "222-222-2222")
        self.assertEqual(self.j.officeDays, "TR")
        self.assertEqual(self.j.officeHoursStart, "1300")
        self.assertEqual(self.j.officeHoursEnd, "1400")

    def test_change_officeNum_success(self):
        self.janeway['officenumber'] = "123"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.password, "123456")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.address, "14 Voyager Drive")
        self.assertEqual(self.j.city, "Delta")
        self.assertEqual(self.j.state, "Quadrant")
        self.assertEqual(self.j.zipCode, "00000")
        self.assertEqual(self.j.officeNumber, "123")
        self.assertEqual(self.j.officePhone, "555-555-5555")
        self.assertEqual(self.j.officeDays, "TR")
        self.assertEqual(self.j.officeHoursStart, "1300")
        self.assertEqual(self.j.officeHoursEnd, "1400")

    def test_change_officedays_success(self):
        self.janeway['officedays'] = "MW"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.password, "123456")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.address, "14 Voyager Drive")
        self.assertEqual(self.j.city, "Delta")
        self.assertEqual(self.j.state, "Quadrant")
        self.assertEqual(self.j.zipCode, "00000")
        self.assertEqual(self.j.officeNumber, "456")
        self.assertEqual(self.j.officePhone, "555-555-5555")
        self.assertEqual(self.j.officeDays, "MW")
        self.assertEqual(self.j.officeHoursStart, "1300")
        self.assertEqual(self.j.officeHoursEnd, "1400")

    def test_change_officeStart_success(self):
        self.janeway['officestart'] = "1200"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.password, "123456")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.address, "14 Voyager Drive")
        self.assertEqual(self.j.city, "Delta")
        self.assertEqual(self.j.state, "Quadrant")
        self.assertEqual(self.j.zipCode, "00000")
        self.assertEqual(self.j.officeNumber, "456")
        self.assertEqual(self.j.officePhone, "555-555-5555")
        self.assertEqual(self.j.officeDays, "TR")
        self.assertEqual(self.j.officeHoursStart, "1200")
        self.assertEqual(self.j.officeHoursEnd, "1400")

    def test_change_officeend_success(self):
        self.janeway['officeend'] = "1500"
        Commands.editPubInfo(self.j, self.janeway)
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.password, "123456")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.address, "14 Voyager Drive")
        self.assertEqual(self.j.city, "Delta")
        self.assertEqual(self.j.state, "Quadrant")
        self.assertEqual(self.j.zipCode, "00000")
        self.assertEqual(self.j.officeNumber, "456")
        self.assertEqual(self.j.officePhone, "555-555-5555")
        self.assertEqual(self.j.officeDays, "TR")
        self.assertEqual(self.j.officeHoursStart, "1300")
        self.assertEqual(self.j.officeHoursEnd, "1500")

    def test_change_email_invalid(self):
        self.janeway['email'] = "jane@hotmail.com"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: The email address you have entered "
                                                                     "is not valid. Please make sure you are using "
                                                                     "a uwm email address in the correct format.")

    def test_change_firstname_invalid(self):
        self.janeway['firstName'] = "jane2"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: First Name can only contain letters")

    def test_change_lastname_invalid(self):
        self.janeway['lastName'] = "jane2"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: Last name can only contain letters")

    def test_change_city_invalid(self):
        self.janeway['city'] = "456"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: City must contain only letters")

    def test_change_state_invalid(self):
        self.janeway['state'] = "456"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: State must contain only letters")

    def test_change_homephone_invalid(self):
        self.janeway['homephone'] = "abc-678-9807"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: Home Phone can only contain numbers")

    def test_change_officedays_invalid(self):
        self.janeway['officedays'] = "ABCTR"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway),
                         "Errors: Invalid days of the week, please enter days in the format: MWTRF or NN for online")

    def test_change_officephone_invalid(self):
        self.janeway['officephone'] = "abc-678-9807"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: Office Phone can only contain numbers")

    def test_change_zip_invalid(self):
        self.janeway['zipcode'] = "t89r3"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: ZipCode my be only numeric")

    def test_change_officeNum_invalid(self):
        self.janeway['officenumber'] = "y89"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: Office Number must be numeric")

    def test_change_times_invalid(self):
        self.janeway['officestart'] = "9999"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: Invalid start time, please use a "
                                                                     "4 digit military time representation")
        self.assertEqual(self.j.officeHoursStart, self.startdefault)
        self.assertEqual(self.j.officeHoursEnd, self.enddefault)

    def test_change_times_invalid2(self):
        self.janeway['officeend'] = "9999"
        #self.janeway['officestart'] = "1300"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: Invalid end time, please use a "
                                                                     "4 digit military time representation")
        self.assertEqual(self.j.officeHoursStart, self.startdefault)
        self.assertEqual(self.j.officeHoursEnd, self.enddefault)

    def test_change_times_start_nofinish(self):
        self.janeway['officestart'] = "1300"
        self.janeway['officeend'] = str(self.enddefault)
        self.janeway['officedays'] = "MW"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway),
                         "Errors: You must enter both a start and end time for office hours")
        self.assertEqual(self.j.officeHoursStart, self.startdefault)
        self.assertEqual(self.j.officeHoursEnd, self.enddefault)

    def test_change_times_finish_nostart(self):
        self.janeway['officestart'] = str(self.startdefault)
        self.janeway['officeday'] = "MW"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway),
                         "Errors: You must enter both a start and end time for office hours")
        self.assertEqual(self.j.officeHoursStart, self.startdefault)
        self.assertEqual(self.j.officeHoursEnd, self.enddefault)

    def test_times_no_day(self):
        self.janeway['officestart'] = "1300"
        self.janeway['officeend'] = "1400"
        self.janeway['officedays'] = str(self.daysdefault)
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway),
                         "Errors: You must enter office days if you enter office hours")
        self.assertEqual(self.j.officeHoursStart, self.startdefault)
        self.assertEqual(self.j.officeHoursEnd, self.enddefault)
        self.assertEqual(self.j.officeDays, self.daysdefault)

    def test_days_no_times(self):
        self.janeway['officestart'] = str(self.startdefault)
        self.janeway['officeend'] = str(self.enddefault)
        self.janeway['officedays'] = 'MW'
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway),
                         "Errors: You must enter office hours if you enter office days")
        self.assertEqual(self.j.officeHoursStart, self.startdefault)
        self.assertEqual(self.j.officeHoursEnd, self.enddefault)
        self.assertEqual(self.j.officeDays, self.daysdefault)

    def test_incorrect_FN_correct_LN(self):
        self.janeway['firstName'] = "12"
        self.janeway['lastName'] = "Brooks"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: First Name can only contain letters")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.lastName, "Brooks")

    def test_incorrect_FN_LN_correct_email(self):
        self.janeway['firstName'] = "12"
        self.janeway['lastName'] = "14"
        self.janeway['email'] = "jk45@uwm.edu"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: First Name can only contain letters, "
                                                                     "Last name can only contain letters")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.email, "jk45@uwm.edu")

    def test_incorrect_FN_LN_email_correct_homephone(self):
        self.janeway['firstName'] = "12"
        self.janeway['lastName'] = "14"
        self.janeway['email'] = "jk45@hotmail.edu"
        self.janeway['homephone'] = "222-222-2222"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: First Name can only contain letters, "
                                                                     "Last name can only contain letters, The email "
                                                                     "address you have entered is not valid. Please "
                                                                     "make sure you are using a uwm email address in "
                                                                     "the correct format.")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.homePhone, "222-222-2222")

    def test_incorect_FN_LN_email_HP_correct_city(self):
        self.janeway['firstName'] = "12"
        self.janeway['lastName'] = "14"
        self.janeway['email'] = "jk45@hotmail.edu"
        self.janeway['homephone'] = "222-2u2-2222"
        self.janeway['city'] = "Racine"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: First Name can only contain letters, "
                                                                     "Last name can only contain letters, The email "
                                                                     "address you have entered is not valid. Please "
                                                                     "make sure you are using a uwm email address in "
                                                                     "the correct format., Home Phone can only contain "
                                                                     "numbers")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.lastName, "Janeway")
        self.assertEqual(self.j.email, "janewayk@uwm.edu")
        self.assertEqual(self.j.homePhone, "555-555-5555")
        self.assertEqual(self.j.city, "Racine")

    def test_days_noHours_correct_FN(self):
        self.janeway['firstName'] = "Jamie"
        self.janeway['officedays'] = "MW"
        self.janeway['officestart'] = str(self.startdefault)
        self.janeway['officeend'] = str(self.enddefault)
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: You must enter office hours "
                                                                     "if you enter office days")
        self.assertEqual(self.j.firstName, "Jamie")
        self.assertEqual(self.j.officeDays, self.daysdefault)
        self.assertEqual(self.j.officeHoursEnd, self.enddefault)
        self.assertEqual(self.j.officeHoursStart, self.startdefault)

    def test_incorrect_FN_correct_Zipcode(self):
        self.janeway['firstName'] = "13ab"
        self.janeway['zipcode'] = "99999"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway), "Errors: First Name can only contain letters")
        self.assertEqual(self.j.firstName, "Kathryn")
        self.assertEqual(self.j.zipCode, "99999")

    def test_times_out_of_order(self):
        self.janeway['officestart'] = "1200"
        self.janeway['officeend'] = "1100"
        self.assertEqual(Commands.editPubInfo(self.j, self.janeway),
                         "Errors: Office hours end time must be after office hours start time")
        self.assertEqual(self.j.officeHoursStart, self.startdefault)
        self.assertEqual(self.j.officeHoursEnd, self.enddefault)