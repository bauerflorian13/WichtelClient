from bcolors import bcolors
import sys

class Log(object):
    def header(self, msg):
        print(bcolors.OKBLUE + msg + bcolors.ENDC)

    def info(self, msg):
        print(bcolors.OKGREEN + msg + bcolors.ENDC)
    
    def fail(self, msg):
        print(bcolors.FAIL + msg + bcolors.ENDC, file=sys.stderr)