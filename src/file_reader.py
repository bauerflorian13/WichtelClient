from user import User
import sys
from log import Log

log = Log()

class FileReader(object):
    def __init__(self):
        pass
    
    def read(self, filename):
        usernames = []
        emails = []
        forbidden = []
        with open(filename, 'r', encoding='utf-8') as infile:
            for line in infile:
                line = line.strip()
                split = line.split(';')

                if (len(split) != 3):
                    log.fail("every line has to follow the format username;email;forbidden")
                    sys.exit(1)
                
                usernames.append(split[0])
                emails.append(split[1])
                forbidden.append(split[2])
        
        # create users
        users = {}
        for (name, email) in zip(usernames, emails):
            user = User(name, email)
            user.forbid(user) # forbid self
            users[name] = user
        
        # add forbidden to users
        for (name,forbidden) in zip(usernames, forbidden):
            user = users[name]

            split = forbidden.split(',')
            
            for fb in split:
                if fb != '':
                    try:
                        users[name].forbid(users[fb])
                    except KeyError as err:
                        log.fail("check input file: {} is an unknown username".format(err))
                        sys.exit(1)
        
        return users.values()