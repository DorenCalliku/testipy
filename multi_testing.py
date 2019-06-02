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
        list_input = generate_trials(list_trials, len(args[0]))
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
        "numbers": [-1,0, 1.1, 100, 1.0j ],
        "string":  ["testing", u"testing"],
        "tuple": [("test_1",0), (None,0 ), ("test", None)],
        "list": [["test_1",0],[None,0],["test_1", None],[],[0]],
        "dict": [{"test_1":0},{None:0},{"test_1":None}]
    }
    list_functions, list_exceptions = find_testable()
    list_functions = list_functions[10:20]
    list_trials = [] # all the options you want to try
    for each in input_trials.keys():
        list_trials += input_trials[each]
    #list_trials = list_trials[:4]
    
    list_functions = test_verification(list_functions)

    #pprint.pprint(list_functions)
    
    print(time.time()-start)
'''
# run code for singular run
def test_single(vals):
    """ Run this method for this input. Return -1 if not accepted.
    
    Parameters:
    method_to_call:   the method you are testing.
    each_input:       input you are going to run the method through
    """
    
    meth       =  vals[0]
    each_input =  vals[1]
    try:                      # save input as acceptable
        caller( meth, each_input)
        return each_input
    except Exception as e:    # skip
        return -1

if __name__ == '__main__':
    start = time.time()
    input_trials = {
        "none": [None],
        "boolean": [True, False],
        "numbers": [-1,0, 1.1, 100, 1.0j ],
        "string":  ["testing", u"testing"],
        "tuple": [("test_1",0), (None,0 ), ("test", None)],
        "list": [["test_1",0],[None,0],["test_1", None],[],[0]],
        "dict": [{"test_1":0},{None:0},{"test_1":None}]
    }
    list_functions, list_exceptions = find_testable()
    
    list_trials = [] # all the options you want to try
    for each in input_trials.keys():
        list_trials += input_trials[each]
    list_trials = list_trials[5:9]
    
    print(time.time()-start)
    
    # for each method get the number of arguments
    for each in list_functions[1:3]:
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
        list_input = generate_trials(list_trials, len(args[0]))
        p = Process(target=test_single, args=([method_to_call,list_trials],))
        p.start()
        p.join()
    print(list_functions[1:3])
'''
