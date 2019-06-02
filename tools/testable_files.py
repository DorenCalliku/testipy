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
from multiprocessing import Pool, Process
import tools.wrapper as wrapper

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
    

def find_testable( directory  = '/../../src/local/'):
    """Walk through the tree of the src of the project and find:
    1) method
    2) method's position
    3) method's arguments
    
    Parameters:
    ------------
    directory:    where to search related to this position.
    """
    
    wd              = os.getcwd()                 # get working directory
    dir_list        = glob.glob(wd + directory)   # search directories 
  
    list_files      = [] # list of files names
    list_functions  = [] # list of functions
    list_exceptions = [] # list of exceptions from calling names
    # find all files
    for each in dir_list: 
        list_files.append([ name.replace(each,'').replace('.py','')\
                            for name in glob.glob(each + '*.py')])
    # find all arguments for each method in these files
    for each_dir in range(0,len(list_files)):
        sys.path.append(dir_list[each_dir])  # bring the path for importing
        for each in list_files[each_dir]:
            try:   # import class
                x = importlib.import_module(each)
                for method in dir(x):
                    try:
                        method_to_call = getattr(x, method)
                        list_functions.append( { 'position': clear_dir(dir_list[each_dir]+each),
                                                 'method_name': method,
                                                 'arguments': inspect.getfullargspec(method_to_call)})
                    except Exception as e:
                        list_exceptions += [{"name": method, "exception": e}]
            except ImportError as err:
                pass

    return list_functions, list_exceptions


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
    
if __name__ == "__main__":
    start = time.time()
    list_functions, list_exceptions = find_testable()
    print("Functions found: ", len(list_functions))
    print("Time consumed:   ", time.time()-start)
