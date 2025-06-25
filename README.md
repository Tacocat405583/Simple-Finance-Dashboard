readme = <<~README
  # 💰 Simple Finance Dashboard

  A personal finance dashboard built with **Streamlit** and **Plotly**, allowing users to upload CSV transaction files, categorize expenses, and visualize income and spending habits through charts and summaries.

  ---

  ## 🚀 Features

  - 📂 Upload CSV files containing your transaction data.
  - 🧠 Auto-categorization of expenses using keyword matching.
  - ✍️ Manually edit categories via an interactive UI.
  - 📊 View pie charts of expenses by category.
  - 💸 See a breakdown of total income and categorized spending.
  - 💾 Categories and keywords are saved to a local `categories.json` file.

  ---

  ## 📁 CSV Format Requirements

  Your file must have the following columns:

  - `Date` (format: `dd mmm yyyy`, e.g., `12 Jan 2024`)
  - `Details` (text description)
  - `Amount` (can include commas)
  - `Debit/Credit` (either "Debit" or "Credit")

  Example:

Date,Details,Amount,Debit/Credit
12 Jan 2024,Amazon,120.00,Debit
15 Jan 2024,Paycheck,2500.00,Credit

yaml
Copy
Edit

---

## 🛠️ Setup Instructions

1. **Install Dependencies**

   ```bash
   pip install streamlit pandas numpy plotly
   ```

2. **Run the App**

   ```bash
   streamlit run your_script_name.py
   ```

   Replace `your_script_name.py` with the actual name of your Python file.

---

## 🧠 How Categorization Works

- The app uses a local `categories.json` file to remember your custom categories and associated keywords.
- When uploading a file, the app auto-assigns categories based on keywords found in the `Details` column.
- You can manually assign or edit categories using the built-in editor, and the app will remember your changes for future uploads.

---

## 📦 File Structure

.
├── categories.json # Saved user categories and keywords (auto-generated)
├── your_script.py # Streamlit app

yaml
Copy
Edit

---

## 📝 TODO / Improvements

- Add authentication for multiple users
- Export categorized data
- Trend analysis over time
- Add search/filter for transactions

---

## 🖼️ Screenshots

*Add screenshots of the dashboard interface here for better clarity.*

---

## 🔒 Disclaimer

All data is stored locally. This is a simple personal-use tool and is not intended for sensitive or commercial finance tracking.
README

puts readme
