import os, sys, importlib
import types, time, inspect
import pprint
import itertools, json  

import   tools.verification as verification
import   tools.validation   as validation
import   tools.wrapper      as wrapper 

verify_method   = verification.verify_method
validate_method = validation.validate_method
wrapper         = wrapper.wrapper


def run_method( method, location, environment, verify = False, validate = False, \
               verbose = False, run_time = 5, domain_input = [], validation = ''):
    """Run method through different testings.
    
    Parameters:
    ------------
    method:      method name.
    location:    where the file is found.
    environment: where to run the method.
    verify:      check which results accepts.
    validate:    check if it works properly.
    verbose:     print for checking.
    validation:  validation folder.
    """
    
    try:
        method_to_call = getattr(environment, method)
        if inspect.getfullargspec( method_to_call)[0][0]  == 'self':
            if verbose:
                print("Class")
            None       # if it is a class dont do anything for now
        else:
            if verbose:
                print("\n------------------------------------------\n")
                print("Analysing:", method)
                print("\n------------------------------------------\n")
            method_info    = { 'location':    location,
                               'method_name': method,
                               'arguments':   inspect.getfullargspec( method_to_call),
                               'validation_file':  '_'.join( location.split('/') )[1:] + method + '.json',
                               'valid': False}
            if verify:   # don't allow running forever
                method_info['acceptable_args'] = wrapper( verify_method, \
                                                 [method_info, method_to_call, verbose, domain_input]\
                                                 , run_time = run_time)
            if validate: 
                method_info['valid'] = wrapper( validate_method, \
                                                 [ method_info, method_to_call, verbose, validation], \
                                                 run_time = run_time)
        return method_info
    except Exception as e:
        return {"name": method, "exception": e}

    
def run_file( name, location, verify = False, validate = False, \
             verbose = False, run_time = 5, domain_input = [], validation = ''):
    """Run file to check exceptions and validations.
    
    Parameters:
    ------------
    name:     signature of the file
    location: where the file is found to be
    """
    
    if verbose:
        print("\n=================================================\n")
        print("Running through file {} at {}.".format( name, location))
        print("\n=================================================\n")
    methods      = []
    exceptions   = []
    sys.path.append(location)
    try: # try to import file
        environment = importlib.import_module( name[:-3]) # remove .py
    except: # skip
        return [],[]
    for method in dir(environment): # get each method/function
        result = run_method(method, location, environment, verify, validate,\
                            verbose, run_time, domain_input, validation)
        if result != None:
            if 'exception' in result.keys():
                exceptions.append(result)
            else:
                methods.append(result)
    return methods, exceptions 
