#!/usr/bin/env python
# coding: utf-8

#################################################
# description:  
# references:
        # github.guacamole: 
#################################################

# import libraries
import glob
import os,sys, importlib
import types, time, inspect
import pprint
import itertools, json       
from multiprocessing import Pool


validation_configuration = {
    "home_doren_Desktop_guacamole_src_local_adder":[[0,0,0]]
}

def find_testable_2( location = "/home/doren/Desktop/guacamole/src/local"):
    """Find testable files by using os.walk().
    
    Parameters:
    -----------
    location:    where to look for files
    """
    
    methods      = []
    exceptions   = []
    for each_tuple in os.walk(location): # get all results
        if '.git' not in each_tuple[0] and '__pycache__' not in each_tuple[0]: # skip git files
            for each in each_tuple[2]:  # for each file
                if each.endswith('.py'):
                    sys.path.append( each_tuple[0])
                    try: # try to import file
                        environment = importlib.import_module(each[:-3])
                    except: # skip
                        continue
                    for method in dir(environment): # get each method/function
                        try:
                            method_to_call = getattr(environment, method)
                            method_info    = { 'position':    each_tuple[0],
                                               'method_name': method,
                                               'arguments':   inspect.getfullargspec( method_to_call),
                                               'validation_file':  '_'.join( each_tuple[0].split('/') )[1:] + method,
                                                'valid': False}
                            
                            #<====== Verify =======>
                            #verify( method_info)
                            
                            #<====== Validate =====>
                            try:
                                validity = True
                                with open("validation/"+ method_info['validation_file']+'.json', 'r') as f:
                                    valid_output = json.load(f)

                                for index in range(len(validation_configuration[ method_info[ 'validation_file']])):
                                    valid_input = validation_configuration[ method_info[ 'validation_file']][index]

                                    validity &= method_to_call(*valid_input) == valid_output[index]
                                if validity:
                                    method_info['valid'] = True
                                    
                            except Exception as e:
                                #print(e)
                                None
                            methods    += [method_info]
                        except Exception as e:
                            exceptions += [{"name": method, "exception": e}]
    return methods, exceptions

if __name__ == "__main__":
    methods, exceptions = find_testable_2("/home/doren/Desktop/guacamole/src/local/")

    for each in methods:
        if each['valid']:
            pprint.pprint(each)

