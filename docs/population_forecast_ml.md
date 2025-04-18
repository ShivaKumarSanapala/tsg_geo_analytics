
---

# Population Analysis and Forecasting

This project analyzes population data for various U.S. states and performs machine learning-based forecasting. The main tasks include:
1. Exploring population trends.
2. Visualizing the relationship between population and economic indicators (e.g., median household income).
3. Using a Linear Regression model to predict future population growth.

## Contents

- `population_analysis.py` – Python script that performs the data analysis and forecasting.
- `states_population1.csv` – The dataset containing the population and related statistics for different U.S. states.

## Requirements

To run this script, you will need to install the required Python libraries:

- **pandas**: For data manipulation and analysis.
- **numpy**: For numerical operations.
- **seaborn**: For statistical data visualization.
- **matplotlib**: For creating static, animated, and interactive visualizations.
- **scikit-learn**: For machine learning models, specifically Linear Regression.

You can install these libraries using `pip`:

```bash
pip install pandas numpy seaborn matplotlib scikit-learn
```

## Data Description

The dataset (`states_population1.csv`) contains information about the population of various U.S. states over multiple years, including demographic breakdowns (e.g., total population, under 5, under 18, 65 and over), median household income, and educational attainment levels for both men and women.

Sample columns in the dataset:
- `YEAR`: The year of the record.
- `NAME`: The name of the state.
- `total_population`: Total population of the state.
- `under_5`: Population under 5 years old.
- `under_18`: Population under 18 years old.
- `65_and_over`: Population over 65 years old.
- `female_population`: Female population in the state.
- `median_gross_rent_in_dollars`: Median rent price in the state.
- `median_household_income_past12months`: Median household income in the last 12 months.
- `male_bachelors_degree_25yrs_above`: Number of males aged 25 and above with a bachelor's degree.
- `female_bachelors_degree_25yrs_above`: Number of females aged 25 and above with a bachelor's degree.
- `state`: The numerical code representing the state.

## Script Overview

### Data Preprocessing and Analysis

1. **Load Dataset**: The script loads the dataset (`states_population1.csv`) into a pandas DataFrame and removes any rows with missing values using `.dropna()`.
   
2. **Exploratory Data Analysis (EDA)**:
   - The script displays basic information about the dataset (e.g., `df.info()`) and checks for missing values (`df.isnull().sum()`).
   - It visualizes trends in **Median Household Income** over the years for selected states (`Iowa`, `Michigan`, `Kentucky`, `Missouri`, `Indiana`, `Wisconsin`) using a line plot.
   - It also visualizes the **Population Growth Rate** for the same states.

### Machine Learning Model (Linear Regression)

1. **Linear Regression Model**:
   - The script creates a simple linear regression model to predict **Median Gross Rent** based on **Total Population**.
   - The dataset is split into training and testing sets using `train_test_split()`. The training set is used to train the model, and the testing set is used to evaluate its performance.
   - The model’s performance is evaluated using **Mean Squared Error (MSE)**.

2. **Future Population Prediction**:
   - The script forecasts future population growth for the years 2025, 2026, and 2027 based on the linear regression model.
   - The predicted populations are displayed for each of these years.

### Visualizations

- **Median Household Income Over Years**: Line plots showing the median household income for selected states over multiple years.
- **Population Growth Rate Over Years**: Line plots illustrating the population growth rate for the same states.
- **Actual vs Predicted Rent**: Scatter plot comparing the actual versus predicted rent values, with a red line showing the ideal fit.

### Forecasted Future Population

The script predicts future population growth for the years 2025, 2026, and 2027 using the trained linear regression model.

Example Output:
```
Predicted population in 2025: 5797457.93 million
Predicted population in 2026: 5826882.21 million
Predicted population in 2027: 5856306.50 million
```

## How to Run the Script

1. **Download the Dataset**:
   Ensure you have the `states_population1.csv` file in the same directory as the script.

2. **Set Up Python Environment**:
   Make sure you have Python 3 installed on your computer. You can download it from the official Python website: [python.org](https://www.python.org/downloads/).

3. **Install Dependencies**:
   Install the required Python libraries using `pip`:
   ```bash
   pip install pandas numpy seaborn matplotlib scikit-learn
   ```

4. **Run the Script**:
   Save the Python script as `population_analysis.py` and run it from the command line or terminal:
   ```bash
   python population_analysis.py
   ```

5. **Results**:
   - The script will display various line plots showing trends in income and population growth.
   - It will output the **Mean Squared Error** of the linear regression model.
   - It will predict future population values for 2025, 2026, and 2027.

## Example Output

After running the script, you will see visualizations for:
1. **Median Household Income Over Time**.
2. **Population Growth Rate Over Time**.
3. A plot comparing **Actual vs Predicted Rent Prices**.
4. The predicted population for the years 2025, 2026, and 2027.

The model's **Mean Squared Error** will also be displayed to assess the quality of the predictions.

## Conclusion

This project provides insights into U.S. state population trends and uses linear regression for forecasting future population growth. You can modify the code to analyze different states or use additional features from the dataset.

---
