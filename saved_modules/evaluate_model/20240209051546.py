import ditto
from sklearn.metrics import mean_absolute_error



@ditto.track_function
def run(X, y, model):
    results = {'MAE': mean_absolute_error(y, model.predict(X))}
    return results