from app.models import Account, Course


def set_courses(account, course_list):
    """Sets a user's extra credit courses to those passed in 'courses'.
    
    :courses: must be a list of primary keys to Course objects.

    """
    courses = get_reference_list(course_list)

    # Reset course list
    account.courses = []

    if courses and len(courses) > 0:
        for c in courses:
            account.courses.append(c)

def get_reference_list(course_list):
    """Returns a list of references to Course objects.

    :course_list: list of primary keys to Course objects.
    """
    
    if course_list:
        return [Course.objects.get(pk=c) for c in course_list]
    
    return []

def get_choices():
    """Returns list of tuples representing all Courses available.

    """

    return [(c.id, str(c)) for c in Course.objects.order_by('name', 'professor_name')]

def get_account_courses(account):
    """Returns list of id's representing the Courses of a user.

    :account: user to get courses of.
    """

    if account.courses:
        return [c.id for c in account.courses]

    return []
