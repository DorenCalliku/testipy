#!/usr/bin/env python
# coding: utf-8

#################################################
# description:  find the testing files.
# references:
        # 
#################################################

# import libraries
import glob
import os,sys, importlib
import types, time, inspect
import pprint
import itertools        

def clear_dir( directory):
    """Remove ../ from the directory address because of sys.path && import_module.
    Usage: print(clear_dir("x/test_validation/../../src/local/wrapper"))
    
    Parameters:
    -----------
    directory:   directory position.
    """
    
    list_path = directory.split('/')
    while '..' in list_path:
        cd = [i for i,x in enumerate(list_path) if x == '..']
        list_path.pop(cd[0])
        list_path.pop(cd[0]-1)
    return '/'.join(list_path)
    
    
def verifier():
    """Generate list of trials to check if functions work."""
    
    input_trials = {
        "none": [None],
        "boolean": [True, False],
        "numbers": [-1,0, 1.1, 100, 1.0j ],
        "string":  ["testing", u"testing"],
        "tuple": [("test_1",0), (None,0 ), ("test", None)],
        "list": [["test_1",0],[None,0],["test_1", None],[],[0]],
        "dict": [{"test_1":0},{None:0},{"test_1":None}]
    }
      
    list_trials = [] # all the options you want to try
    for each in input_trials.keys():
        list_trials += input_trials[each]
    return list_trials[ 5 : 9]


def generate_trials( num_args, extra = []):
    """Generate input for the tests depending on the number of args.
    
    Parameters:
    ------------
    list_input:    all possible input listed for generation
    num_args:      number of arguments the method needs to take    
    """
    
    list_trials = verifier() 
    if extra == []: 
        list_trials += extra
    trials      = []
    for i in range(0,num_args+1):
        trials += [list(p) for p in itertools.product( list_trials, repeat=i)]
    return trials


def caller(func, args):
    """Used to call the methods by passing a list args.
    Parameters:
    ------------
    func:   the method to be called.
    args:   the arguments to be passed.
    """
    
    return func(*args)


def get_extra( list_exceptions):
    """Find libraries and classes imported.
    
    Parameters:
    -------------
    list_exceptions:  result from testable files"""
    
    libraries =[]
    ## find libraries in a src code tree
    for each in list_exceptions:
        if not each['name'].startswith('__'):
            libraries.append(each['name'])
    libraries = list(set(libraries))
    return libraries


# turn complex to str
def replace_problem( inp, type_inp = complex):
    """Replace complex numbers with strings of 
       complex number + __ in the beginning.
       
    Parameters:
    ------------
    inp:       input dictionary.
    type_inp:  can be an exception or complex number
    """
    
    try:
        if isinstance(inp, type_inp):
            return "__" + str(inp)
        elif isinstance(inp, list):
            for each in range(len(inp)):
                inp[ each] = replace_problem( inp[ each])
            return inp
        elif isinstance(inp, dict):
            for key,val in inp.items():
                inp[key] = replace_problem( val)
                return inp
        else:
            return inp # nothing found - better than no checks
    except Exception as e:
        print(e)
        return ""

if __name__ == "__main__":
    start = time.time()
    print("Time consumed:   ", time.time()-start)
