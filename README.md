# 🚇 Travel Reimbursement Automation with Monzo Data

This project automates the process of filtering and calculating eligible **Transport for London (TfL)** travel expenses from **Monzo** bank transaction exports. It helps streamline the tracking of commuting costs for workdays, making it easier to organize or submit for reimbursement if applicable.

---

## 💡 Project Purpose

Manually identifying and summing up daily transport expenses for specific workdays can be tedious. This tool was created to:

- Extract and clean relevant entries from Monzo bank statements
- Parse custom travel dates using **regular expressions**
- Match spending to predefined **working days**
- Calculate **daily totals** and optionally reimbursable amounts
- Export a clean, ready-to-use **CSV** for reporting or review

---

## 🛠️ Tools & Technologies

- **Python**
- **pandas**
- **Regular Expressions (re)**
- **CSV File Handling**

---

## 📁 How It Works

1. **Load Monzo Export**  
   Reads a CSV export and filters rows with `"Transport for London"` as the merchant.

2. **Parse Travel Dates**  
   Extracts day, month, and weekday info from the `Notes and #tags` column using regex.

3. **Filter Workdays**  
   Compares parsed dates against a manually defined list of valid **workdays per month**.

4. **Calculate Totals**  
   Sums up travel costs on matching days. You can also define a custom reimbursement percentage.

5. **Export Results**  
   Outputs a new CSV file with only relevant transactions and summary calculations.

---

## ✅ Benefits

- Eliminates repetitive manual logging
- Works directly with Monzo exports
- Saves time on organizing or reporting transport expenses
- Easily customizable for different months or travel providers

---

## ⚙️ Customization

Update these in the script as needed:
- `days_worked` dictionary – to reflect your actual work calendar
- Reimbursement logic – adjust the percentage or add thresholds
- File paths – set your own input/output locations

---

## 📎 Sample Output

- `Final_Filtered_Transport_for_London.csv`  
  Includes:
  - Date (parsed from notes)
  - Total amount spent
  - Optional reimbursable amount

---

## 📂 Suggested Folder Structure

