import json, glob

def get_config( folder):
    """Get local files and also the data inside these files.
    
    Parameters:
    -------------
    folder:    location of the validation file
    """
    
    if folder == 'validation/':
        validation_configuration = glob.glob("../validation/" + "*.json")
    else: 
        files = glob.glob(folder + "*.json")
    validation_configuration = {}
    for each in files:
        with open( each) as file:
            data = json.load(file)
        validation_configuration[each] = data
    return validation_configuration
    

def validate_method( method_info, method_to_call, verbose = False, validation = "validation/" ):
    """Validate if method returns what it is expected to return.
    
    Parameters:
    ------------
    method_info:    method information provided by calling method.
    method_to_call: location of running method.
    verbose:        printing while running.
    validation:     folder for where to check for validating.
    """
    
    if verbose:
        print("\nValidating:")
    try:
        validity = True                                    # set valid in the begining
        with open(validation + method_info["validation_file"]) as f:
            data = json.load( f)    # get the data       
        if data == []:
            if verbose:
                print("\t{} does not have any validation data to be "+\
                       "checked against".format(method_info["method_name"]))
            return False
        for index in range(len(data)):
            valid_input = data[index]['input']
            validity   &= method_to_call(*valid_input) == data[index]['output']
        if validity:
            if verbose:
                print("\t{} passed all tests, valid.".format(method_info["method_name"]))
            return True
        else:
            if verbose:
                print("\t{} did not pass all tests, not valid.".format(method_info["method_name"]))
            return False
    except Exception as e:
        if verbose:
            print(e)
        return False
        
        
def generate_validation_files( methods, validation = "validation/"):
    """Checking validity of validation.
    
    Parameters:
    ------------
    methods:    create these files in folder for further usage
    validation: validation folder
    """
    
    for each in methods: 
        with open( validation + each['validation_file'], 'w+') as f:
            json.dump([], f)
        with open( validation + "sample.json", 'w+') as sample:
            json.dump([{'input':[0], 'output':[0]}], sample)
