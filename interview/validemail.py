# find email match using regex  python


import re


def valid_email(email):
    if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return True
    else:
        return False


# print(valid_email("1231q43q4fedsfdeepakgmail.com"))


if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", "deepasdcvsd2332@kgmail.com"):
    print(True)
else:
    print(False)
