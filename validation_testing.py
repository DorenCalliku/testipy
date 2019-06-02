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
import tools.testable_files as find

# validation structure

