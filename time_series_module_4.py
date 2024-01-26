# -*- coding: utf-8 -*-
"""Time Series_module_4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t22MUJV3f7NZn-0dNW8i4LNIDCSzBZo-
"""

import pandas as pd
from google.colab import drive

drive.mount('/content/drive')
file_path = ('/content/drive/MyDrive/MASTER_DATA/Data_Application /Modulo4/CO2_rev.csv')

# Load the data
data = pd.read_csv(file_path)

data.head()

data['ti'] = (data.index + 0.5) / 12

data

data.columns

from sklearn.model_selection import train_test_split

# Clean the data by dropping missing values
data_cleaned = data[data.iloc[:, 4] != -99.99]

# Correct column name for CO2
data_cleaned.rename(columns={'     CO2': 'CO2'}, inplace=True)

# Keep only the 'CO2' and 'ti' columns
data_cleaned = data_cleaned[[' Mn', 'CO2', 'ti']]

# Split the data into training and test sets (80:20 split)
train_data, test_data = train_test_split(data_cleaned, test_size=0.2, shuffle=False)  # Set shuffle to False for chronological split

data_cleaned

data_cleaned.columns

# Calculate the index for splitting (80% for training, 20% for testing)
split_index = int(0.8 * len(data_cleaned))

# Split the data into training and test sets
train_data = data_cleaned.iloc[:split_index, :]
test_data = data_cleaned.iloc[split_index:, :]

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Fit the simple linear model F1(t) ~ α0 + α1t using training data
model = LinearRegression()
model.fit(train_data[['ti']], train_data['CO2'])

alpha0 = model.intercept_
alpha1 = model.coef_[0]

print(alpha0)
print(alpha1)

# Plot the data and the fit
plt.figure(figsize=(10, 6))
plt.scatter(train_data['ti'], train_data['CO2'], label='Training Data')
plt.scatter(test_data['ti'], test_data['CO2'], label='Test Data')
plt.plot(train_data['ti'], model.predict(train_data[['ti']]), label=f'F1(t) = {alpha0:.2f} + {alpha1:.2f}t - Training')
plt.plot(test_data['ti'], model.predict(test_data[['ti']]), label=f'F1(t) - Test')
plt.xlabel('ti')
plt.ylabel('CO2 Concentration')
plt.legend()
plt.show()

# Calculate residuals for the training data
residuals_train = train_data['CO2'] - model.predict(train_data[['ti']])

# Plot the residuals for the training data
plt.scatter(train_data['ti'], residuals_train, label='Residuals - Training Data')
plt.axhline(y=0, color='red', linestyle='--', label='Zero Residual Line')
plt.xlabel('ti')
plt.ylabel('Residuals')
plt.legend()
plt.title('Residuals Plot for Training Data')
plt.show()

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error

# Calculate predictions for the test set
predictions_test = model.predict(test_data[['ti']])

# Calculate RMSE (Root Mean Squared Error) on the test set
rmse_test = np.sqrt(mean_squared_error(test_data['CO2'], predictions_test))
print(f'Root Mean Squared Error (RMSE) on Test Set: {rmse_test}')

# Calculate MAPE (Mean Absolute Percentage Error) on the test set
mape_test = mean_absolute_percentage_error(test_data['CO2'], predictions_test) * 100
print(f'Mean Absolute Percentage Error (MAPE) on Test Set: {mape_test:.6f}%')

# Fit the quadratic model F2(t) ~ α0 + α1*t + α2*t^2
quad_model = np.polyfit(train_data['ti'], train_data['CO2'], deg=2)
quad_predictions_train = np.polyval(quad_model, train_data['ti'])
quad_predictions_test = np.polyval(quad_model, test_data['ti'])

# Extract coefficients
alpha0, alpha1, alpha2 = quad_model
print(f'Alpha 2: {alpha0:.6f}')
print(f'Alpha 1: {alpha1:.6f}')
print(f'Alpha 0: {alpha2:.6f}')

# Calculate residuals for the training data using quadratic predictions
quad_residuals_train = train_data['CO2'] - quad_predictions_train

# Plot the residuals for the quadratic model
plt.figure(figsize=(10, 6))
plt.scatter(train_data['ti'], quad_residuals_train, label='Residuals - Quadratic Model')
plt.axhline(y=0, color='red', linestyle='--', label='Zero Residual Line')
plt.xlabel('ti')
plt.ylabel('Residuals')
plt.legend()
plt.title('Residuals Plot for Quadratic Model (Training Data)')
plt.show()

# Calculate RMSE (Root Mean Squared Error) on the test set for the quadratic model
rmse_quad_test = np.sqrt(mean_squared_error(test_data['CO2'], quad_predictions_test))
print(f'Root Mean Squared Error (RMSE) on Test Set (Quadratic Model): {rmse_quad_test:.6f}')

