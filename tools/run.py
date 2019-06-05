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


def run_method( method, location, environment, verify = False, validate = False,\
               verbose = False, run_time = 5, domain_input = [], validation = '', classe = False):
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
    
    methods = []
    try:
        method_to_call = getattr(environment, method)
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
                                             [method_info, method_to_call, verbose, domain_input, classe]\
                                             , run_time = run_time)
        if validate: 
            method_info['valid'] = wrapper( validate_method, \
                                             [ method_info, method_to_call, verbose, validation], \
                                             run_time = run_time)
        methods.append(method_info)
        # in case you found a class run its methods
        if inspect.getfullargspec( method_to_call)[0][0]  == 'self':
            obj_methods = [ method for method in dir( method_to_call) \
                                    if callable(getattr(method_to_call, method))\
                                   and '__' not in method]
            classe = method_to_call()
            for each in obj_methods:
                methods.append( run_method( each, location, classe, verify, validate,\
                   verbose, run_time, domain_input, validation, classe))
    except Exception as e:
        methods.append({"name": method, "exception": e})
    return methods

    
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
    results = []
    sys.path.append(location)
    try: # try to import file
        environment = importlib.import_module( name[:-3]) # remove .py
    except: # skip
        return []
    for method in dir(environment): # get each method/function
        if callable(getattr(environment, method)) and '__' not in method:
            result = run_method(method, location, environment, verify, validate,\
                                verbose, run_time, domain_input, validation)
            results += result                        
    return results
