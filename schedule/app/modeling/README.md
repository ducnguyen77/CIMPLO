# Idea:

-  We estimate the RUL through classification:
By choosing a lookback value (k), we label the k time-steps
prior to the EoL of the training units as faulty. We do this
so the learning algorithm learns any salient changes in the 
sensor values.

-  Using the trained model we use the probability of a time-step belonging
to the faulty class as the HI of that time-step. We do this for all units
of the train and test sets.

-  Afterwards, we match the HI trajectory of the test set to each HI of the train set
and estimate an RUL for each match. We end up with a distribution of RUL for the test set.
We repeat this for all test sets.

# Important Files
-	In the /modeling folder there are two types of files. The source codes (denoted by *.py*) and the /main.spec and /dist/ which contain the **Linux** executable of the *main.py* which is the *head* of the pipeline.

# Execution
The below example trains from scratch a model using */home/marios/Projects/CIMPLO_Platform/CIMPLO/sample_data_modeling/CMAPSS_1* as the data input location, */home/marios/Projects/CIMPLO_Platform/CIMPLO/modeling/output* as the output location where the results are saved [**Note:** *if the location does not exist, it creates it*]. It *drops* from training features *unit, cycles* and performs hyperparameter optimization of the model. Finally, it creates an output config file for the scheduling optimization with 3 workshops, 1 component and a lookback value of 25 [**Note:** The *lookback* value is problem specific.]

- Of the source code:
	- In terminal: *python<version_number> main.py -W 3 -C 1 -L 25 -P /home/marios/Projects/CIMPLO_Platform/CIMPLO/sample_data_modeling/CMAPSS_1 -OUT /home/marios/Projects/CIMPLO_Platform/CIMPLO/modeling/output -D unit -D cycles -F /home/marios/Desktop/Projects/CIMPLO_Platform/CIMPLO/sample_data_modeling/CMAPSS_1/features_list25_rep_1.pkl -O True*

	- To view the different options do: *python<version_number> main.py --help*

- Of the command line exectuable tool:
	- In terminal: *./dist/main/main -W 3 -C 1 -L 25 -P /home/marios/Projects/CIMPLO_Platform/CIMPLO/sample_data_modeling/CMAPSS_1 -OUT /home/marios/Projects/CIMPLO_Platform/CIMPLO/modeling/output -D unit -D cycles -F /home/marios/Desktop/Projects/CIMPLO_Platform/CIMPLO/sample_data_modeling/CMAPSS_1/features_list25_rep_1.pkl -O True*

	- 	- To view the different options do: *./dist/main/main  --help*


# Details
- The input data path is currently used in order to load *specific datasets*

- The program outputs a taskconfig.txt for the optimization module and the RUL distributions per unit (as a *.png*)

- **NOTE:** Currently the executable is only working for *Linux*, the reason being that it is *fitted* to the platform that generates it. In order to make it compatible with Windows and macOS then do the following:
	
	1)Downloand *pyinstaller*

	2) Run *pyinstaller main.py* on Windows or macOS

	3) Try to run it as an executable. If it failes telling you a package is missing you must help the *main.spec* file find them (see here why https://pyinstaller.readthedocs.io/en/stable/spec-files.html) then you must run *pyinstaller main.spec*

	4) I.e., I had to add the following in the respective field of the *.spec* file below:

             binaries=[('/home/marios/anaconda3/envs/CIMPLO/lib/libiomp5.so', '.')],
             hiddenimports=['scipy.special.cython_special', 'sklearn.neighbors._typedefs', 
             'sklearn.utils._cython_blas',   'sklearn.neighbors._quad_tree', 'sklearn.tree._utils'],_..


main.exe -W 3 -C 1 -L 25 -P "J:\repos\CimploGithub\sample_data_modeling\CMAPSS_1" -OUT J:\repos\CimploGithub\modeling\output -D unit -D cycles -F J:\repos\CimploGithub
   

# Requirements
-  Requirements.txt : enviroment requirements



