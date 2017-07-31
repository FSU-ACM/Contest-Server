from xkcdpass import xkcd_password as xp

from app.models import Account

# Wind up
wordfile = xp.locate_wordfile()
mywords = xp.generate_wordlist(wordfile=wordfile, min_length=3, max_length=5)

# Easy wrapper to gen password
def make_password():
    words = xp.generate_xkcdpassword(mywords, numwords=3).split()
    words = [s.capitalize() for s in words]
    return ''.join(words)

# This is what gets called
def reset_password(account):

    password = make_password()
    account.set_password(password)
    account.save()
    return password
