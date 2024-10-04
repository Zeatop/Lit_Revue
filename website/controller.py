from django.contrib.auth import authenticate


# Authentifiction
user = authenticate(username="john", password="secret")
if user is not None:
    print('User authenticated')
    ...
else:
    print('User non authenticated')
    ...