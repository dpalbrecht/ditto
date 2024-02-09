import tracker



def child_function():
    pass


@tracker.save_experiment
@tracker.track_function
def main_function():
    child_function()
    return 'Success!'