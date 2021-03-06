# Import libraries necessary for this project
import numpy as np
import pandas as pd
import renders as rs
from IPython.display import display # Allows the use of display() for DataFrames

# # Show matplotlib plots inline (nicely formatted in the notebook)
# %matplotlib inline

# Load the wholesale customers dataset
try:
    data = pd.read_csv("customers.csv")
    data.drop(['Region', 'Channel'], axis = 1, inplace = True)
    print "Wholesale customers dataset has {} samples with {} features each.".format(*data.shape)
except:
    print "Dataset could not be loaded. Is the dataset missing?"

display(data.describe())

# TODO: Select three indices of your choice you wish to sample from the dataset
indices = [2,220,178]

# Create a DataFrame of the chosen samples
samples = pd.DataFrame(data.loc[indices], columns = data.keys()).reset_index(drop = True)
print "Chosen samples of wholesale customers dataset:"
display(samples)
display(samples.sum())

from sklearn.cross_validation import train_test_split
from sklearn import tree
# TODO: Make a copy of the DataFrame, using the 'drop' function to drop the given feature
new_data = pd.read_csv("customers.csv")
new_data.drop(['Region', 'Channel'], axis = 1, inplace = True)
y_data = new_data['Delicatessen']
new_data.drop(['Delicatessen'], axis = 1, inplace = True)


# TODO: Split the data into training and testing sets using the given feature as the target
X_train, X_test, y_train, y_test = train_test_split(new_data, y_data, test_size=0.25, random_state=42)	

# TODO: Create a decision tree regressor and fit it to the training set
regressor = tree.DecisionTreeRegressor(random_state=42)

# TODO: Report the score of the prediction using the testing set
regressor = regressor.fit(X_train,y_train)
regressor.score(X_test, y_test)  

print regressor.score(X_test, y_test)  

# TODO: Scale the data using the natural logarithm
log_data = np.log(data)

# TODO: Scale the sample data using the natural logarithm
log_samples = np.log(samples)

# Produce a scatter matrix for each pair of newly-transformed features
pd.scatter_matrix(log_data, alpha = 0.3, figsize = (14,8), diagonal = 'kde');

# OPTIONAL: Select the indices for data points you wish to remove
outliers  = [];

# For each feature find the data points with extreme high or low values
for feature in log_data.keys():
    
    # TODO: Calculate Q1 (25th percentile of the data) for the given feature
    Q1, Q3 = np.percentile(log_data[feature], [25 ,75])
    iqr = Q3-Q1
    
    # TODO: Calculate Q3 (75th percentile of the data) for the given feature
    #Q3 = None
    
    # TODO: Use the interquartile range to calculate an outlier step (1.5 times the interquartile range)
    step = 1.5*iqr
    
    # Display the outliers
    print "Data points considered outliers for the feature '{}':".format(feature)
    #display(log_data[~((log_data[feature] >= Q1 - step) & (log_data[feature] <= Q3 + step))])
    outlierVals = log_data[~((log_data[feature] >= Q1 - step) & (log_data[feature] <= Q3 + step))].index
    for val in outlierVals:outliers.append(val)
    
print outliers

# Remove the outliers, if any were specified
good_data = log_data.drop(log_data.index[outliers]).reset_index(drop = True)

completedOutliers=[];
for ii, val in enumerate(outliers):
	if val not in completedOutliers:
		for jj, check in enumerate(outliers):
			if ii != jj and val == check:
				print val
		completedOutliers.append(val)