#!/usr/bin/python3
from docopt import docopt
import os
import Crawler.crawler

__doc__ = \
    """
Usage: 
    aid -a | --all <module>...
    aid -c | --crawler <module>...
    aid -d | --downloader <module>...
    aid -v | --verifier <module>...
    aid -p | --packager <module>...
    aid -u | --unpackager <module>...
    aid -h | --help
    aid -l | --list
        
 
Options:
    when no module is specified, all modules will be run
    
    components:
    -a --all            Run all components with specified modules
    -c --crawler        Run the Crawler component
    -d --downloader     Run the Downloader component
    -v --verifier       Run the Verifier component
    -p --packager       Run the Packaging components (Pre- and Packaging)
    -u --unpackager     Run the Unpackaging component
    <module>            Specify modules to run with the component
    
    helpers:
    -h --help                   Show this screen
    -l --list                   List all available modules
"""

# Helper functions
def list_modules():
    # Returns the list of modules, when -l is given
    modules_dir = 'Crawler/modules'
    try:
        modules = [f for f in os.listdir(modules_dir) if f.endswith('.py') and not f.startswith('_')] # get all python files in Crawler/modules, excluding _templates
        modules = [f[:-3] for f in modules] # Remove the .py extension
        return modules
    except FileNotFoundError:
        print (f"Directory {modules_dir} not found.")
        return []

def run_component (component, modules): # Run a Single Component
    print (f"Running {component} with modules: {modules}")
    if component == 'crawler':
        Crawler.crawler.get_applications()
    # TODO implement the run_component function

# Main function
if __name__ == '__main__':
    arguments = docopt(__doc__)
    available_modules = list_modules() # get a list of all available modules

    if arguments['--list']:
        print("Available modules:")
        for module in available_modules:
            print(f" - {module}")
        exit(0)

    if not arguments['<module>']:
        selected_modules = available_modules # if no module is specified, run all modules
    else:
        selected_modules = []   # if modules are specified, check if they are available
        for module in arguments['<module>']:
            if module not in available_modules:
                print (f"Module {module} not found.")
            else:
                selected_modules.append(module)

    # if no modules are specified or the modules don't exist -> exit
    if not selected_modules:
        print ("No modules specified, exiting.")
        exit(1)

    for arg in arguments:
        if arguments[arg] == True:
            if arg in ['-a', '--all']:
                run_component('crawler', selected_modules)
                run_component('Downloader', selected_modules)
                run_component('Verifier', selected_modules)
                run_component('Prepackaging', selected_modules)
                run_component('Packaging', selected_modules)
                run_component('Unpackaging', selected_modules)
            elif arg in ['-c', '--crawler']:
                run_component('crawler', selected_modules)
            elif arg in ['-d', '--downloader']:
                run_component('Downloader', selected_modules)
            elif arg in ['-v', '--verifier']:
                run_component('Verifier', selected_modules)
            elif arg in ['-p', '--packager']:
                run_component('Prepackaging', selected_modules)
                run_component('Packaging', selected_modules)
            elif arg in ['-u', '--unpackager']:
                run_component('Unpackaging', selected_modules)

    # TODO implement progress bar
    # TODO implement logging







