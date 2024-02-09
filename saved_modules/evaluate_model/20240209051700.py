import ditto
from sklearn.metrics import accuracy_score



@ditto.track_function
def run(X, y, model):
    results = {'accuracy': accuracy_score(y, model.predict(X))}
    return results