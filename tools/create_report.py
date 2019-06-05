#!/usr/bin/env python
# coding: utf-8

#################################################
# last tested:  -
# testing file: test_create_report.py
# description:  create the report after getting the analysis 
# references:   
        # pdfkit:   https://pypi.org/project/pdfkit/
#################################################

# import libraries
import argparse, pdfkit


# Create Report
def construct_string(inp):
    """Create printing options for input.
    
    Parameter:
    -----------
    inp:    input which can be of different types
            for now takes in consideration:
            - string, list, dict
    """

    string = ""
    try:
        if isinstance(inp, str):
            string += inp 
        elif isinstance(inp, list):
            string += "\n"
            for each in inp:
                string += "\t" + construct_string(each) + "\n"
            string += "\n"
        elif isinstance(inp, dict):
            string += "\n"
            for key,val in inp.items():
                result = construct_string(val)
                if result != None:
                    string += key + " : " + result + "\n"
        else:
            return None # nothing found - better than no checks
        return string
    except:
        return None
   
                    
def create_report(recon, html = "results/report_results.html"):
    """Create PDF report related to the analysis that you run."""

    # structure of html
    string_input = """<!DOCTYPE html> <html> <body>
    <h1> Testing Report</h2>
    <h2> Code </h2>
    <p> a1 </p>
    </body></html>"""
    string_input = string_input.replace('a1', construct_string(recon) ).replace("\n","<br />\n")\
                  .replace("\t","&nbsp;&nbsp;&nbsp;")
    with open(html, "w+") as html:
        html.write(string_input)
    options = {'quiet': ''}
    pdfkit.from_file("results/report_results.html", 'results/report_results.pdf', options=options)
    return
