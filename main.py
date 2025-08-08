import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data = pd.read_csv('housing.csv')
data.dropna(inplace=True)

X = data.drop(['median_house_value'], axis=1)
y = data['median_house_value']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

train_data = X_train.join(y_train)

# train_data.hist(figsize=(12, 8)) # this will plot the chart
# plt.tight_layout()
# plt.show() # this shows the plotted chart

# # sns.heatmap(train_data.corr())

# plt.figure(figsize=(12, 8))
# sns.heatmap(train_data.corr(), annot=True, cmap='YlGnBu')
# plt.show()

# print(train_data.ocean_proximity.value_counts())
# print('--------------------------------')
# print(train_data['ocean_proximity'].value_counts()) 

train_data = train_data.join(pd.get_dummies(train_data['ocean_proximity'])).drop(['ocean_proximity'], axis=1)
# plt.figure(figsize=(15, 8))
# sns.heatmap(train_data.corr(), annot=True, cmap='YlGnBu')
# plt.show()

# plt.figure(figsize=(15, 8))
# sns.scatterplot(x='longitude', y='latitude', hue='median_house_value', data=train_data, palette='coolwarm')
# plt.show()

train_data['bedroom_ratio'] = train_data['total_bedrooms'] / train_data['total_rooms']
train_data['household_rooms'] = train_data['total_rooms'] / train_data['households']

# plt.figure(figsize=(15, 8))
# sns.heatmap(train_data.corr(), annot=True, cmap='YlGnBu')
# plt.show()

X_train, y_train = train_data.drop(['median_house_value'], axis=1), train_data['median_house_value']
reg = LinearRegression()

reg.fit(X_train, y_train)

test_data = X_test.join(y_test)

test_data['total_rooms'] = np.log(test_data['total_rooms'] + 1)
test_data['total_bedrooms'] = np.log(test_data['total_bedrooms'] + 1)
test_data['population'] = np.log(test_data['population'] + 1)
test_data['households'] = np.log(test_data['households'] + 1)

test_data = test_data.join(pd.get_dummies(test_data['ocean_proximity'])).drop(['ocean_proximity'], axis=1)
test_data['bedroom_ratio'] = test_data['total_bedrooms'] / test_data['total_rooms']
test_data['household_rooms'] = test_data['total_rooms'] / test_data['households']

print(test_data)