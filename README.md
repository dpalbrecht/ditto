<img src="https://github.com/dpalbrecht/ditto/assets/20650445/c3835c89-01b8-4841-ab4a-d25dabdb3086" width="150"><br>
<h2>A lightweight framework for easy ML experiment tracking.</h2>
<h3>Ditto's purpose is to store the code you write, as you run experiments, such that you don't have to worry about keeping track of what you're doing and the effects on your results. 
All you have to do is experiment.</h3>
<br>
<div>The intended workflow is as follows (and as shown in this repo):</div>
<ol>
  <li>Define your experiment in any number of modules, such as <code>get_data.py</code>, <code>train_model.py</code>, and <code>evaluate_model.py</code>.</li>
  <li>For each module that you want to keep track of, decorate the main controller function of the module with the <code>@ditto.track_function</code> decorator.</li>
  <li>Define a function, in another module like <code>controller.py</code> or in your monolithic module, that controls the entire experiment from end-to-end. Decorate it with the  <code>@ditto.save_experiment</code> decorator to keep track of the experiment and results. This function should return your results to be saved. It is also recommended to decorate it with <code>@ditto.track_function</code> second to keep track of the module.</li>
  <li>Run your main controller function and watch the experiment run!</li>
</ol>
<br>
An example like the above is shown in the modules in this repo and finally called in <code>Example.ipynb</code>.
