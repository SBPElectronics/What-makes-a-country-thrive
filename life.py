import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image, ImageTk
import io

df = pd.read_csv("life.csv")
latest = df.sort_values("Year").groupby("Country").tail(1)
countries = sorted(latest["Country"].unique())


def show_graph(data, title):
    names = list(data["Country"])
    values = list(data["Life expectancy "])
    n = len(names)

    # Force large height so each label gets space
    fig_height = n * 0.45   # increase to 0.5 if still tight

    fig, ax = plt.subplots(figsize=(12, fig_height))

    ax.barh(range(n), values)
    ax.set_yticks(range(n))
    ax.set_yticklabels(names, fontsize=10)

    ax.set_xlabel("Life Expectancy")
    ax.set_title(title)

    # Make room for long country names
    plt.subplots_adjust(left=0.35)

    plt.tight_layout()

    # Convert figure to image
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


def show_all():
    sorted_data = latest.sort_values("Life expectancy ")
    show_graph(sorted_data, "Life Expectancy by Country")


def show_selected():
    selected = [countries[i] for i in country_listbox.curselection()]
    if not selected:
        return
    filtered = latest[latest["Country"].isin(selected)].sort_values("Life expectancy ")
    show_graph(filtered, "Life Expectancy (Selected Countries)")


# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("Life Expectancy Viewer")
root.geometry("900x700")

title_label = tk.Label(root, text="Life Expectancy Dashboard", font=("Arial", 18))
title_label.pack(pady=10)

buttons_frame = tk.Frame(root)
buttons_frame.pack()

tk.Button(buttons_frame, text="Show All Countries", command=show_all).pack(side="left", padx=10)
tk.Button(buttons_frame, text="Show Selected", command=show_selected).pack(side="left", padx=10)

# --- Country list with scrollbar ---
frame = tk.Frame(root)
frame.pack(pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

country_listbox = tk.Listbox(frame, selectmode="multiple", width=40, height=15, yscrollcommand=scrollbar.set)
scrollbar.config(command=country_listbox.yview)

for c in countries:
    country_listbox.insert(tk.END, c)

country_listbox.pack(side="left")

# --- SCROLLABLE GRAPH AREA ---
graph_frame = tk.Frame(root)
graph_frame.pack(fill="both", expand=True)

graph_canvas = tk.Canvas(graph_frame, bg="white")
graph_canvas.pack(side="left", fill="both", expand=True)

graph_scrollbar = tk.Scrollbar(graph_frame, orient="vertical", command=graph_canvas.yview)
graph_scrollbar.pack(side="right", fill="y")

graph_canvas.config(yscrollcommand=graph_scrollbar.set)

root.mainloop()