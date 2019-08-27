# imports
import numpy as np
import pandas as pd
from flask import Flask, request, render_template, jsonify
# read in recommender df
recommender_df = pd.read_csv('../data/tfidf_recommender.csv').set_index('name_x')
# initialize the flask app
app = Flask('myApp')
### route 1: hello world
# define the route
@app.route('/')
# create the controller
def form():
    #return the view
    return render_template('form.html')

@app.route('/submit')

def submit():
    user_input = request.args
    # get user input from dict
    product = user_input["ProductName"]
    # run sort values code
    results = list(recommender_df[product].sort_values()[1:11].index)

    return jsonify({'results': results})
    # sort values list

# run the app
if __name__ == '__main__':
    app.run(debug=True)
