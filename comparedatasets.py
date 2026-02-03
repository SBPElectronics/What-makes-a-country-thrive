import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from itertools import combinations


def open_dataset(parent):
    file_paths = filedialog.askopenfilenames(
        title="Select Datasets",
        filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")]
    )

    if len(file_paths) < 2:
        messagebox.showwarning(
            "Not enough files",
            "Please select at least 2 datasets."
        )
        return

    analyze_datasets(parent, file_paths)


def load_dataframe(file):
    if file.endswith(".csv"):
        df = pd.read_csv(file)
    elif file.endswith(".xlsx"):
        df = pd.read_excel(file)
    else:
        return None

    # Normalise column names
    df.columns = df.columns.str.strip().str.lower()
    return df


def analyze_datasets(parent, file_paths):
    datasets = {}

    for file in file_paths:
        try:
            df = load_dataframe(file)
            if df is not None:
                datasets[file] = set(df.columns)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load:\n{file}\n\n{e}")
            return

    similar_groups = []
    used_files = set()

    # Compare every pair of datasets
    for file1, file2 in combinations(datasets.keys(), 2):
        common_cols = datasets[file1] & datasets[file2]

        # If they share enough columns, treat them as similar
        if len(common_cols) >= 2:
            group = {file1, file2}

            # Merge with existing group if overlapping
            merged = False
            for existing in similar_groups:
                if existing & group:
                    existing.update(group)
                    merged = True
                    break

            if not merged:
                similar_groups.append(group)

            used_files.update(group)

    excluded_files = set(datasets.keys()) - used_files

    show_results(parent, similar_groups, excluded_files, datasets)


def show_results(parent, similar_groups, excluded_files, datasets):
    window = tk.Toplevel(parent)
    window.title("Dataset Comparison Results")
    window.geometry("700x500")

    text = tk.Text(window, wrap="word")
    text.pack(expand=True, fill="both", padx=10, pady=10)

    if similar_groups:
        text.insert("end", "Similar datasets found:\n\n")

        for i, group in enumerate(similar_groups, start=1):
            text.insert("end", f"Group {i}:\n")
            for file in group:
                text.insert("end", f"  • {file}\n")

            common = set.intersection(*(datasets[f] for f in group))
            text.insert("end", "  Common columns:\n")
            for col in sorted(common):
                text.insert("end", f"    - {col}\n")

            text.insert("end", "\n")
    else:
        text.insert("end", "No similar datasets found.\n\n")

    if excluded_files:
        text.insert("end", "Excluded datasets (not compatible):\n\n")
        for file in excluded_files:
            text.insert("end", f"  • {file}\n")

    text.config(state="disabled")