def check_alpha(s):
    str = '''0123456789!@#$%^'&*()-+?_=,<>/"'''
    for i in s:
        if i in str:
            return False
    else:
        return True

def check_pass(s):
    special_characters = r"!@#$%^&*()-+?_=,<>/"""
    upper = False
    lower = False
    number = False
    special = False
    if len(s) > 6:
        for i in s:
            if i.isupper():
                upper = True
            if i.islower():
                lower = True
            if i.isdigit():
                number = True
            if i in special_characters:
                special = True
    if upper == True and lower == True and number == True and special == True:
        return True
    else:
        return False
