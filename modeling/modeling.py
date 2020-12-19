import warnings

warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import pickle as pkl
from tqdm import tqdm

np.random.seed(2020)

# modules sklearn

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

import time
from joblib import dump

# modules MIP-EGO (actually it's the BO package from Hao's github)

from boruta_feature_selection import boruta_feature_selection
from bayes_optim import BO, NominalSpace, OrdinalSpace
from bayes_optim.Surrogate import RandomForest, GaussianProcess
# from bayes_optim.SearchSpace import NominalSpace, OrdinalSpace


def modeling(train, targets, to_optimize, **kwargs):
    """
    Training and performing hyperparmeter optimization
    by Bayesian Optimization. Currently only supporting
    Random Forests.
    TODO: Make the HO and train_seting more interactive

    :param to_optimize: perform or not HO (boolean)
    :param train: train set (pandas)
    :param targets: targets (labels) (np.arrays)
    :cv: CV count for hyperparameter optimization
    :to_drop: Features to be dropped from learning such as unit numbers,
     cycles, etc (list of string names)
    :DoE_size: Initial design of experiment for the BO HO.
    :max_FEs: maximum number of function evaluations of the BO HO
    :features_list= a list of features to use, cv=
    :return: trained model and list of used features
    """

    start = time.time()
    features_list = kwargs.get('features_list', None)
    to_drop = kwargs.get('to_drop', None)
    cv = kwargs.get('cv', 10)
    DoE_size = kwargs.get('DoE_size', 200)
    max_FEs = kwargs.get('max_FEs', 20)

    print(max_FEs)
    print(to_drop)

    train_set = train.copy()
    if to_drop:
        train_set.drop(to_drop, axis=1, inplace=True)

    if features_list:
        print('Features selected by user')
        train_set = train_set[features_list]
        train_set = train_set.values

    else:
        print('Feature Selection')
        train_set, features_list = boruta_feature_selection(train_set, targets)

        with open('./features_list.pkl', 'wb') as f:
            pkl.dump(features_list, f)

    df_columns = ['acc', 'max_depth', 'n_estimators', 'bootstrap', 'max_features', 'min_samples_leaf',
                  'min_samples_split']

    df_eval = pd.DataFrame(columns=df_columns)

    # max_FEs = 3  # reduced from 200 to 20 for testing
    # DoE_size = 2

    # Hyperparameter optimization
    # objective function
    def obj_func(x):

        # logger.info('Started internal cross-validation')
        nonlocal df_eval

        performance_ = []

        skf = StratifiedKFold(n_splits=cv, random_state=np.random, shuffle=True)
        for train_set_index, test_index in tqdm(skf.split(train_set, targets), 'Optimizing HO'):
            X_train_set, X_test = train_set[train_set_index], train_set[test_index]
            y_train_set, y_test = targets[train_set_index], targets[test_index]

            rf_ = RandomForestClassifier(n_estimators=int(x[1]), max_depth=int(x[0]), bootstrap=x[2],
                                         max_features=x[3], min_samples_leaf=x[4], min_samples_split=x[5],
                                         n_jobs=-1)

            rf_.fit(X_train_set, y_train_set)

            predictions_ = rf_.predict(X_test)

            performance_.append(accuracy_score(y_test, predictions_))

        val = np.mean(performance_)

        df_eval_tmp = pd.DataFrame([[val, x[0], x[1], x[2], x[3], x[4], x[5]]],
                                   columns=df_columns)
        df_eval = df_eval.append(df_eval_tmp)
        return val

    # definition of hyperparameter search space:
    max_depth = OrdinalSpace([2, 100])
    n_estimators = OrdinalSpace([1, 1000])
    min_samples_leaf = OrdinalSpace([1, 10])
    min_samples_split = OrdinalSpace([2, 20])
    bootstrap = NominalSpace(['True', 'False'])
    max_features = NominalSpace(['auto', 'sqrt', 'log2'])

    search_space = max_depth + n_estimators + bootstrap + max_features + min_samples_leaf + min_samples_split
    model = RandomForest(levels=search_space.levels)

    opt = BO(search_space=search_space, obj_fun=obj_func, model=model, max_FEs=max_FEs,
             DoE_size=DoE_size,
             n_point=1,
             n_job=1,
             minimize=False,
             verbose=False)

    if to_optimize:
        print('Hyperparameter optimization')
        opt.run()
    best_params_ = df_eval[df_columns[1:]][df_eval['acc'] == df_eval['acc'].max()][:1].to_dict('records')

    # Training using the best parameters
    if to_optimize:
        rf = RandomForestClassifier(n_jobs=-1, **best_params_[0])
    else:
        rf = RandomForestClassifier(n_jobs=-1)
    rf.fit(train_set, targets)

    dump(rf, './rf_model.joblib')
    end = time.time()

    print(f'----Duration of repetition is {(end - start) / 60} minutes')

    return rf, features_list