# Calculate MAPE (Mean Absolute Percentage Error) on the test set for the quadratic model
mape_quad_test = mean_absolute_percentage_error(test_data['CO2'], quad_predictions_test) * 100
print(f'Mean Absolute Percentage Error (MAPE) on Test Set (Quadratic Model): {mape_quad_test:.6f}%')

# Fit the cubic model F3(t) ~ γ0 + γ1*t + γ2*t^2 + γ3*t^3
cubic_model = np.polyfit(train_data['ti'], train_data['CO2'], deg=3)

# Extract coefficients
gamma3, gamma2, gamma1, gamma0 = cubic_model
print(f'Gamma 3: {gamma3:.6f}')
print(f'Gamma 2: {gamma2:.6f}')
print(f'Gamma 1: {gamma1:.6f}')
print(f'Gamma 0: {gamma0:.6f}')

# Calculate residuals for the training data using cubic predictions

cubic_predictions_train = np.polyval(cubic_model, train_data['ti'])
cubic_residuals_train = train_data['CO2'] - cubic_predictions_train

# Plot the residuals for the cubic model on the training data
plt.figure(figsize=(10, 6))
plt.scatter(train_data['ti'], cubic_residuals_train, label='Residuals - Cubic Model')
plt.axhline(y=0, color='red', linestyle='--', label='Zero Residual Line')
plt.xlabel('ti')
plt.ylabel('Residuals')
plt.legend()
plt.title('Residuals Plot for Cubic Model (Training Data)')
plt.show()

from sklearn.metrics import mean_squared_error

# Calculate predictions for the test set using the cubic model
cubic_predictions_test = np.polyval(cubic_model, test_data['ti'])

# Calculate RMSE (Root Mean Squared Error) on the test set for the cubic model
rmse_cubic_test = np.sqrt(mean_squared_error(test_data['CO2'], cubic_predictions_test))
print(f'Root Mean Squared Error (RMSE) on Test Set (Cubic Model): {rmse_cubic_test:.6f}')

# Calculate MAPE (Mean Absolute Percentage Error) on the test set for the cubic model
mape_cubic_test = mean_absolute_percentage_error(test_data['CO2'], cubic_predictions_test) * 100
print(f'Mean Absolute Percentage Error (MAPE) on Test Set (Cubic Model): {mape_cubic_test:.6f}%')

# Add the residuals column to the training dataset
train_data['Residuals'] = quad_residuals_train

train_data

# Calculate average residuals by month
average_residuals_by_month = train_data.groupby(' Mn')['Residuals'].mean()

# Display the result
print(average_residuals_by_month)

file_path_2 = '/content/drive/MyDrive/MASTER_DATA/Data_Application /Modulo4/CPI.csv'

# Load the data
CPI = pd.read_csv(file_path_2)

# Convert the 'DATE' column to datetime format
CPI['DATE'] = pd.to_datetime(CPI['date'])

# Set the 'DATE' column as the index
CPI.set_index('DATE', inplace=True)

# Plot the monthly CPI values as a time series
plt.plot(CPI.resample('M').mean(), label='Monthly CPI')
plt.title('Monthly CPI Time Series')
plt.xlabel('Date')
plt.ylabel('CPI Value')
plt.legend()
plt.show()

CPI

CPI.columns

import numpy as np
from sklearn.linear_model import LinearRegression

# Assuming CPI is the DataFrame containing CPI data with 'DATE' as the index
# Make sure the 'DATE' column is in datetime format and the index is set

# Resample the data to monthly frequency and take the first value of each month
monthly_cpi = CPI.resample('M').first()

# Filter the training data (months prior to and not including September 2013)
train_data = monthly_cpi[monthly_cpi.index < '2013-09-01']

