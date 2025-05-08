import pandas as pd
import re
import os

def main():
    # Ask user for input file path and output details
    file_path = input("Enter the full path of the Monzo CSV file: ").strip()
    document_name = input("Enter a short name for the output file (e.g., 'TFL_March2025'): ").strip()
    output_folder = input("Enter the folder path where the output should be saved: ").strip()

    # Read the CSV file
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Filter the rows where the "Name" column is "Transport for London"
    filtered_data = data[data['Name'] == 'Transport for London'].copy()

    # Days worked by month
    days_worked = {
        "Dec": [15, 18, 19, 21, 26, 28, 31],
        "Jan": [1, 4, 5, 9, 11, 14, 16, 18, 20, 21, 24, 25, 26, 27, 31],
        "Feb": [1, 3, 6, 7, 10, 11, 13, 14, 15, 17, 20, 21, 24, 26, 27, 28],
        "Mar": [1, 3, 6, 7, 9, 10, 11]
    }

    unmatched_days = []

    def extract_day_month_weekday(notes):
        match = re.search(r'(\w+),\s*(\d{1,2})\s*(\w+)', str(notes))
        if match:
            weekday = match.group(1)
            day = int(match.group(2))
            month = match.group(3)
            return weekday, day, month
        return None, None, None

    filtered_data['Weekday'], filtered_data['Day'], filtered_data['Month'] = zip(*filtered_data['Notes and #tags'].apply(extract_day_month_weekday))
    filtered_data['Day'] = pd.to_numeric(filtered_data['Day'], errors='coerce').astype('Int64')

    invalid_dates = filtered_data[filtered_data['Day'].isna() | filtered_data['Month'].isna()]
    if not invalid_dates.empty:
        print("Warning: Some rows have invalid date descriptions and were excluded.")
        print(invalid_dates[['Notes and #tags']])

    def is_worked_day(row):
        month = row['Month']
        day = row['Day']
        if pd.notna(day) and month in days_worked:
            if int(day) in days_worked[month]:
                return True
            else:
                unmatched_days.append((row['Weekday'], int(day), month))
        return False

    final_filtered_data = filtered_data[filtered_data.apply(is_worked_day, axis=1)].copy()

    if unmatched_days:
        print("Unmatched Days (Days in Notes and #tags column not worked):")
        for weekday, day, month in unmatched_days:
            print(f"{weekday}, {day:02d}/{month}/2024")

    final_filtered_data['Total Spent'] = final_filtered_data['Money Out'].fillna(0) + final_filtered_data['Money In'].fillna(0)

    output_file = os.path.join(output_folder, f"{document_name}.csv")
    try:
        final_filtered_data.to_csv(output_file, index=False)
        print(f"\nFiltered data saved to: {output_file}\n")
    except Exception as e:
        print(f"Error saving output file: {e}")
        return

    # Show an example row
    print("Example of filtered data:")
    print(final_filtered_data.head(1).to_string(index=False))

if __name__ == "__main__":
    main()
