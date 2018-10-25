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

def main():
    conf = Config()
    users = []

    fr = FileReader()
    users = fr.read('in.txt')

    log.header("USERS FROM FILE")
    for user in users:
        log.info("name: {} email: {} forbidden: {}".format(user.name, user.email, [u.name for u in user.forbidden]))

    perfect_matchings = bfs(users)

    if len(perfect_matchings) < 1:
        log.fail("No perfect matching found.")
        sys.exit(1)
    
    log.header("PERFECT MATCHINGS")
    log.info("Found {} perfect matchings.".format(len(perfect_matchings)))
    
    rnd = random.randint(0, len(perfect_matchings) - 1)

    chosen_perf_matching = perfect_matchings[rnd]

    log.header("CHOSEN PERFECT MATCHING")
    for user, match in chosen_perf_matching:
        log.info("{} -> {}".format(user.name, match.name))
    
    if conf.mail_enabled:
        mail = Mail(conf)
        for user, match in zip(users, chosen_perf_matching):
            mail.send_mail(user.email, conf.mail_subject, "Hallo {}, \r\ndein Wichtelpartner ist {}.\r\nViel Spaß,\r\ndein Wichtelmagic System\r\n".format(user.name, match.name))
        mail.quit()
        log.info("mails sent")

if __name__ == "__main__":
    main()