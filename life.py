import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image, ImageTk
import io

# ---------------- LOAD DATA ---------------- #

df = pd.read_csv("life.csv")

# Clean column names (IMPORTANT)
df.columns = df.columns.str.strip()

years = sorted(df["Year"].unique())

# ---------------- GRAPH FUNCTION ---------------- #

def show_graph(data, title):
    names = list(data["Country"])
    values = list(data["Life expectancy"])
    n = len(names)

    fig_height = n * 0.45  # forces spacing between labels
    fig, ax = plt.subplots(figsize=(12, fig_height))

    ax.barh(range(n), values)
    ax.set_yticks(range(n))
    ax.set_yticklabels(names, fontsize=10)

    ax.set_xlabel("Life Expectancy")
    ax.set_title(title)

    plt.subplots_adjust(left=0.35)  # space for long country names
    plt.tight_layout()

    # Convert to image for Tkinter scrolling
    buf = io.BytesIO()
    FigureCanvasAgg(fig).print_png(buf)
    buf.seek(0)

    img = Image.open(buf)
    plt.close(fig)

    img_tk = ImageTk.PhotoImage(img)

    graph_canvas.delete("all")
    graph_canvas.image = img_tk
    graph_canvas.create_image(0, 0, anchor="nw", image=img_tk)
    graph_canvas.config(scrollregion=(0, 0, img.width, img.height))


# ---------------- FILTERING LOGIC ---------------- #

def get_filtered_data():
    year = int(year_var.get())
    sort_option = sort_var.get()

    filtered = df[df["Year"] == year]

    if sort_option == "Highest to Lowest":
        filtered = filtered.sort_values("Life expectancy", ascending=False)
    elif sort_option == "Lowest to Highest":
        filtered = filtered.sort_values("Life expectancy", ascending=True)

    return filtered


def show_all():
    filtered = get_filtered_data()
    show_graph(filtered, f"Life Expectancy by Country ({year_var.get()})")


def show_selected():
    selected = country_listbox.curselection()
    if not selected:
        return

    selected_names = [country_listbox.get(i) for i in selected]
    filtered = get_filtered_data()
    filtered = filtered[filtered["Country"].isin(selected_names)]

    show_graph(filtered, f"Selected Countries ({year_var.get()})")


# ---------------- SEARCH FILTER ---------------- #

def update_country_list(event=None):
    search_term = search_var.get().lower()
    country_listbox.delete(0, tk.END)

    filtered = df[df["Year"] == int(year_var.get())]["Country"].unique()

    for country in sorted(filtered):
        if search_term in country.lower():
            country_listbox.insert(tk.END, country)


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Life Expectancy Dashboard")
root.geometry("1000x750")

tk.Label(root, text="Life Expectancy Dashboard", font=("Arial", 18)).pack(pady=10)

# --- Controls Frame ---
controls = tk.Frame(root)
controls.pack(pady=5)

# Year Selector
tk.Label(controls, text="Select Year:").grid(row=0, column=0)
year_var = tk.StringVar(value=str(years[-1]))
year_menu = ttk.Combobox(controls, textvariable=year_var, values=years, width=8)
year_menu.grid(row=0, column=1)
year_menu.bind("<<ComboboxSelected>>", update_country_list)

# Sort Selector
tk.Label(controls, text="Sort:").grid(row=0, column=2)
sort_var = tk.StringVar(value="Highest to Lowest")
sort_menu = ttk.Combobox(
    controls,
    textvariable=sort_var,
    values=["Highest to Lowest", "Lowest to Highest"],
    width=20
)
sort_menu.grid(row=0, column=3)

# Search Bar
tk.Label(controls, text="Search Country:").grid(row=0, column=4)
search_var = tk.StringVar()
search_entry = tk.Entry(controls, textvariable=search_var)
search_entry.grid(row=0, column=5)
search_entry.bind("<KeyRelease>", update_country_list)

# --- Buttons ---
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Show All Countries", command=show_all).pack(side="left", padx=5)
tk.Button(btn_frame, text="Show Selected Countries", command=show_selected).pack(side="left", padx=5)

# --- Country List ---
list_frame = tk.Frame(root)
list_frame.pack(pady=10)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

country_listbox = tk.Listbox(
    list_frame,
    width=45,
    height=15,
    selectmode="multiple",
    yscrollcommand=scrollbar.set
)

scrollbar.config(command=country_listbox.yview)
country_listbox.pack(side="left")

update_country_list()

# --- Scrollable Graph Area ---
graph_frame = tk.Frame(root)
graph_frame.pack(fill="both", expand=True)

graph_canvas = tk.Canvas(graph_frame, bg="white")
graph_canvas.pack(side="left", fill="both", expand=True)

graph_scroll = tk.Scrollbar(graph_frame, orient="vertical", command=graph_canvas.yview)
graph_scroll.pack(side="right", fill="y")

graph_canvas.config(yscrollcommand=graph_scroll.set)

root.mainloop()