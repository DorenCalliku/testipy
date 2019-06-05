#!/usr/bin/env python
# coding: utf-8


# import libraries
import pprint, json, argparse, sys, os

# local files
import   tools.helper     as helper
import   tools.wrapper    as wrappers
import   tools.run        as run
import   tools.validation as val
import   tools.create_report as cr

def test( location = "/home/doren/Desktop/Python/",\
           verify  = False, validate = False, verbose = False, \
           run_time = 5, domain_input = [], validation = ''):
    """Find testable files by using os.walk().
    
    Parameters:
    -----------
    location:     where to look for files.
    verify:       apply verification to all python files and modules.
    validate:     apply validation related.
    verbose:      check what happens with the tests.
    run_time:     allow the code to run for this much for each of verification codes.
    domain_input: add to the list of checks you want to do.
    validation:   folder of validation tests.
    """
    
    if verbose:
        print("Information organized according to file, method")
        print("Some of printed information will be as a result of running the files.")
        print("----------------------------------------------------------------------")
    else:
        print("All of printed information will be as a result of running your code.")
        print("----------------------------------------------------------------------")
    all_methods      = []
    all_exceptions   = []
    for each_tuple in os.walk(location): # get all results
        if '.git' not in each_tuple[0] and '__pycache__' not in each_tuple[0]: # skip git files
            for each in each_tuple[2]:   # for each file
                if each.endswith('.py') and '__' not in each: # is it python
                    methods = run.run_file(each, each_tuple[0], verify, validate, verbose, run_time, domain_input, validation)
    return methods
    
    
def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(
        epilog="\tExample: \r\npython " + sys.argv[0] + " /home/doren/Desktop/Python/"
    )
    parser._optionals.title = "OPTIONS"
    parser.add_argument(   "-l", "--location", help="Which folder to", required=True)
    parser.add_argument( "-ver",   "--verify", help="Run the verification", default=False)
    parser.add_argument( "-val", "--validate", help="Run the validation",   default=False)
    parser.add_argument(   "-v",  "--verbose", help="Show the process progress", default=False)
    parser.add_argument(   "-r", "--run_time", help="Run the processes for this much.", default = 5)
    parser.add_argument(   "-d", "--domain_input", help="Domain inputs that one would try.", nargs="*",type=str, default = [])
    parser.add_argument(   "-f", "--validation", help="Validation folder for the validation process.", default='validation/')
    parser.add_argument(   "-g", "--generate", help="Generate empty files for validation.",   default=False)
    parser.add_argument(   "-s",     "--save", help="Save the information in pdf and json format.", default=False)
    return parser.parse_args()


if __name__ == "__main__":
    import time
    start = time.time()
    args = parse_args()
    all_methods     = test(  location =args.location, verify=args.verify, validate=args.validate,\
                                         verbose=args.verbose , run_time=args.run_time, \
                                         domain_input=args.domain_input, validation=args.validation)
    if all_methods != []:
        if args.verify:
            for each in range(len(all_methods)):
                try:
                    all_methods[ each]['acceptable_args'] = helper.replace_problem(all_methods[ each][ 'acceptable_args'])
                except:
                    None
    """
    with open( "results/analysis.json", "w+") as f:
        json.dump(all_methods, f, sort_keys = True, indent = 4, ensure_ascii = False)
    if args.generate:
        val.generate_validation_files( all_methods)
    if args.save:
        print("Will save info under results/report_results.pdf")
        with open( "results/report_results.json", 'w+') as file:
            json.dump( all_methods, file)
        cr.create_report( all_methods)
    """
    print(time.time()- start)
