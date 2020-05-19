'''
Author: Julian Levi Hernandez
'''

import argparse
from os import path, listdir, getcwd
import kennel as kn


class Datadog:
    def __init__(self):
        return None

    '''
    Name: getArgs
    Syntax: python3 KennelApi -c get_dashboard
    Required endpoint command must have a conf/get_dashboard.conf file.
    '''

    def getArgs(self):
        # Get cli input
        parser = argparse.ArgumentParser(description='Process DataDog API calls with KennelApi.')
        parser.add_argument('-c', '--call', type=str, help='name of config file that calls the API action')
        args = parser.parse_args()
        cmd = args.call
        argument = cmd
        return argument

    '''
    Name: execapi
    assembles the current working directory + endpoint command + .conf 
    '''

    def execApi(self):
        argument = self.getArgs()
        # pass config file information
        cnffile = 'config/' + self.getArgs() + '.conf'
        if path.exists(cnffile):
            cl = kn.Kennel(cnffile)
            fun = cl.commands[argument]()
        else:
            print(cnffile, " does not exist, please create it!")
            print(listdir(getcwd()))
        return fun

    def main(self, ):
        print("Processing API endpoint transaction: ", self.getArgs())
        self.execApi()
        return True


if __name__ == "__main__":
    kclass = Datadog()
    kclass.main()
