from boruta import BorutaPy
from sklearn.ensemble import RandomForestClassifier


def boruta_feature_selection(X, Y, n_jobs=-1, n_estimators=1000, max_iter=400, verbose=2):
    """
    Boruta feature selection wrapper
    Currently only supporting random forests
    TODO: Add regressor or classifier as argument.

    :param X: training set
    :param Y: train set labels
    :param n_jobs: number of jobs (default -1: all cores)
    :param n_estimators: number of random trees (default 1000)
    :param max_iter: number of iterations (default 400)
    :param verbose: level of verbosity (default 2)
    :return: reduce data sets and selected features
    """
    rf = RandomForestClassifier(n_jobs=n_jobs, n_estimators=n_estimators)
    feat_selector = BorutaPy(rf, n_estimators=n_estimators, alpha=0.05, max_iter=max_iter, verbose=verbose)

    feat_selector.fit(X.values, Y)

    k = 0
    features = X.columns
    features_list = []
    features_importance_list = []

    for i in feat_selector.support_:
        if i:
            features_list.append(features[k])
            features_importance_list.append(feat_selector.ranking_[k])
        k = k + 1

    features_list = [x for _, x in sorted(zip(features_importance_list, features_list))]

    # call transform() on X to filter it down to selected features
    X_boruta = feat_selector.transform(X.values)
    # X_boruta_test = feat_selector.transform(X_test.values)

    return X_boruta, features_list
