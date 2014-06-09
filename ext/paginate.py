#
# pagination decorator 
# implemented as an extension exmaple.
# you can easily use this as a template to
# write your own extensions (as decorators)
# validation, authentication, ...
#
# khz / 2014

import functools
import sys
import os

sys.path.append(os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../config" )))
sys.path.append(os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../lib" )))

def will_paginate(per_page=5):
    def paginate(func):
        """ 
            pagination decorator
            You can use it as a template for your own extensions
            Looks a little complex but copy&paste and put your code
            just in wrapper. Rest is (neccesary) boilerplate.

        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            #
            # put your implementation right here. 
            # 
            print("In will_paginate decorator")
            print("  -- per_page: ", per_page)
            print("args: ", args)
            print("kwargs: ",kwargs)
            func(*args,**kwargs)
        return wrapper
    return paginate
