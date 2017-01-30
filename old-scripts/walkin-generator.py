from xkcdpass import xkcd_password as xp

# create a wordlist from the default wordfile
# use words between 5 and 8 letters long
wordfile = xp.locate_wordfile()
mywords = xp.generate_wordlist(wordfile=wordfile, min_length=5, max_length=8)

for i in range(100):
    userid = "walk-in-%i" % i
    password = xp.generate_xkcdpassword(mywords, numwords=3)
    password = password.title().replace(" ", "")
    print "{0},{1},{2}".format(userid, password, userid)
