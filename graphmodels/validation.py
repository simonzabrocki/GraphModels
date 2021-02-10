from sklearn.metrics import r2_score
import plotly.express as px
import numpy as np
import pandas as pd

'''
TO IMPROVE
Make the graph more flexible in terms of hoverdata etc, function has now weird parameters
also plot_comp_base have reveresed agruments
check model should plot the one that are not checked
'''


def check_model(Model, X, y_true):
    '''Run a model without scenario to check that the aggregation is correct

    TO CLEAN UP

    '''

    results = Model.run(X)

    print('Checking computations:')
    for var in y_true.keys():
        computation = results[var]
        baseline = y_true[var]
        scores = scores_baseline_computation(baseline, computation)
        print(var, "r2:", scores['r2'], end=' | ')
        print(var, "corr:", scores['corr'])


def scores_baseline_computation(baseline, computation):

    base_comp = pd.concat([baseline, computation], axis=1).replace(
        [np.inf, -np.inf], np.nan).dropna()

    base_comp.columns = ['baseline', 'computation']

    return {'r2': r2_score(base_comp.baseline, base_comp.computation), 'corr': base_comp.baseline.corr(base_comp.computation)}


def plot_computation_vs_baseline(baseline, computation):
    df = pd.concat([baseline, computation], axis=1).dropna()
    df.columns = ['baseline', 'computation']
    fig = px.scatter(df.reset_index(), x=f'baseline', y=f'computation', hover_data=['ISO', 'Year'], trendline='ols')
    return fig


def check_variable_graph(Model, X, y_true, var):
    """TO CLEAN UP"""
    results = Model.run(X)

    computation = results[var]
    baseline = y_true[var]
    scores = scores_baseline_computation(baseline, computation)
    print(var, "r2:", scores['r2'], end=' | ')
    print(var, "corr:", scores['corr'])

    return plot_computation_vs_baseline(baseline, computation)
