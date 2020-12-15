import pandas as pd
from tqdm import tqdm


def construction(model, train, test, features_list):
    """
    The health index is defined here as the probability of belonging
    to the failure class.

    :param features_list: list of features used in training the model
    :param model: a trained model with class probability outputs
    :param train: train set (pandas)
    :param test: test set (pandas)
    :return: health index curves for train and test sets {dictionary of dataframes}
    """

    F_prob_tr = {}
    # w = 0
    for unit in tqdm(train.unit.unique(), 'Constructing train HI'):
        temp = train[train.unit == unit]
        prob_f = model.predict_proba(temp[features_list])[:, 1]
        F_prob_tr[unit] = pd.DataFrame({'hi': prob_f})

    F_prob_te = {}
    # w = 0
    for unit in tqdm(test.unit.unique(), 'Constructing test HI'):
        temp = test[test.unit == unit]
        prob_f = model.predict_proba(temp[features_list])[:, 1]
        F_prob_te[unit] = pd.DataFrame({'hi': prob_f})

    return F_prob_tr, F_prob_te
