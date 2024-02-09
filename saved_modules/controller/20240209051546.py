import ditto
import get_data
import train_model
import evaluate_model



@ditto.save_experiment
@ditto.track_function
def run():
    X, y = get_data.run()
    model = train_model.run(X, y)
    result = evaluate_model.run(X, y, model)
    return result