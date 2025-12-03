import tkinter as tk
from tkinter import ttk
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SearchableComboBox:
    """Searchable dropdown list attached to an Entry widget."""

    def __init__(self, entry_widget, options, on_select_callback):
        self.options = options
        self.entry = entry_widget
        self.on_select_callback = on_select_callback
        self.listbox = tk.Listbox(self.entry.master, height=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown)
        self.entry.bind("<FocusOut>", self.hide_dropdown)

        for option in self.options:
            self.listbox.insert(tk.END, option)

    def on_entry_key(self, event):
        typed_value = self.entry.get().strip().lower()
        self.listbox.delete(0, tk.END)
        for option in self.options:
            if typed_value in option.lower():
                self.listbox.insert(tk.END, option)
        self.show_dropdown()

    def on_select(self, event):
        if self.listbox.curselection():
            selected_option = self.listbox.get(self.listbox.curselection())
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_option)
            self.on_select_callback(selected_option)
        self.hide_dropdown()

    def show_dropdown(self, event=None):
        self.listbox.place(in_=self.entry, x=0, rely=1, relwidth=1.0)
        self.listbox.lift()

    def hide_dropdown(self, event=None):
        # Hide dropdown only if focus is not on listbox or entry
        if not (self.entry.focus_get() == self.entry or self.listbox.focus_get() == self.listbox):
            self.listbox.place_forget()


class PopulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Population Trends")

        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.pop_file_path = self.find_csv_file("population.csv")
        if not self.pop_file_path:
            tk.messagebox.showerror("File Not Found", "population.csv not found in the directory.")
            root.destroy()
            return

        self.countries, self.population_data = self.read_population_data()

        # Entry with Searchable ComboBox for country selection
        tk.Label(self.main_frame, text="Select a Country:").pack(pady=(0,5))
        self.country_entry = tk.Entry(self.main_frame)
        self.country_entry.pack(fill=tk.X)
        self.searchable_combo = SearchableComboBox(self.country_entry, self.countries, self.on_country_selected)

        # Plot button
        self.plot_button = ttk.Button(self.main_frame, text="Plot Population Over Years", command=self.plot_population)
        self.plot_button.pack(pady=10)

        # Matplotlib figure embedded in Tkinter
        self.figure, self.ax = plt.subplots(figsize=(8,5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def find_csv_file(self, filename):
        for dirpath, _, filenames in os.walk(os.getcwd()):
            if filename in filenames:
                return os.path.join(dirpath, filename)
        return None

    def read_population_data(self):
        countries = []
        population_data = {}

        with open(self.pop_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country = row['country_name']
                countries.append(country)
                population_data[country] = {}

                for col in row.keys():
                    if col.isdigit():
                        try:
                            population_data[country][int(col)] = float(row[col])
                        except ValueError:
                            # skip invalid values
                            pass

        return countries, population_data

    def on_country_selected(self, country):
        # Optional: auto-plot when country selected
        pass

    def plot_population(self):
        country = self.country_entry.get().strip()
        if country not in self.population_data:
            tk.messagebox.showwarning("Invalid Country", "Please select a valid country from the list.")
            return

        years = sorted(self.population_data[country].keys())
        populations = [self.population_data[country][year] for year in years]

        self.ax.clear()
        self.ax.plot(years, populations, marker='o', color='blue')
        self.ax.set_title(f"Population over Years: {country}")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("Population (units as per data)")
        self.ax.grid(True)

        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = PopulationApp(root)
    root.mainloop()
