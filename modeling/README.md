Idea:

We estimate the RUL through classification:
By choosing a lookback value (k), we label the k time-steps
prior to the EoL of the training units as faulty. We do this
so the learning algorithm learns any salient changes in the 
sensor values.

Using the trained model we use the probability of a time-step belonging
to the faulty class as the HI of that time-step. We do this for all units
of the train and test sets.

Afterwards, we match the HI trajectory of the test set to each HI of the train set
and estimate an RUL for each match. We end up with a distribution of RUL for the test set.
We repeat this for all test sets.

===========================================================================================

To run the modeling:

python main.py

===========================================================================================

1) The program outputs a taskconfig.txt for the optimization module.
2) There is already a trained model and selected features given for a quick check (these are in the /sample_data_modeling/CMAPSS-1/).
   There is also a taskconfig.txt output that has been already created.

===========================================================================================

Requirements.txt : enviroment requirements



