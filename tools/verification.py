# import libraries
from   multiprocessing import Pool
import tools.helper  as hlp
import tools.wrapper as wrapper


generate_trials = hlp.generate_trials
wrapper = wrapper.wrapper
    
    
def verify_method( method_info, method_to_call, verbose = False, extra = []):
    """Run the code with different input to understand what kinds of inputs 
    are acceptable and to expect different run-time errors when using this code.
    
    Parameters:
    -------------
    method_info:    method information provided by calling method.
    method_to_call: location of running method.
    verbose:        printing while running.
    extra:          extra parameters you want to run the code through.
    """
    
    if verbose:
        print("\nVerifying:")
    try:                          # if wrong structure of method_info
        list_input = generate_trials( len(method_info['arguments'][0]), extra)
    except Exception as e:
        if verbose:
            print(e)
        return []
    acceptable = []               # input that worked
    for each_input in list_input: # try for each input type
        try:
            if verbose:
                print('\t{0: <30}->\t{0: <10}'.format( \
                            str(each_input), str( method_to_call(*each_input))))
            else:
                method_to_call(*each_input)
            acceptable.append( each_input)
        except Exception as e:    # skip
            None
    return acceptable 
