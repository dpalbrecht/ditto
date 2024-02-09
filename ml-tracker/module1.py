from tracker import track_this_method



def child_function(self):
    pass

@track_this_method
def main_function(self):
    self.child_function()