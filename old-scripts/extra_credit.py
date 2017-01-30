from app.models import *
import csv

if __name__ == '__main__':

    f1 = open("extra-credit.csv")
    lines = f1.readlines()

    with open("ec-output.csv", "wb") as f2:

        f2.write("First Name, Last Name, FSUID, # of Questions Solved\n")

        lines = [line.replace("\r\n", "") for line in lines]

        for line in lines:
            tokens = line.split(",")
            fsuid = tokens[0]
            s = Student.query.filter_by(fsuid=fsuid).first()
            if s is None:
                continue
            names = [s.first_name or "", s.last_name or ""]
            names = [str(s) for s in names]
            solved = len(tokens) - tokens.count("") - 1
            data = "{0},{1},{2},{3}\n".format(names[0], names[1], fsuid, solved)
            f2.write(data)
