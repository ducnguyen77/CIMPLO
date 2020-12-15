from data_loader import load_data
from modeling import modeling
from transformations import preprocessing
from health_index import construction
from useful_life import rul_distr
import pickle as pkl
from joblib import load

if __name__ == '__main__':

    # TODO: To become more interactive
    # The parameters below are just examples
    number_of_workshops = 3
    number_of_components = 1
    lookback = 25

    cv = 10
    DoE_size = 3
    max_FEs = 2
    to_drop = ['unit', 'cycles']  # not to be used during modeling

    with open('../sample_data_modeling/CMAPSS_1/features_list25_rep_1.pkl', 'rb') as f:
        features_list = pkl.load(f)

    print('Loading Data')
    train, test = load_data()  # it takes by default the dataset t=1
    print('Pre-processing Data')
    train, targets, test = preprocessing(train, test, lookback=lookback)
    print('Modeling')
    # fitted_model, features_list = modeling(train, targets, cv=cv, to_drop=to_drop, max_FEs=max_FEs, DoE_size=DoE_size,
    #                                        features_list=features_list)
    # Note: Temporary
    fitted_model = load('../sample_data_modeling/CMAPSS_1/rf_all_set1_boruta_no_unit_no_cycles_25_rep_1.joblib')

    print('Health Index construction')
    hi_tr, hi_te = construction(fitted_model, train, test, features_list)
    print('RUL distributions')

    rul_distr_test = rul_distr(train, test, hi_tr, hi_te, number_of_workshops, number_of_components, viz=False)




