import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def preprocessing(train, test, lookback):
    """
    Data pre-processing. Currently supporting Standardization
    and labeling of the train set.
    :param train: train set
    :param test: test set
    :param lookback: (int) how many time-steps before the failure
                      should we label the time-steps as faulty
    :return: transformed train and test sets and training labels
    """

    # Z-normalization of training and test sets, based on the training set #
    scaler = StandardScaler()

    train_ = train.copy()
    test_ = test.copy()

    train_norm = scaler.fit_transform(train_.values[:, 2:])
    test_norm = scaler.transform(test_.values[:, 2:])

    n_train = pd.DataFrame(train.values[:, :2], dtype='int64')
    n_test = pd.DataFrame(test.values[:, :2], dtype='int64')

    cols = train.columns
    df_train = pd.DataFrame(train_norm, columns=cols[2:])
    normed_train = pd.concat([n_train, df_train], axis=1)
    df_test = pd.DataFrame(test_norm,  columns=cols[2:])
    normed_test = pd.concat([n_test, df_test], axis=1)

    normed_train.columns = cols
    normed_test.columns = cols

    # Labelling the last k time-steps as faulty (label=1): lookback

    labels = []
    for unit in normed_train.unit.unique():
        temp = normed_train[normed_train.unit == unit]
        max_cycle = temp.cycles.max()
        labels.append((max_cycle - lookback) * [0] + lookback * [1])

    labels = [int(item) for sublist in labels for item in sublist]
    labels = np.array(labels)

    # normed_train['labels'] = labels

    return normed_train, labels, normed_test
