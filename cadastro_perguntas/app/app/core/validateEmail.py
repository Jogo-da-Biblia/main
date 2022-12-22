import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def validateEmail(email):
    if len(email) > 6:
        if re.fullmatch(regex, email) != None:
            return True
    return False