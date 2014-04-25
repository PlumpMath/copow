#
# small module with basic cli progress bars.
# based on and  inspired by:  
#       http://thelivingpearl.com/2012/12/31/creating-progress-bars-with-python/
# but functionality implemented as coroutine.
#
# Author: khz@tzi.org
# Web: www.pythononwheels.org
# 
# Licence: short: Free to use for all purposes.
# Licence detailed: Apache 2.0 (more see: http://www.apache.org/licenses/LICENSE-2.0)
#
# Have fun !

import sys
import time

def progress_bar_sequence(  max, steps=10, status_string="Starting", pattern=".", 
                            placeholder= " ", end_string='Done! ' ):
    """
        Parameters:
            max             : maximum number of calls to .send update method
            steps           : how many steps would you like in your progress bar.
            status_string   : The String preceeding the progress bar.
            pattern         : progress bar indicator (default is .)
            placeholder     : the character shown before a step is updated. Default is " "
            
            example: max = 100, steps = 10 all others default would result in:

                Starting  [  ..........  ]

    """
    # initialize the progress bar with give size and placeholders.
    print status_string,
    print ' [ ',
    print steps*placeholder,
    print ' ]',
    shiftback = steps+4
    print '\b'*(shiftback),
    sys.stdout.flush()
    mod = max / steps
    # enter coroutine
    while True:
        # next line is fed by the call to send()
        num = (yield)
        # update the progress bar
        if num % mod == 0:
            print '\b' + pattern,
            sys.stdout.flush()
        if num == max-1:
            print '\b ] ' + end_string
            sys.stdout.flush()


def progress_bar_slash(status_string="Starting"):
    """
        Parameter: sleep => time to wait until the next printed update 
        just for the beauty ;)

        Result looks like: Starting [ / ] 
            with a rotating center

    """
    print status_string,
    print ' [   ]',
    print '\b'*3,
    sys.stdout.flush()
    while True:
        num = (yield)
        if (num%4) == 0: 
            sys.stdout.write('\b/')
        elif (num%4) == 1: 
            sys.stdout.write('\b-')
        elif (num%4) == 2: 
            sys.stdout.write('\b\\')
        elif (num%4) == 3: 
            sys.stdout.write('\b|')
        sys.stdout.flush()