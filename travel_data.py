import pandas as pd
import re

# File path
file_path = "/Users/alialnaimi/VS Code_projects/Travel_Cost_TFL/2025/Monzo Data Export - CSV (Wednesday, March 12th, 2025).csv"

# Read the CSV file
data = pd.read_csv(file_path)

# Filter the rows where the "Name" column is "Transport for London"
filtered_data = data[data['Name'] == 'Transport for London'].copy()  # Use .copy() to avoid warnings

# Days worked by month (this is where you define the days worked)
days_worked = {
    "Dec": [15, 18, 19, 21, 26, 28, 31],
    "Jan": [1, 4, 5, 9, 11, 14, 16, 18, 20, 21, 24, 25, 26, 27, 31],
    "Feb": [1, 3, 6, 7, 10, 11, 13, 14, 15, 17, 20, 21, 24, 26, 27, 28],
    "Mar": [1, 3, 6, 7, 9, 10, 11]
}

# Initialize a list to store unmatched days
unmatched_days = []

# Function to extract the day, month, and weekday from the Notes and #tags column
def extract_day_month_weekday(notes):
    # Use regular expression to find patterns like 'Thursday, 1 Aug'
    match = re.search(r'(\w+),\s*(\d{1,2})\s*(\w+)', str(notes))
    if match:
        weekday = match.group(1)
        day = int(match.group(2))
        month = match.group(3)
        return weekday, day, month
    return None, None, None  # Return None if no match is found

# Extract the day, month, and weekday from the Notes column
filtered_data['Weekday'], filtered_data['Day'], filtered_data['Month'] = zip(*filtered_data['Notes and #tags'].apply(extract_day_month_weekday))

# Convert Day to integer, handling NaN values
filtered_data['Day'] = pd.to_numeric(filtered_data['Day'], errors='coerce').astype('Int64')

# Check for any rows where the date could not be extracted (invalid date descriptions)
invalid_dates = filtered_data[filtered_data['Day'].isna() | filtered_data['Month'].isna()]

# If there are invalid dates, warn the user
if not invalid_dates.empty:
    print("Warning: Some rows have invalid date descriptions and were excluded.")
    print(invalid_dates)

# Filter data based on the worked days
def is_worked_day(row):
    month = row['Month']
    day = row['Day']
    if pd.notna(day) and month in days_worked:
        if int(day) in days_worked[month]:
            return True
        else:
            unmatched_days.append((row['Weekday'], int(day), month))  # Collect unmatched days for reference
    return False

# Apply the filter
final_filtered_data = filtered_data[filtered_data.apply(is_worked_day, axis=1)].copy()

# Print unmatched days for reference
if unmatched_days:
    print("Unmatched Days (Days in Notes and #tags column not worked):")
    for weekday, day, month in unmatched_days:
        print(f"{weekday}, {day:02d}/{month}/2024")

# Calculate total money spent (Money Out + Money In)
final_filtered_data['Total Spent'] = final_filtered_data.loc[:, 'Money Out'].fillna(0) + final_filtered_data.loc[:, 'Money In'].fillna(0)

# Save the final filtered data to a new CSV file
output_file = "/Users/alialnaimi/Downloads/Final_Filtered_Transport_for_London.csv"
final_filtered_data.to_csv(output_file, index=False)

# Print results
print(f"Filtered data saved to {output_file}")
