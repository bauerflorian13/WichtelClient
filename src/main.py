#! /usr/bin/env python3

from user import User
import itertools
import random
from mail import Mail
from config import Config
import sys

def find_allowed_permutations(users):
    print("ALLOWED MATCHES: ")
    for user in users:
        others = [u for u in users if not user.is_forbidden(u)]
        print("{}: {}".format(user.name, [o.name for o in others]))

    # create all options
    perms = list(itertools.permutations(users))

    # filter
    allowed_perms = []
    for perm in perms:
        #print(perm)
        perm_allowed = True
        
        for user, match in zip(users, perm):
            if user.is_forbidden(match):
                perm_allowed = False
        
        if perm_allowed:
            allowed_perms.append(perm)
    
    print("ALLOWED PERMS")
    i = 1
    for perm in allowed_perms:
        print("Permutation {}".format(i))
        i += 1
        for user, match in zip(users, perm):
            print("{} -> {}".format(user.name, match.name))
    
    return allowed_perms

def main():
    conf = Config()
    users = []

    for name in ["u1", "u2", "u3"]:
        user = User(name, "example@example.org")
        user.forbid(user) # forbid matching to self
        users.append(user)

    users[1].forbid(users[2])
    
    allowed_perms = find_allowed_permutations(users)
    
    if len(allowed_perms) < 1:
        print("No allowed perms found.")
        sys.exit(1)

    rnd = random.randint(0, len(allowed_perms) - 1)

    chosen_perm = allowed_perms[rnd]

    print("CHOSEN PERM")
    for user, match in zip(users, chosen_perm):
        print("{} -> {}".format(user.name, match.name))
    
    if conf.mail_enabled:
        mail = Mail(conf)
        for user, match in zip(users, chosen_perm):
            mail.send_mail(user.email, conf.mail_subject, "Hallo {}, \r\ndein Wichtelpartner ist {}.\r\nViel Spaß,\r\ndein Wichtelmagic System\r\n".format(user.name, match.name))
        mail.quit()
        print("mails sent")

if __name__ == "__main__":
    main()