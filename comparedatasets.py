import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd


def open_dataset(parent):
    file_paths = filedialog.askopenfilenames(
        title="Select Two or More Datasets",
        filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")]
    )

    if len(file_paths) < 2:
        messagebox.showwarning(
            "Not Enough Files",
            "Please select at least two datasets to compare."
        )
        return

    analyze_datasets(parent, file_paths)


def analyze_datasets(parent, file_paths):
    dataframes = []

    for file in file_paths:
        if file.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            continue

        df.columns = df.columns.str.strip()
        dataframes.append(df)

    common_columns = set(dataframes[0].columns)

    for df in dataframes[1:]:
        common_columns = common_columns.intersection(df.columns)

    show_results(parent, file_paths, common_columns)


def show_results(parent, file_paths, common_columns):
    window = tk.Toplevel(parent)
    window.title("Dataset Compatibility Check")
    window.geometry("600x400")

    text = tk.Text(window, wrap="word")
    text.pack(expand=True, fill="both", padx=10, pady=10)

    text.insert("end", "Datasets selected:\n\n")
    for file in file_paths:
        text.insert("end", f"- {file}\n")

    text.insert("end", "\nCommon columns found:\n\n")

    if common_columns:
        for col in sorted(common_columns):
            text.insert("end", f"• {col}\n")

        text.insert(
            "end",
            "\nResult: ✅ These datasets are suitable for comparison.\n"
            "They share one or more common columns (such as Year, Date, Country, etc.).\n"
        )
    else:
        text.insert(
            "end",
            "❌ No common columns found.\n\n"
            "Result: These datasets are NOT suitable for direct comparison.\n"
        )

    text.config(state="disabled")
