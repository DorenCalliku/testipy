#!/usr/bin/env python
# coding: utf-8

#################################################
# description:  take a website and run it through the tools.
# references:
        # github.guacamole: https://github.com/berkgoksel/guacamole
#################################################

# import libraries
import glob
import os,sys, importlib
import types, time, inspect
import pprint
import itertools        
from multiprocessing import Pool, Process
import tools.testable_files as find

def caller(func, args):
    """Used to call the methods by passing a list args.
    Parameters:
    ------------
    func:   the method to be called.
    args:   the arguments to be passed.
    """
    
    func(*args)
    

def generate_trials( list_trials , num_args):
    """Generate input for the tests depending on the number of args.
    
    Parameters:
    ------------
    list_input:    all possible input listed for generation
    num_args:      number of arguments the method needs to take    
    """
    
    return [list(p) for p in itertools.product(list_trials, repeat=num_args)]


def test_verification( list_functions = [], verbose = False):
    """Tests if the methods crash because of wrong input.
    
    Parameters:
    -----------
    list_functions:   input methods to check if they run properly with different input
    """
    
    # for each method get the number of arguments
    for each in list_functions:
        print("\n\n", each['method_name'])
        print("\n\n")
        each['acceptable_input'] = []
        try:       # import the file and methods
            last_sep = each['position'].rfind('/')
            sys.path.append( each['position'][ : last_sep])
            env = importlib.import_module( each['position'][ last_sep+1 : ])
        except Exception as e:
            print(e)
            continue
        method_to_call = getattr( env, each[ 'method_name']) # callable
        args = each['arguments']   # get args
        if args[0][0] == 'self':   # class: needs other testing
            continue 
        try:                       # simple testing
            err_ar = (len(args[0])+ 1)*[0]
            caller( method_to_call, err_ar)
            each['acceptable_input'].append(err_ar)
        except Exception as e:
            None
        
        list_input = []
        for i in range(0, len(args[0])):
            list_input += generate_trials(list_trials, i)
        for each_input in list_input: # try for each input type
            if verbose:
                print('Trying: ', each_input)
            try:                      # save input as acceptable
                caller( method_to_call, each_input)
                each['acceptable_input'].append( each_input)
            except Exception as e:    # skip
                None
    return list_functions

if __name__ == "__main__":
    start = time.time()
    input_trials = {
        "none": [None],
        "boolean": [True, False],
        "numbers": [-1,0, 1.1, 1, 1.0j ],
        "string":  ["testing", u"testing", "google.com"],
        "tuple": [("test_1",0), (None,0 ), ("test", None)],
        "list": [["test_1",0],[None,0],["test_1", None],[],[0]],
        "dict": [{"test_1":0},{None:0},{"test_1":None}]
    }
    list_functions, list_exceptions = find.find_testable("/../src/local/")
    
    #pprint.pprint(list_functions)
    list_functions = list_functions[:]
    list_trials = [] # all the options you want to try
    for each in input_trials.keys():
        list_trials += input_trials[each]
    list_trials = list_trials[:4]
    list_functions = test_verification(list_functions, True)
    pprint.pprint(list_functions)
    print(time.time()-start)
