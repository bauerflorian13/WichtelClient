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

# breadth-first-search
def bfs(users, all = False):
    return bfs_rec(users, users, [], all)

def bfs_rec(unmatched_left, unmatched_right, pairs, all):
    if len(unmatched_left) != len(unmatched_right):
        log.fail('unmachted_left and unmatched_right are not the same size. cannot find pefect matching')
        sys.exit(1)
    
    # recursion end
    if len(unmatched_left) == 0 and len(unmatched_right) == 0:
        return [pairs]
    
    new_unmatched_left = unmatched_left.copy()
    
    # get unmatched user
    user = new_unmatched_left.pop()

    # get allowed matches from unmatched_right
    allowed_matches = [u for u in unmatched_right if not user.is_forbidden(u)]

    # randomize if not generating all matchings
    if not all:
        random.shuffle(new_unmatched_left)
        random.shuffle(allowed_matches)

    # form all pairs and go on with recursion
    perfect_matchings = []
    for am in allowed_matches:
        new_pairs = pairs.copy()
        new_pairs.append((user, am))
        
        new_unmatched_right = unmatched_right.copy()
        new_unmatched_right.remove(am)

        perfect_matchings += bfs_rec(new_unmatched_left, new_unmatched_right, new_pairs, all)

        if (not all) and len(perfect_matchings) > 0:
            break

    return perfect_matchings

def get_matching(list, user):
    #return filter(lambda usr,match: usr == user, list)[0]
    return [match for (u, match) in list if u == user][0]

def main():
    conf = Config()
    users = []

    fr = FileReader()
    users = fr.read('in.txt')

    log.header("USERS FROM FILE")
    users_list = []
    for user in users:
        log.info("name: {} email: {} forbidden: {}".format(user.name, user.email, [u.name for u in user.forbidden]))
        users_list.append(user)

    # "Normales Wichteln" and "Schrottwichteln"
    perms_normal = bfs(users_list)

    if len(perms_normal) < 1:
        log.fail("No allowed perms found ('Normales Wichteln').")
        sys.exit(1)

    log.header("PERFECT MATCHINGS NORMAL")
    log.info("Found {} perfect matchings for normal wichteln.".format(len(perms_normal)))
    
    rnd = random.randint(0, len(perms_normal) - 1)

    perm_normal = perms_normal[rnd]


    # forbid the matches from "Normales Wichteln"
    for (user,match) in perm_normal:
        user.forbid(match)

    perms_schrott = bfs(users_list)

    if len(perms_schrott) < 1:
        log.fail("No allowed perms found ('Schrott-Wichteln').")
        sys.exit(1)
    
    log.header("PERFECT MATCHINGS SCHROTT")
    log.info("Found {} perfect matchings for schritt wichteln.".format(len(perms_schrott)))
    
    rnd = random.randint(0, len(perms_schrott) - 1)

    perm_schrott = perms_schrott[rnd]

    log.header("CHOSEN PERM Normal")
    for (paira,pairb) in perm_normal:
        log.info("{} -> {}".format(paira.name, pairb.name))

    log.header("CHOSEN PERM Schrott")
    for (paira,pairb) in perm_schrott:
        log.info("{} -> {}".format(paira.name, pairb.name))

    if conf.mail_enabled:
        mail = Mail(conf)
        for user in users_list:
            mail.send_mail(user.email, conf.mail_subject, "Hallo {}, \r\ndein normaler Wichtelpartner ist {}.\r\n "
                                                                  "Desweiteren ist dein Schrottwichtelpartner {}.\r\n"
                                                                  "Viel Spaß,\r\ndein Wichtelmagic System\r\n".format(user.name, get_matching(perm_normal, user).name, get_matching(perm_schrott, user).name))
        mail.quit()
        log.info("mails sent")

if __name__ == "__main__":
    main()
