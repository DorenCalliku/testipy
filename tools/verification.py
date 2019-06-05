# import libraries
from   multiprocessing import Pool
import tools.helper  as hlp
import tools.wrapper as wrapper
import itertools
wrapper = wrapper.wrapper

    
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
    return list_trials


def generate_trials( num_args, extra = []):
    """Generate input for the tests depending on the number of args.
    
    Parameters:
    ------------
    list_input:    all possible input listed for generation
    num_args:      number of arguments the method needs to take    
    """
    
    list_trials = verifier() 
    if extra != []: 
        list_trials = extra
    trials      = []
    for i in range(0,num_args+1):
        trials += [list(p) for p in itertools.product( list_trials, repeat=i)]
    return trials


def verify_method( method_info, method_to_call, verbose = False, extra = [], classe = False):
    """Run the code with different input to understand what kinds of inputs 
    are acceptable and to expect different run-time errors when using this code.
    
    Parameters:
    -------------
    method_info:    method information provided by calling method.
    method_to_call: location of running method.
    verbose:        printing while running.
    extra:          extra parameters you want to run the code through.
    classe:         is it a class obj or method.
    """
    
    print("\nVerifying:") if verbose else None
    try:                         # if wrong structure of method_info
        list_input = generate_trials( len(method_info['arguments'][0]), extra) \
               if not classe else generate_trials( len(method_info['arguments'][0]) -1, extra)
    except Exception as e:
        if verbose:
            print(e)
        return []
    acceptable = []               # input that worked
    try:                          # try for empty input
        empty = method_to_call()
        if verbose:
            print('\t{0: <30} -> '.format("__empty") \
                + '\t{0: <10}'.format(str(empty)))
        acceptable.append("__empty")
    except:
        None
    for each_input in list_input: # try for each input type
        each_input = each_input
        try:
            result = method_to_call( *each_input)
            if verbose:
                print('\t{0: <30} -> '.format( str(each_input)) \
                    + '\t{0: <10}'.format(str(result)))
            acceptable.append( each_input)
        except Exception as e:    # skip
            None
    if acceptable == []:
        if verbose:
            print("\tMethod most probably has domain specific input.")
    return acceptable 
    
