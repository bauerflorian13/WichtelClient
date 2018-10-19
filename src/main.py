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

    allowed_perms = generate_permutation(users_list)
    
    if len(allowed_perms) < 1:
        log.fail("No allowed perms found.")
        sys.exit(1)

#    rnd = random.randint(0, len(allowed_perms) - 1)

#    chosen_perm = allowed_perms[rnd]
    
    chosen_perm = allowed_perms

    log.header("CHOSEN PERM")
#    for user, match in zip(users, chosen_perm):
#        log.info("{} -> {}".format(user.name, match.name))
    for (paira,pairb) in chosen_perm:
        log.info("{} -> {}".format(paira.name, pairb.name))

    if conf.mail_enabled:
        mail = Mail(conf)
        for user, match in zip(users, chosen_perm):
            mail.send_mail(user.email, conf.mail_subject, "Hallo {}, \r\ndein Wichtelpartner ist {}.\r\nViel Spaß,\r\ndein Wichtelmagic System\r\n".format(user.name, match.name))
        mail.quit()
        log.info("mails sent")

if __name__ == "__main__":
    main()
