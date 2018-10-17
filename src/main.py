#! /usr/bin/env python3

from user import User
import itertools
import random
from mail import Mail
from config import Config
import sys
from file_reader import FileReader
from log import Log

log = Log()

def find_allowed_permutations(users):
    log.header("ALLOWED MATCHES: ")
    for user in users:
        others = [u for u in users if not user.is_forbidden(u)]
        log.info("{}: {}".format(user.name, [o.name for o in others]))

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
    
    log.header("ALLOWED PERMS")
    i = 1
    for perm in allowed_perms:
        log.info("Permutation {}".format(i))
        i += 1
        for user, match in zip(users, perm):
            log.info("{} -> {}".format(user.name, match.name))
    
    return allowed_perms

def generate_permutation(users):
    # init local variables
    generated_pairs = []
    current_unmatched_users = users
    current_unmatched_partners = users

    # match until there are no more unmatched user
    while len(current_unmatched_users) > 0 and len(current_unmatched_partners) > 0:
        if(len(current_unmatched_users) != len(current_unmatched_partners)):
            log.fail("The number of unmatched users and partners is not the same!")
            return

        rnd = random.randint(0, len(current_unmatched_users) - 1)
        current_user = current_umatched_users[rnd]
        current_user_possible_partners = current_unmatched_partners

        # remove all impossible partners
        for forbidden in current_user.forbidden:
            list(filter(lambda a: a != forbidden, current_user_possible_partners))
    
        # no possible partner
        if len(current_user_possible_partners):
            # do not fail here, but implement some clever code, which goes a step back and avoid this case in the future
            pass

        # generate pair 
        rnd = random.randint(0, len(current_user_possible_partners) - 1)
        current_partner = current_user_possible_partners[rnd]
        pair = (current_user, current_partner)
        generated_pairs = []

        # remove current user and current_partner
        list(filter(lambda a: a != current_user, current_unmatched_users))
        list(filter(lambda a: a != current_partner, current_possible_partners))

    return generated_pairs

def main():
    conf = Config()
    users = []

    fr = FileReader()
    users = fr.read('in.txt')

    log.header("USERS FROM FILE")
    for user in users:
        log.info("name: {} email: {} forbidden: {}".format(user.name, user.email, [u.name for u in user.forbidden]))

    allowed_perms = generate_permutation(users)
    
    if len(allowed_perms) < 1:
        log.fail("No allowed perms found.")
        sys.exit(1)

#    rnd = random.randint(0, len(allowed_perms) - 1)

#    chosen_perm = allowed_perms[rnd]
    
    chosen_perm = allowed_perms

    log.header("CHOSEN PERM")
    for user, match in zip(users, chosen_perm):
        log.info("{} -> {}".format(user.name, match.name))
    
    if conf.mail_enabled:
        mail = Mail(conf)
        for user, match in zip(users, chosen_perm):
            mail.send_mail(user.email, conf.mail_subject, "Hallo {}, \r\ndein Wichtelpartner ist {}.\r\nViel Spaß,\r\ndein Wichtelmagic System\r\n".format(user.name, match.name))
        mail.quit()
        log.info("mails sent")

if __name__ == "__main__":
    main()
