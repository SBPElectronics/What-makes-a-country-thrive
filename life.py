import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image, ImageTk
import io

class life_expectancy_app:
    def __init__(self, root):
        self.root = root
        self.root.title("Life Expectancy Dashboard")
        self.root.geometry("1000x750")

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

        ttk.Combobox(controls, textvariable=self.year_var, values=self.years, width=8).grid(row=0, column=1)
        ttk.Combobox(
            controls,
            textvariable=self.sort_var,
            values=["Highest to Lowest", "Lowest to Highest"],
            width=20
        ).grid(row=0, column=3)

        self.search_entry = tk.Entry(controls, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=5)
        self.search_entry.bind("<KeyRelease>", self.update_country_list)

        self.country_listbox = tk.Listbox(self.root, width=45, height=15, selectmode="multiple")
        self.country_listbox.pack(pady=10)

        tk.Button(self.root, text="Show All Countries", command=self.show_all).pack()
        tk.Button(self.root, text="Show Selected Countries", command=self.show_selected).pack()

        self.graph_canvas = tk.Canvas(self.root, bg="white")
        self.graph_canvas.pack(fill="both", expand=True)

    def get_filtered_data(self):
        year = int(self.year_var.get())
        filtered = self.df[self.df["Year"] == year]

        if self.sort_var.get() == "Lowest to Highest":
            filtered = filtered.sort_values("Life expectancy")
        else:
            filtered = filtered.sort_values("Life expectancy", ascending=False)

        return filtered

    def show_all(self):
        self.show_graph(self.get_filtered_data(), "Life Expectancy by Country")

    def show_selected(self):
        selected = self.country_listbox.curselection()
        if not selected:
            return

        names = [self.country_listbox.get(i) for i in selected]
        data = self.get_filtered_data()
        self.show_graph(data[data["Country"].isin(names)], "Selected Countries")

    def update_country_list(self, event=None):
        self.country_listbox.delete(0, tk.END)
        year = int(self.year_var.get())
        countries = self.df[self.df["Year"] == year]["Country"].unique()

        for c in sorted(countries):
            if self.search_var.get().lower() in c.lower():
                self.country_listbox.insert(tk.END, c)

    def show_graph(self, data, title):
        fig, ax = plt.subplots(figsize=(10, len(data) * 0.4))
        ax.barh(data["Country"], data["Life expectancy"])
        ax.set_title(title)

        buf = io.BytesIO()
        FigureCanvasAgg(fig).print_png(buf)
        buf.seek(0)
        img = ImageTk.PhotoImage(Image.open(buf))
        plt.close(fig)

        self.graph_canvas.delete("all")
        self.graph_canvas.image = img
        self.graph_canvas.create_image(0, 0, anchor="nw", image=img)
