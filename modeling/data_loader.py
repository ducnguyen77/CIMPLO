import pandas as pd


def load_data(t=1):
    """
    This is just an example using the first dataset of
    CMAPSS.
    TODO: Update this function to a more general file picker
    :param t: dataset number
    :return: train and test sets
    """

    # Fetching data #
    train = pd.read_csv('../sample_data_modeling/CMAPSS_1/train_FD00' + str(t) + '.csv', parse_dates=False,
                        delimiter=" ", decimal=".",
                        header=None)
    test = pd.read_csv('../sample_data_modeling/CMAPSS_1/test_FD00' + str(t) + '.csv', parse_dates=False,
                       delimiter=" ", decimal=".",
                       header=None)

    train.drop(train.columns[[-1, -2]], axis=1, inplace=True)
    test.drop(test.columns[[-1, -2]], axis=1, inplace=True)

    cols = ['unit', 'cycles', 'op_setting1', 'op_setting2', 'op_setting3', 's1', 's2', 's3', 's4', 's5', 's6', 's7',
            's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21']
    train.columns = cols
    test.columns = cols

    return train, test
