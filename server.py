#10440-10447
# ['Juzang', 'Bernard', 'Jaquez', 'Campbell', 'Clark']
'''
adapted from Kimmo's previous year's slides
thank you Kimmo for the example
'''

import argparse
import startserver

def parsing():
    parser = argparse.ArgumentParser(description='Take a server.')
    parser.add_argument('server', nargs=1, choices = ['Juzang', 'Bernard', 'Jaquez', 'Campbell', 'Clark'],
                         help='start a server')
    args = parser.parse_args()
    myserver = args.server[0]
    startserver.startserver(myserver)
    

if __name__ == "__main__":
    parsing()
