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
import seaborn as sns

feature_cols = ('LeadTimeInterval', 'ArrivalMonth', 'NumWeekendNights', 'NumWeekNights', 'RoomType', 'NumAdults',
                'NumChildren', 'MarketSegment', 'NumPrevCancellations', 'AvgRoomPrice', 'SpecialRequests')

room_types = ('Room_Type 1', 'Room_Type 2', 'Room_Type 4', 'Room_Type 6', 'Room_Type 7', 'Room_Type 5', 'Room_Type 3')

market_segment = ('Online', 'Offline', 'Corporate', 'Complementary')


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


# Create a dataframe out of the trainingdata.csv file
df = pd.read_csv('trainingdata.csv')

# Replace all string data with numeric values

df['RoomType'] = get_numeric_value(df['RoomType'])

df['MarketSegment'] = get_numeric_value(df['MarketSegment'])

df['BookingStatus'] = get_numeric_value(df['BookingStatus'])

# Remove parking, arrival year, repeated guest, arrival year (PREDICT BOOKING STATUS)
df.drop(['Parking'], axis=1, inplace=True)
df.drop(['MealPlan'], axis=1, inplace=True)
df.drop(['RepeatedGuest'], axis=1, inplace=True)
df.drop(['ArrivalYear'], axis=1, inplace=True)

# Set the leadtime to intervals to make testing quicker
bins = [0, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480]
labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

df['LeadTime'] = pd.cut(df['LeadTime'], bins=bins, labels=labels, include_lowest=True)
df.rename(columns={'LeadTime': 'LeadTimeInterval'}, inplace=True)
pd.set_option('display.max_columns', None)
print(df.head(10))

# Create X features

X = df.loc[:, feature_cols]
print(X.shape)

# Create Y responses
Y = df.BookingStatus
print(Y.shape)

# Make scikit model
logreg = LogisticRegression(max_iter=7254)
print(logreg.fit(X, Y))

# Get the test Data
# Create a dataframe out of the testdata.csv file
test = pd.read_csv('testdata.csv')

# Change the string values to numerical Values
test['RoomType'] = get_numeric_value(test['RoomType'])
test['MarketSegment'] = get_numeric_value(test['MarketSegment'])
test['BookingStatus'] = get_numeric_value(test['BookingStatus'])

# Make the prices in intervals instead of set values
bins = [0, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480]
labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
test['LeadTime'] = pd.cut(test['LeadTime'], bins=bins, labels=labels, include_lowest=True)
test.rename(columns={'LeadTime': 'LeadTimeInterval'}, inplace=True)

# New X features for test data
X_new = test.loc[:, feature_cols]
print(X_new.shape)

# Predict the values
new_pred_class = logreg.predict(X_new)
test_data = pd.DataFrame({'BookingStatus': new_pred_class})
test_data.to_csv('results.csv')
print("------------------------------------------------------------")
print(f"Training Value: {df['BookingStatus'].sum()}")
print(f"Predicted Cancellations: {test_data['BookingStatus'].sum()}")

# Fill the BookingStatus coloumn with the predicted values
test['BookingStatus'] = test_data['BookingStatus']

# Create Graphs
for col in feature_cols:
    graph = sns.regplot(data=test, x=col, y='BookingStatus', logistic=True)
    graph.set_yticks([0, 1])
    graph.set_yticklabels(['Canceled', 'Not_Canceled'])

    # Add string labels to values that were replaced with integers
    if col == 'RoomType':
        graph.set_xticks([0, 1, 2, 3, 4, 5, 6])
        graph.set_xticklabels(room_types)
    elif col == 'MarketSegment':
        graph.set_xticks([0, 1, 2, 3])
        graph.set_xticklabels(market_segment)

    plt.show()

# Change predicted values from numerical values back to string values
test['RoomType'] = test['RoomType'].replace({0: room_types[0], 1: room_types[1], 2: room_types[2], 3: room_types[3], 4: room_types[4], 5: room_types[5], 6: room_types[6]})
test['MarketSegment'] = test['MarketSegment'].replace({0: market_segment[0], 1: market_segment[1], 2: market_segment[2], 3: market_segment[3]})
test['BookingStatus'] = test['BookingStatus'].replace({1: 'Not_Canceled', 0: "Canceled"})

# Save the dataframe into a csv file
test.to_csv('team_18.csv')
