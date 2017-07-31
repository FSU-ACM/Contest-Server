# util.views.profile

from datetime import date,datetime

def verifyuserdetails(firstname, lastname, dob, major, advProg, ifstudent):
    error = ""
    dob_date = None
    wrong_dob_format = False
    #dob_date = datetime.strptime(dob,"%Y-%m-%d")
    #Checking date format
    try:
        dob_date = datetime.strptime(dob,"%Y-%m-%d")
    except ValueError as err:
        print(err)
        wrong_dob_format = True
    if dob_date > datetime(2017,01,01) or dob_date < datetime(1890,01,01):
        wrong_dob_format = True

    if not firstname:
        error += "Please enter a valid first name."

    if not lastname:
        error += "Please enter a valid last name.\n"

    if not dob or wrong_dob_format:
        error += "Please enter a valid date of birth. Format yyyy-mm-dd.\n"

    if not major and ifstudent:
        error += "Please enter a valid major.\n"

    if not advProg and ifstudent:
        error += "Please select a valid most advanced program.\n"

    return error
