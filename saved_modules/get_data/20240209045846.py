import ditto
from sklearn import datasets



@ditto.track_function
def run():
    X, y = datasets.load_iris(return_X_y=True, as_frame=True)
    return X, y