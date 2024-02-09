import inspect
import os
from pathlib import Path
import datetime
import json
from collections import OrderedDict
import importlib
from types import MethodType
from functools import wraps



def track_this_method(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        method_name = func.__name__
        method = func.__get__(self, type(self))
        file_path = Path(inspect.getfile(method))
        
        print(f'Method being called: {method_name}')
        file_contents = open(file_path, 'r').read()
        module_folder = os.path.join(file_path.parent, 'saved_modules', file_path.name.rstrip('.py'))
        print(f'Path to module it belongs to: {module_folder}')
        used_module_path = os.path.join(module_folder, f'{self.NOW}.py')

        # Create a new folder for this module if one doesn't exist
        if not os.path.exists(module_folder):
            os.makedirs(module_folder)
            print(f'Created new folder for {file_path.name}')

        # If this is a new version of the module, save it.
        save_new_code = True
        for previous_fname in os.listdir(module_folder):
            if previous_fname != '.ipynb_checkpoints':
                previous_fname_path = os.path.join(module_folder, previous_fname)
                fname_contents = open(previous_fname_path, 'r').read()
                if file_contents == fname_contents:
                    print(f'Reusing saved file: {previous_fname}')
                    used_module_path = previous_fname_path
                    save_new_code = False
                    break
        if save_new_code:
            print(f"Saving new file: {self.NOW}.py")
            with open(used_module_path, 'w') as f:
                f.write(file_contents)

        self.experiment[method_name] = used_module_path
        print()

        # Call the original method
        return func(self, *args, **kwargs)
    return wrapper



class Tracker:
    def __init__(self, module_names):
        self.NOW = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
        self.experiment = OrderedDict()
        self.load_modules_and_attach_methods(module_names)


    def load_modules_and_attach_methods(self, module_names):
        for name in module_names:
            module = importlib.import_module(name)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr):
                    bound_method = MethodType(attr, self)
                    setattr(self, attr_name, bound_method)


    def save_experiment(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if not os.path.exists('saved_experiments'):
                os.mkdir('saved_experiments')
            with open(f'saved_experiments/{self.NOW}.json', 'w') as f:
                f.write(json.dumps(self.experiment))
            return result
        return wrapper


    @track_this_method
    @save_experiment
    def main(self):
        self.main_function()