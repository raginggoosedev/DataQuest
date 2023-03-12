import time
import pandas as pd
import numpy as np
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


# Function for replacing string data into numeric values
def get_numeric_value(datf):
    # Create list to store all different strings in the column
    items = []
    for i in range(len(datf)):
        if not datf[i] in items:
            # String is not in the list, add it at the end
            items.append(datf[i])

    for i in range(len(items)):
        # Replace string with index integer
        datf = datf.replace({items[i]: i})

    return datf


# Get the Dataframe
df = pd.read_csv('trainingdata.csv')

# Replace all string data with numeric values

df['RoomType'] = get_numeric_value(df['RoomType'])

df['MarketSegment'] = get_numeric_value(df['MarketSegment'])

df['BookingStatus'] = get_numeric_value(df['BookingStatus'])

#Remove parking, arrival year, repeated guest, arrival year (PREDICT BOOKING STATUS)
df.drop(['Parking'], axis=1, inplace = True)
df.drop(['MealPlan'], axis=1, inplace = True)
df.drop(['RepeatedGuest'], axis=1, inplace = True)
df.drop(['ArrivalYear'], axis=1, inplace = True)

#Replace Adults and Children with number of guests and whether they have children or not
df['NumAdults'] = df[['NumAdults', 'NumChildren']].sum(axis=1)
df['NumChildren'] = np.where(df['NumChildren'] > 0, 1, 0)
df.rename(columns={'NumAdults': 'NumberOfGuests'}, inplace=True)
df.rename(columns={'NumChildren': 'HasChildren'}, inplace=True)

#Set the leadtime to intervals to make testing quicker
bins = [0, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480]
labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

df['LeadTime'] = pd.cut(df['LeadTime'], bins=bins, labels=labels, include_lowest=True)
df.rename(columns={'LeadTime': 'LeadTimeInterval'}, inplace=True)
pd.set_option('display.max_columns', None)
print(df.head(10))

#Create X features
feature_cols = ['LeadTimeInterval', 'ArrivalMonth', 'NumWeekendNights', 'NumWeekNights', 'RoomType', 'NumberOfGuests', 'HasChildren', 'MarketSegment', 'NumPrevCancellations', 'AvgRoomPrice', 'SpecialRequests']
X = df.loc[:, feature_cols]
print(X.shape)

#Create Y responses
Y = df.BookingStatus
print(Y.shape)

#Make scikit model
logreg = LogisticRegression(max_iter=30000)
print(logreg.fit(X, Y))

#Get the test Data
test = pd.read_csv('trainingdata.csv')
test['NumAdults'] = test[['NumAdults', 'NumChildren']].sum(axis=1)
test['NumChildren'] = np.where(test['NumChildren'] > 0, 1, 0)
test.rename(columns={'NumAdults': 'NumberOfGuests'}, inplace=True)
test.rename(columns={'NumChildren': 'HasChildren'}, inplace=True)
test['RoomType'] = get_numeric_value(test['RoomType'])

test['MarketSegment'] = get_numeric_value(test['MarketSegment'])

test['BookingStatus'] = get_numeric_value(test['BookingStatus'])

bins = [0, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480]
labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
test['LeadTime'] = pd.cut(test['LeadTime'], bins=bins, labels=labels, include_lowest=True)
test.rename(columns={'LeadTime': 'LeadTimeInterval'}, inplace=True)

#New X features for test data
X_new = test.loc[:, feature_cols]
print(X_new.shape)

#Predict the values
new_pred_class = logreg.predict(X_new)
test_data = pd.DataFrame({'BookingStatus': new_pred_class})
test_data.to_csv('results.csv')
print("------------------------------------------------------------")
print(f"Training Value: {df['BookingStatus'].sum()}")
print(f"Predicted Cancellations: {test_data['BookingStatus'].sum()}")
