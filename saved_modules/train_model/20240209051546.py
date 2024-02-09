import ditto
from sklearn.linear_model import LinearRegression



@ditto.track_function
def run(X, y):
    model = LinearRegression()
    model.fit(X,y)
    return model