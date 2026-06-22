import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class life_expectancy_app:
    def __init__(self, root):
        self.root = root
        self.root.title("Life Expectancy Dashboard")
        self.root.geometry("1000x500")

        self.df = pd.read_csv("life.csv")
        self.df.columns = self.df.columns.str.strip()
        self.years = sorted(self.df["Year"].unique())

        self.build_gui()
        self.update_country_list()

    def build_gui(self):
        tk.Label(self.root, text="Life Expectancy Dashboard", font=("Arial", 18)).pack(pady=10)

        controls = tk.Frame(self.root)
        controls.pack(pady=5)

        self.year_var = tk.StringVar(value=str(self.years[-1]))
        self.sort_var = tk.StringVar(value="Highest to Lowest")
        self.search_var = tk.StringVar()

        tk.Label(controls, text="Year:").grid(row=0, column=0, padx=5)
        ttk.Combobox(controls, textvariable=self.year_var, values=self.years, width=8).grid(row=0, column=1)

        tk.Label(controls, text="Sort:").grid(row=0, column=2, padx=5)
        ttk.Combobox(
            controls,
            textvariable=self.sort_var,
            values=["Highest to Lowest", "Lowest to Highest"],
            width=20
        ).grid(row=0, column=3)

        tk.Label(controls, text="Search:").grid(row=0, column=4, padx=5)
        self.search_entry = tk.Entry(controls, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=5)
        self.search_entry.bind("<KeyRelease>", self.update_country_list)

        self.country_listbox = tk.Listbox(self.root, width=45, height=15, selectmode="multiple")
        self.country_listbox.pack(pady=10)

        tk.Button(self.root, text="Show All Countries", command=self.show_all).pack(pady=3)
        tk.Button(self.root, text="Show Selected Countries", command=self.show_selected).pack(pady=3)

    def get_filtered_data(self):
        year = int(self.year_var.get())
        filtered = self.df[self.df["Year"] == year]
        sort_mode = self.sort_var.get()

        if sort_mode == "Highest to Lowest":
            filtered = filtered.sort_values("Life expectancy", ascending=True)
        elif sort_mode == "Lowest to Highest":
            filtered = filtered.sort_values("Life expectancy", ascending=False)

        return filtered

    def update_country_list(self, event=None):
        self.country_listbox.delete(0, tk.END)
        year = int(self.year_var.get())
        countries = self.df[self.df["Year"] == year]["Country"].unique()
        search_text = self.search_var.get().lower()

        for c in sorted(countries):
            if search_text in c.lower():
                self.country_listbox.insert(tk.END, c)

    def show_all(self):
        self.show_graph(self.get_filtered_data(), "Life Expectancy by Country")

    def show_selected(self):
        selected = self.country_listbox.curselection()
        if not selected:
            return
        names = [self.country_listbox.get(i) for i in selected]
        data = self.get_filtered_data()
        self.show_graph(data[data["Country"].isin(names)], "Selected Countries")

    def show_graph(self, data, title):
        if data.empty:
            return

        graph_window = tk.Toplevel(self.root)
        graph_window.title(title)
        graph_window.geometry("900x600")

        graph_canvas = tk.Canvas(graph_window)
        scrollbar = ttk.Scrollbar(graph_window, orient="vertical", command=graph_canvas.yview)
        scrollable_frame = tk.Frame(graph_canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: graph_canvas.configure(scrollregion=graph_canvas.bbox("all"))
        )

        graph_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        graph_canvas.configure(yscrollcommand=scrollbar.set)
        graph_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        height = max(6, len(data) * 0.25)
        fig, ax = plt.subplots(figsize=(10, height))
        ax.barh(data["Country"], data["Life expectancy"])
        ax.set_title(title)
        ax.tick_params(axis='y', labelsize=7)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

if __name__ == "__main__":
    root = tk.Tk()
    app = life_expectancy_app(root)
    root.mainloop()