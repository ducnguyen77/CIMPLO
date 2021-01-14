from data_loader import load_data
from modeling import modeling
from transformations import preprocessing
from health_index import construction
from useful_life import rul_distr
import pickle as pkl
from joblib import load
import click
import os
import tkinter as tk
from tkinter import filedialog


@click.command()
@click.option('--workshops', '-W', default=1, required=True, type=int, help='Number of workshops', show_default=True,
              prompt='Please specify number of workshops')
@click.option('--components', '-C', default=1, required=True, type=int, help='Number of components', show_default=True,
              prompt='Please specify number of components')
@click.option('--lookback', '-L', default=1, required=True, type=int, help='Lookback value', show_default=True,
              prompt='Please specify lookback value')
@click.option('--path', '-P', required=True, default='/home', type=click.Path(), help='Data path',
              show_default=True, prompt='Please specify input data location')
@click.option('--out', '-OUT', required=True, default='/home', type=click.Path(), help='Output folder',
              show_default=True, prompt='Please specify output location')
@click.option('--model', '-M', default=None, type=click.Path(exists=True),
              help='Path to trained model (if it exists)',  show_default=True)
@click.option('--drop', '-D', default=None, type=str,
              help='Feature(s) to ignore during training', show_default=True, multiple=True)
@click.option('--features', '-F', default=None, type=click.Path(exists=True),
              help='Path to list of features for the model to train on',
              show_default=True)
@click.option('--optim', '-O', default=False, type=bool,
              help='To optimize or not the model hyperparameters (Bayesian Optimization)', show_default=True)
@click.option('--cv', '-CV', default=10, type=int, help='Number of fold of the objective function',
              show_default=True)
@click.option('--doe', '-DOE', default=20, type=int, help='Initial sample for DoE',
              show_default=True)
@click.option('--max_f', '-MAX', default=200, type=int,
              help='Maximum number of function evaluations for the hyperparameter optimization', show_default=True)
# @click.option('--select', '-S', default=True, type=bool, help='Perform feature selection during training?',
#               show_default=True)  # TODO: Can be added..
def main(workshops, components, lookback, path, out, model, drop, features, optim, cv, doe, max_f):
    number_of_workshops = workshops
    number_of_components = components
    lookback = lookback

    print(path)

    click.echo('Loading Data')
    # root = tk.Tk()
    # root.withdraw()
    # path_data = filedialog.askopenfilenames(parent=root,
    #                                      initialdir=os.getcwd(),
    #                                      title="Please select two files.\n First file should be the train set"
    #                                            "and second file the test set:")

    train, test = load_data(path)
    click.echo('Pre-processing Data')
    train, targets, test = preprocessing(train, test, lookback=lookback)

    # drop = click.prompt('Drop certain columns from training [y/N]?', type=bool)
    # # TODO: ask the user for multiple input
    # to_drop = None
    # if drop:
    #     to_drop = []
    #     while drop:
    #         to_drop.append(click.prompt('Add feature to drop?'))
    #         drop = click.prompt('Drop more [y/N]?', type=bool)
    # #     # to_drop = ['unit', 'cycles']  # not to be used during modeling

    click.echo('Modeling')
    feature_list = None
    if model:
        if features:
            with open(features, 'rb') as f:
                feature_list = pkl.load(f)
        fitted_model = load(model)
    # selected_features = click.prompt('List of features to use [y/N]?', type=bool)
    #
    # features_list = list(train.columns)
    # if selected_features:
    #     root = tk.Tk()
    #     root.withdraw()
    #     path_features = filedialog.askopenfilename(parent=root,
    #                                             initialdir=os.getcwd(),
    #                                             title='Enter file name of features:')
    #     # file = click.prompt('Enter file name of features', type=str)
    #     with open(path_features, 'rb') as f:
    #         features_list = pkl.load(f)
    #
    # trained = click.prompt('Is there a trained model available already [y/N]?', type=bool)

    # if not trained:
    #     ho = click.prompt('Perform hyperparameter optimization?', default=True, type=bool)
    #     if ho:
    #         cv = click.prompt('Please enter a CV value', default=10, type=int)
    #         DoE_size = click.prompt('Please enter the DoE size', default=20, type=int)
    #         max_FEs = click.prompt('Please enter the maximum value of function evaluations', default=200, type=int)
    #         print('Modeling')
    #         fitted_model, features_list = modeling(train, targets, to_optimize=ho, cv=cv, to_drop=to_drop,
    #                                                max_FEs=max_FEs, DoE_size=DoE_size, features_list=features_list)
    #
    #     else:
    #         fitted_model, features_list = modeling(train, targets, to_optimize=ho, to_drop=to_drop,
    #                                                features_list=features_list)
    else:
        # root = tk.Tk()
        # root.withdraw()
        # path_trained = filedialog.askopenfilename(parent=root,
        #                                         initialdir=os.getcwd(),
        #                                         title="Select trained model")
        # # file = click.prompt('Enter file name of trained model', type=str)
        if features:
            with open(features, 'rb') as f:
                feature_list = pkl.load(f)

        to_drop = [x for x in drop]
        fitted_model, features_list = modeling(train, targets, to_optimize=optim, cv=cv, to_drop=to_drop,
                                               max_FEs=max_f, DoE_size=doe, features_list=feature_list)

    click.echo('Health Index construction')
    hi_tr, hi_te = construction(fitted_model, train, test, feature_list)
    click.echo('RUL distributions')

    # # out_path = click.prompt('Set output path (current path is: '+str(os.getcwd()+')'), type=str)
    # root = tk.Tk()
    # root.withdraw()
    # out_path = filedialog.askdirectory(parent=root,
    #                                  initialdir=os.getcwd(),
    #                                  title="Please select an output folder:")
    # if not os.path.isdir(out_path):
    #     os.makedirs(out_path)
    rul_distr(train, test, hi_tr, hi_te, number_of_workshops, number_of_components, out)

    click.echo('Process finished!')


if __name__ == '__main__':
    main()
