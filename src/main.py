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

def generate_permutation(users):
    # init local variables
    log.header("START PAIR GENERATION")
    generated_pairs = gen_perms_recursive(users, users)

    if len(generated_pairs) == 0 and len(users) > 0:
        log.fail("There was no matching possible!")
        sys.exit(1)

    return generated_pairs

def gen_perms_recursive(unmatched_users, unmatched_partners):
    # check if there are more unmatched users
    if len(unmatched_users) == 0 and len(unmatched_partners) == 0:
        return []

    if len(unmatched_users) == 0 or len(unmatched_partners) == 0:
        log.fail("The number of unmatched users or partners is null but not both!")
        sys.exit(1)

    if len(unmatched_users) != len(unmatched_partners):
        log.fail("The number of unmatched users and partners is not equal!")
        sys.exit(1)


    # for random selection shuffle the user list before
    random.shuffle(unmatched_users)

    for current_user in unmatched_users:
        # remove forbidden partners
        possible_partners = [u for u in unmatched_partners]

        for forbidden in current_user.forbidden:
            if forbidden in possible_partners:
                possible_partners.remove(forbidden)

        if len(possible_partners) == 0:
            log.info("No matching possible for '{}' in this part of the tree.".format(current_user))
            continue

        # for double randomnes shuffle partner list as well:P
        random.shuffle(possible_partners)
        for current_partner in possible_partners:
            print("Current partner {}".format(current_partner.name))
            current_pair = (current_user, current_partner)

            if len(unmatched_users) == 1:
                log.info("Matched as first pair this pair: '{} -> {}'".format(current_user.name, current_partner.name))
                return [current_pair]

            else:
                new_unmatched_users = [u for u in unmatched_users if u != current_user]
                new_unmatched_partners = [u for u in unmatched_partners if u != current_partner]
                gen_pairs = gen_perms_recursive(new_unmatched_users, new_unmatched_partners)

                if len(gen_pairs) == 0:
                    continue

                else:
                    log.info("Matched as pair no. {} this pair: '{} -> {}'".format(len(gen_pairs), current_user.name, current_partner.name))
                    gen_pairs.insert(0, current_pair)
                    return gen_pairs


    # in case there was no possible matching return an empty []
    return []

def get_matching(list, user):
    return filter(lambda usr,match: usr == user, list)[0]

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
    perms_normal = generate_permutation(users_list)

    if len(perms_normal) < 1:
        log.fail("No allowed perms found ('Normales Wichteln').")
        sys.exit(1)

    # forbid the matches from "Normales Wichteln"
    for user,match in perms_normal:
        user.forbid(match)

    perms_schrott = generate_permutation(users_list)

    if len(perms_schrott) < 1:
        log.fail("No allowed perms found ('Schrott-Wichteln').")
        sys.exit(1)

    log.header("CHOSEN PERM Normal")
    for (paira,pairb) in perms_normal:
        log.info("{} -> {}".format(paira.name, pairb.name))

    log.header("CHOSEN PERM Schrott")
    for (paira,pairb) in perms_schrott:
        log.info("{} -> {}".format(paira.name, pairb.name))

    if conf.mail_enabled:
        mail = Mail(conf)
        for user in users_list:
            mail.send_mail(user.email, conf.mail_subject, "Hallo {}, \r\ndein normaler Wichtelpartner ist {}.\r\n "
                                                                  "Desweiteren ist dein Schrottwichtelpartner {}.\r\n"
                                                                  "Viel Spaß,\r\ndein Wichtelmagic System\r\n".format(user.name, get_matching(perms_normal, user), get_matching(perms_schrott, user)))
        mail.quit()
        log.info("mails sent")

if __name__ == "__main__":
    main()
