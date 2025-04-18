import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the dataset
df = pd.read_csv('states_population1.csv')

# Drop rows with missing values
df = df.dropna()

# Print the first few rows of the dataframe
print(df.head())

# Display info about the dataset
print("\nDataset Info:")
df.info()

# Check for any null values
print("\nMissing values in dataset:")
print(df.isnull().sum())

# Visualizing median household income over years for selected states
states = {'Iowa', 'Michigan', 'Kentucky', 'Missouri', 'Indiana', 'Wisconsin'}

for state in states:
    state_df = df[df['NAME'] == state]
    sns.lineplot(data=state_df, x='YEAR', y='median_household_income_past12months', label=state)

plt.title('Median Household Income Over Years')
plt.xlabel('Year')
plt.ylabel('Median Household Income (USD)')
plt.legend(title='State')
plt.show()

# Visualizing population growth rate over years for selected states
for state in states:
    state_df = df[df['NAME'] == state]
    state_df = state_df.sort_values('YEAR')
    state_df['Growth Rate (%)'] = state_df['total_population'].pct_change() * 100

    sns.lineplot(data=state_df, x='YEAR', y='Growth Rate (%)', label=state)

plt.title('Population Growth Rate Over Years for Selected States')
plt.xlabel('Year')
plt.ylabel('Population Growth Rate (%)')
plt.legend(title='State')
plt.show()

# Prepare data for linear regression model
X = df[['total_population']]  # Predictor variable: total population
y = df['median_gross_rent_in_dollars']  # Target variable: median rent in dollars

# Split the data into training and testing sets (67% train, 33% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

# Initialize the linear regression model
model = LinearRegression()

# Train the model on the training data
model.fit(X_train, y_train)

# Predict on the testing data
y_pred = model.predict(X_test)

# Calculate the Mean Squared Error of the model
mse = mean_squared_error(y_test, y_pred)
print(f"\nMean Squared Error: {mse:.2f}")

# Visualizing the predicted vs actual values for rent
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', lw=2)
plt.title('Actual vs Predicted Rent Prices')
plt.xlabel('Actual Rent Prices')
plt.ylabel('Predicted Rent Prices')
plt.show()

# Forecast future population growth
future_years = np.array([2025, 2026, 2027]).reshape(-1, 1)

# Predict future population based on the trained model
future_population = model.predict(future_years)

# Print the predicted population for the future years
print("\nPredicted Population Growth for the Next Years:")
for year, pop in zip(future_years.flatten(), future_population):
    print(f"Predicted population in {year}: {pop:.2f} million")

