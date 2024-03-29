import inspect
import os
from pathlib import Path
from collections import OrderedDict
from functools import wraps
import datetime
import json



def track_function(func):
    """
    Tracks the module of the function that it decorates.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the name of the function being called
        file_path = Path(inspect.getfile(func))
        function_name = f"{file_path.name.rstrip('.py')}.{func.__name__}"
        print(f'Function being called: {function_name}')

        # Construct the path of the module the function is defined in
        original_module_folder = os.path.join(file_path.parent, file_path.name.rstrip('.py'))
        print(f'Path to module it belongs to: {original_module_folder}')

        # Create a new folder for this module if one doesn't exist
        saved_module_folder = os.path.join(file_path.parent, 'saved_modules', file_path.name.rstrip('.py'))
        if not os.path.exists(saved_module_folder):
            os.makedirs(saved_module_folder)
            print(f'Created new folder for {file_path.name}')

        # If this is a new version of the module, save it
        used_module_path = os.path.join(saved_module_folder, f'{NOW}.py')
        save_new_code = True
        file_contents = open(file_path, 'r').read()
        for previous_fname in os.listdir(saved_module_folder):
            if previous_fname != '.ipynb_checkpoints':
                previous_fname_path = os.path.join(saved_module_folder, previous_fname)
                fname_contents = open(previous_fname_path, 'r').read()
                if file_contents == fname_contents:
                    print(f'Reusing saved file: {previous_fname}')
                    used_module_path = previous_fname_path
                    save_new_code = False
                    break
        if save_new_code:
            print(f"Saving new file: {NOW}.py")
            with open(used_module_path, 'w') as f:
                f.write(file_contents)

        # Log experiment details
        EXPERIMENT[function_name] = used_module_path

        print()
        return func(*args, **kwargs)
    return wrapper


def save_experiment(func):
    """
    Initializes and saves an experiment.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Initialize a fresh EXPERIMENT dictionary and NOW value for this invocation
        global NOW, EXPERIMENT
        NOW = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
        EXPERIMENT = OrderedDict()

        # Call the main function and save results
        EXPERIMENT['results'] = func(*args, **kwargs)

        # Save the experiment data after the function completes
        if not os.path.exists('saved_experiments'):
            os.mkdir('saved_experiments')
        with open(f'saved_experiments/{NOW}.json', 'w') as f:
            f.write(json.dumps(EXPERIMENT, indent=4))
            
        print('Done!')
        return None
    return wrapper