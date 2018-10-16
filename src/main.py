#! /usr/bin/env python3

from user import User
import itertools

def findMatches(users):
    print("ALLOWED MATCHES: ")
    for user in users:
        others = [u for u in users if not user.isForbidden(u)]
        print("{}: {}".format(user.getName(), [o.getName() for o in others]))

    # create all options
    perms = list(itertools.permutations(users))

    # filter
    allowedPerms = []
    for perm in perms:
        #print(perm)
        permAllowed = True
        
        for user, match in zip(users, perm):
            # print("user {} -> match {}".format(user.getName(), match.getName()))
            if user.isForbidden(match):
                permAllowed = False
        
        if permAllowed:
            allowedPerms.append(perm)

    print("ALLOWED PERMS")
    i = 1
    for perm in allowedPerms:
        print("Permutation {}".format(i))
        i += 1
        for user, match in zip(users, perm):
            print("{} -> {}".format(user.getName(), match.getName()))

def main():
    users = []
    for name in ["u1", "u2", "u3"]:
        user = User(name)
        user.forbid(user)
        users.append(user)


    users[1].forbid(users[2])
    
    findMatches(users)

if __name__ == "__main__":
    main()