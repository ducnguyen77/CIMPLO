import mass_ts as mts
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
# import json
import re
import os


def rul_distr(train, test, hi_tr, hi_te, number_of_workshops, number_of_components, path):
    """

    :param number_of_components: number of workshops (int)
    :param number_of_workshops: number of components (int)
    :param train: train set (pandas)
    :param test: test set (pandas)
    :param hi_tr: HI of training units (dictionary. Keys:unit numbers,
    values: list of HI values)
    :param hi_te: HI of test units (dictionary. dictionary. Keys:unit numbers,
    values: list of HI values)
    :param path: path for output folder to save visualizations as .png
    :return: taskconfig.txt files
    """
    RUL_distr = {}

    for u in tqdm(test.unit.unique(), 'Creating the RUL distributions'):
        rul_pred = []
        max_test = test[test.unit == u].cycles.max()

        for unit in train.unit.unique():
            max_train = train[train.unit == unit].cycles.max()
            if max_train >= max_test:
                distances = mts.mass(hi_tr[unit].hi.values, hi_te[u].hi.values)

                if distances.any():
                    min_idx = np.argmin(distances)
                    rul = max_train - max_test - min_idx  # taking into account initial variation of machine condition
                    rul_pred.append(rul)

        # Interquantile range cleaning to remove outliers
        q1, q2, q3 = np.quantile(rul_pred, [0.25, 0.5, 0.75])
        IQ = q3 - q1
        rul_pred_ = [x for x in rul_pred if q1 - 1.5 * IQ < x < q3 + 1.5 * IQ]
        if rul_pred_:
            RUL_distr[u] = rul_pred_
        else:
            RUL_distr[u] = rul_pred

    # Writing to .txt file with a pre-defined structure (IMPORTANT)
    means = [np.mean(RUL_distr[u]) for u in RUL_distr.keys()]
    std = [np.std(RUL_distr[u]) for u in RUL_distr.keys()]
    means_and_stds = means+std

    means_and_stds = (re.sub(r'[][,]', '', str(means_and_stds))).split(' ')

    with open(str(path)+'/taskconfig.txt', 'w') as f:
        f.write(str(len(test.unit.unique()))+' '+str(number_of_components)+' '+str(number_of_workshops)+'\n')
        f.write('Due dates \n')
        for item in means_and_stds[:100]:
            f.write("%s\n" % item)

        f.write('Standard deviation \n')
        for item in means_and_stds[100:]:
            f.write("%s\n" % item)

    if path:
        for test_unit in test.unit.unique():
            # plt.figure(figsize=(10, 10))
            fig, ax = plt.subplots()
            # bins = int(np.ceil((np.max(RUL_distr[test_unit]) - np.min(RUL_distr[test_unit]))/1))
            n, bins, patches = plt.hist(x=RUL_distr[test_unit], bins='auto', density=True, color='#0504aa',
                                        alpha=0.7, rwidth=0.85)

            temp_df = pd.DataFrame({'RUL': RUL_distr[test_unit]})
            try:
                temp_df.RUL.plot.kde(ax=ax)
            except np.linalg.LinAlgError as err:
                print(f'unit {test_unit} error {err}')

            plt.grid(axis='y', alpha=0.3)
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            plt.title(f'Predicted RUL distribution for unit {test_unit}')
            plt.legend()
            plt.savefig(str(path)+'/rul_distribution_unit'+str(test_unit))
