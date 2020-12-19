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
# @click.option('--p', '-P', required=True, default='/home/', type=click.Path(exists=True), help='Input data path',
#               show_default=True, prompt='Please specify input data location')
def main(workshops, components, lookback):
    number_of_workshops = workshops
    number_of_components = components
    lookback = lookback

    print('Loading Data')
    root = tk.Tk()
    root.withdraw()
    path_data = filedialog.askopenfilenames(parent=root,
                                         initialdir=os.getcwd(),
                                         title="Please select two files.\n First file should be the train set"
                                               "and second file the test set:")

    train, test = load_data(path_data)
    print('Pre-processing Data')
    train, targets, test = preprocessing(train, test, lookback=lookback)

    drop = click.prompt('Drop certain columns from training [y/N]?', type=bool)
    # TODO: ask the user for multiple input
    if drop:
        to_drop = []
        while drop:
            to_drop.append(click.prompt('Add feature to drop?'))
            drop = click.prompt('Drop more [y/N]?', type=bool)
    #     # to_drop = ['unit', 'cycles']  # not to be used during modeling
    selected_features = click.prompt('List of features to use [y/N]?', type=bool)

    features_list = list(train.columns)
    if selected_features:
        root = tk.Tk()
        root.withdraw()
        path_features = filedialog.askopenfilename(parent=root,
                                                initialdir=os.getcwd(),
                                                title='Enter file name of features:')
        # file = click.prompt('Enter file name of features', type=str)
        with open(path_features, 'rb') as f:
            features_list = pkl.load(f)

    trained = click.prompt('Is there a trained model available already [y/N]?', type=bool)

    if not trained:
        ho = click.prompt('Perform hyperparameter optimization?', default=True, type=bool)
        if ho:
            cv = click.prompt('Please enter a CV value', default=10, type=int)
            DoE_size = click.prompt('Please enter the DoE size', default=20, type=int)
            max_FEs = click.prompt('Please enter the maximum value of function evaluations', default=200, type=int)
            print('Modeling')
            fitted_model, features_list = modeling(train, targets, to_optimize=ho, cv=cv, to_drop=to_drop,
                                                   max_FEs=max_FEs, DoE_size=DoE_size, features_list=features_list)

        else:
            fitted_model, features_list = modeling(train, targets, to_optimize=ho, to_drop=to_drop,
                                                   features_list=features_list)
    else:
        root = tk.Tk()
        root.withdraw()
        path_trained = filedialog.askopenfilename(parent=root,
                                                initialdir=os.getcwd(),
                                                title="Select trained model")
        # file = click.prompt('Enter file name of trained model', type=str)
        fitted_model = load(path_trained)

    print('Health Index construction')
    hi_tr, hi_te = construction(fitted_model, train, test, features_list)
    print('RUL distributions')

    # out_path = click.prompt('Set output path (current path is: '+str(os.getcwd()+')'), type=str)
    root = tk.Tk()
    root.withdraw()
    out_path = filedialog.askdirectory(parent=root,
                                     initialdir=os.getcwd(),
                                     title="Please select an output folder:")
    if not os.path.isdir(out_path):
        os.makedirs(out_path)
    rul_distr(train, test, hi_tr, hi_te, number_of_workshops, number_of_components, out_path)


if __name__ == '__main__':
    main()