# Create a time variable 't' for linear regression as the number of months from the start of the dataset
train_data['t'] = ((train_data.index - train_data.index[0]).days // 30) + 1

# Fit a linear trend Tt = α1t + α0
model = LinearRegression()
model.fit(train_data[['t']], train_data['CPI'])

# Extract the coefficients
alpha1 = model.coef_[0]
alpha0 = model.intercept_

# Print the coefficients
print(f'Linear Trend Coefficients:')
print(f'  Alpha 1: {alpha1:.6f}')
print(f'  Alpha 0: {alpha0:.6f}')

# Subtract the linear trend from the training data to get the residuals Rt
train_data['Residuals'] = train_data['CPI'] - (alpha1 * train_data['t'] + alpha0)

# Visualize the residuals Rt
plt.plot(train_data.index, train_data['Residuals'], label='Residuals')
plt.title('Residuals (Rt) after Subtracting Linear Trend')
plt.xlabel('Date')
plt.ylabel('Residuals')
plt.legend()
plt.show()

# Report the maximum absolute value of the residuals over the training data
max_absolute_residual = np.max(np.abs(train_data['Residuals']))
print(f'Maximum Absolute Value of Residuals: {max_absolute_residual:.6f}')

import statsmodels.api as sm
import statsmodels.graphics.tsaplots as tsaplots

residuals = train_data['Residuals'].dropna()  # Drop any NaN values if present

# Plot the autocorrelation function (ACF) and partial autocorrelation function (PACF)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# ACF plot
tsaplots.plot_acf(residuals, lags=20, ax=ax1)
ax1.set_title('Autocorrelation Function (ACF) of Residuals')

# PACF plot
tsaplots.plot_pacf(residuals, lags=20, ax=ax2)
ax2.set_title('Partial Autocorrelation Function (PACF) of Residuals')

plt.show()

CPI

test_data = monthly_cpi[monthly_cpi.index >= '2013-09-01']
test_data

import statsmodels.api as sm

# Specify the lag order (p)
p = 2

# Fit AR(2) model
ar_model = sm.tsa.AutoReg(train_data['Residuals'].dropna(), lags=p, trend='c')  # 'c' for constant term
ar_results = ar_model.fit()

# Extract coefficients
coefficients = ar_results.params

# Display the coefficients
print(f'Coefficients:\n{coefficients}')

# Filter the data for validation starting from September 2013
validation_data = CPI[CPI.index >= '2013-09-01']

# Generate the time variable 't' for the validation data
validation_data['t'] = np.arange(1, len(validation_data) + 1)

# Fit the linear trend to the validation data
validation_data['Linear_Trend'] = alpha1 * validation_data['t'] + alpha0

# Make predictions for the AR(2) model on the validation data
validation_data['AR_Predictions'] = ar_results.predict(start=len(train_data), end=len(train_data) + len(validation_data) - 1)

# Combine the linear trend and AR predictions to get the final model predictions
validation_data['Final_Predictions'] = validation_data['Linear_Trend'] + validation_data['AR_Predictions']

# Plot the actual CPI and the final model predictions
plt.figure(figsize=(10, 6))
plt.plot(validation_data.index, validation_data['CPI'], label='Actual CPI', marker='o', linestyle='-', color='b')
plt.plot(validation_data.index, validation_data['Final_Predictions'], label='Final Model Predictions', marker='o', linestyle='-', color='r')
plt.title('Actual CPI vs Final Model Predictions')
plt.xlabel('Time')
plt.ylabel('CPI')
plt.legend()
plt.show()

# Calculate the monthly inflation rate
CPI['Inflation Rate'] = (CPI['CPI'] - CPI['CPI'].shift(1)) / CPI['CPI'].shift(1) * 100

# Plot the monthly inflation rate
plt.figure(figsize=(10, 6))
plt.plot(CPI['Inflation Rate'], label='Monthly Inflation Rate')
plt.title('Monthly Inflation Rate Over Time')
plt.xlabel('Date')
plt.ylabel('Inflation Rate (%)')
plt.legend()
plt.show()

# Report the value for February 2013
inflation_rate_feb_2013 = CPI.loc['2013-02-01', 'Inflation Rate']
print(f'Inflation Rate for February 2013: {inflation_rate_feb_2013:.2f}%')

# Calculate the monthly inflation rate using logarithmic formula
CPI['Log Inflation Rate'] = np.log(CPI['CPI']) - np.log(CPI['CPI'].shift(1))

# Plot the monthly inflation rate
plt.figure(figsize=(10, 6))
plt.plot(CPI['Log Inflation Rate'], label='Log Monthly Inflation Rate')
plt.title('Log Monthly Inflation Rate Over Time')
plt.xlabel('Date')
plt.ylabel('Log Inflation Rate')
plt.legend()
plt.show()

# Report the value for February 2013
log_inflation_rate_feb_2013 = CPI.loc['2013-02-01', 'Log Inflation Rate']
print(f'Log Inflation Rate for February 2013: {log_inflation_rate_feb_2013:.6f}')

0.002953*100

file_path_3 = '/content/drive/MyDrive/MASTER_DATA/Data_Application /Modulo4/T10YIE.csv'

# Load the data
BER = pd.read_csv(file_path_3)

BER['DATE'] = pd.to_datetime(BER['DATE'])
BER.set_index('DATE', inplace=True)

BER

# Convert BER values from percentages to rates
BER['BER Rate'] = BER['T10YIE'] / 100.0

# Calculate the average BER for each month
average_BER_per_month = BER.resample('M').mean()

# Deannualize the monthly BER to get the monthly inflation rate
average_BER_per_month['Inflation Rate'] = (average_BER_per_month['BER Rate'] + 1) ** (1/12) - 1

# Report the monthly inflation rate for February 2013
inflation_rate_feb_2013 = average_BER_per_month.loc['2013-02-28', 'Inflation Rate']
print(f'Monthly Inflation Rate for February 2013: {inflation_rate_feb_2013:.6f}')

0.002104 * 100

data

data.columns

data_cleaned

from scipy.interpolate import interp1d

# with 'Mn' and 'CO2' columns
months = data_cleaned[' Mn']
co2_values = data_cleaned['CO2']

# Calculate average values for each month
average_co2_values = [co2_values[months == month].mean() for month in range(1, 13)]

# Create an interpolation function
interp_function = interp1d(range(1, 13), average_co2_values, kind='quadratic', fill_value='extrapolate')

# Generate points for smoother plotting
interp_months = np.linspace(1, 12, 1000)
interp_co2_values = interp_function(interp_months)

# Plot the original data points and the interpolated curve
plt.scatter(range(1, 13), average_co2_values, label='Monthly average', color='blue')
plt.plot(interp_months, interp_co2_values, label='Interpolated Curve', color='red')
plt.xlabel('Month')
plt.ylabel('CO2')
plt.title('Interpolated Periodic Signal')
plt.legend()
plt.show()

all_data = data[data.iloc[:, 4] != -99.99]
train_data = data_cleaned.iloc[:split_index, :]
test_data = data_cleaned.iloc[split_index:, :]

all_data

all_data.columns

test_data

quad_model = np.polyfit(train_data['ti'], train_data['CO2'], deg=2)

# Extract coefficients
alpha0, alpha1, alpha2 = quad_model
print(f'Alpha 2: {alpha0:.6f}')
print(f'Alpha 1: {alpha1:.6f}')
print(f'Alpha 0: {alpha2:.6f}')

# Calculate predictions for the test set using the quadratic model
all_data['quad'] = np.polyval(quad_model, all_data['ti'])

all_data

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Create a DataFrame for average residuals
average_residuals_by_month = pd.DataFrame({'Mn': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                           'Residuals': [-0.012919, 0.646407, 1.355569, 2.561858, 2.982891, 2.316473, 0.776297, -1.301213, -3.128074, -3.309520, -2.081487, -0.921507]})

# Calculate the periodic signal Pi for each month
average_residuals_interp = interp1d(average_residuals_by_month['Mn'], average_residuals_by_month['Residuals'], kind='quadratic', fill_value='extrapolate')
all_data['periodic_signal'] = average_residuals_interp(all_data[' Mn'])

# Calculate the final fit Fn(t) + Pi
all_data['final fit'] = all_data['quad'] + all_data['periodic_signal'] # all_data['AR_predictions'] +

# Extract the year from the 'ti' column
all_data['year'] = pd.to_datetime(all_data['ti']).dt.year

# Plot the final fit on top of the entire time series
plt.figure(figsize=(10, 6))
plt.plot(all_data['ti'], all_data['     CO2'], label='Actual Data')
plt.plot(all_data['ti'], all_data['final fit'], label='Final Fit (Fn(t) + Pi)')
plt.scatter(train_data['ti'], train_data['CO2'], label='Training Data', color='red')
plt.scatter(test_data['ti'], test_data['CO2'], label='Testing Data', color='green')
plt.xlabel('Year')
plt.ylabel('CO2 Levels')
plt.legend()
plt.title('Final Fit of the Model with Periodic Signal')
plt.show()

test_data

from sklearn.metrics import mean_squared_error, mean_absolute_error

test_data['quad'] = np.polyval(quad_model, test_data['ti'])
test_data['periodic_signal'] = average_residuals_interp(test_data[' Mn'])

test_data['final fit'] = test_data['quad'] + test_data['periodic_signal']

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(test_data['CO2'], test_data['final fit']))

# Calculate MAPE
mape = np.mean(np.abs((test_data['CO2'] - test_data['final fit']) / test_data['CO2'])) * 100

# Print the results
print(f'Root Mean Squared Error (RMSE): {rmse:.4f}')
print(f'Mean Absolute Percentage Error (MAPE): {mape:.4f}%')

# Calculate the range of values of F and amplitude of Pi
range_F = all_data['final fit'].max() - all_data['final fit'].min()
amplitude_Pi = average_residuals_by_month['Residuals'].max() - average_residuals_by_month['Residuals'].min()

# Calculate the range of residuals Ri (after removing trend and periodic signal)
residuals = all_data['     CO2'] - all_data['final fit']
range_Ri = residuals.max() - residuals.min()

# Calculate the specified ratios
ratio_F_P = range_F / amplitude_Pi
ratio_P_R = amplitude_Pi / range_Ri

# Print the ratios
print(f'Ratio of F Range to Pi Amplitude: {ratio_F_P:.4f}')
print(f'Ratio of Pi Amplitude to Ri Range: {ratio_P_R:.4f}')