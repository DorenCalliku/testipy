#!/usr/bin/env python
# coding: utf-8

#################################################
# last tested:  -
# testing file: test_wrapper.py
# description:  protect running time of processes.
# references:   
        # timeout:   https://stackoverflow.com/questions/492519/timeout-on-a-function-call
        #            https://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish
        # spinner:   https://stackoverflow.com/questions/4995733/how-to-create-a-spinning-command-line-cursor
        #            https://github.com/pavdmyt/yaspin
#################################################

from functools import wraps
import errno, traceback
import sys, os, time, signal
import threading


class TimeoutError(Exception):
    """Class for raising errors. Not sure of functionality yet."""
#    print("Method took too long. Interrupting ...")
    pass

def timeout(seconds = 120, error_message = os.strerror(errno.ETIME)):
    """Checks for timeout of the functions.
    
    Parameter:
    ----------
    seconds:         time for the exception to run.
    error_message:   taken from os class error.
    """
    
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator


def wrapper(method_name = "__default", positional_arguments = [], \
            keyword_arguments = None, spinner = False, run_time = 120, verbose = False):
    """Checks for each method.
    1) Does it throw an exception?
    2) Does it pass the timing for a normal function?
    3) Create spinner to not make user bored and to show that it is working.
    
    Parameters:
    -----------
    methodToRun:          the method name.
    positional_arguments: needed arguments whose values are not passed.
    keyword_arguments:    arguments passed with their values.
    run_time:             time it will run before stopping.
    """

    # check for wrong naming
    if method_name == "__default":
        __default()
        return
    # check timing functionalities
    timing = timeout( run_time)
    func   = timing( method_name)
    try:  
        if spinner:
            with Spinner():
            # check the timing of running the method
                if keyword_arguments:
                    return func(*positional_arguments, **keyword_arguments)
                else: 
                    return func(*positional_arguments)
        else:
            if keyword_arguments:
                return func(*positional_arguments, **keyword_arguments)
            else: 
                return func(*positional_arguments)

    except (BrokenPipeError, IOError):
        if verbose:
            print ('BrokenPipeError caught', file = sys.stderr)
        return None
    except Exception:
        if verbose:
            print("Exception at "+ str(method_name))
        return None

class Spinner:
    """For keeping the user focused."""
    
    busy  = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False

    
def adder( a= 4, b = 5):
    """Cheap testing."""
    
    #time.sleep(sleep)
    #print("Checker Method")
    return a + b
    
if __name__ == "__main__":
    print("Run Adder Method.")
    wrapper(adder, positional_arguments = [1],run_time = 100)
    print("Running after checking...")
    
