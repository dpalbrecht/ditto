import ditto
from sklearn.linear_model import LogisticRegression



@ditto.track_function
def run(X, y):
    model = LogisticRegression()
    model.fit(X,y)
    return model