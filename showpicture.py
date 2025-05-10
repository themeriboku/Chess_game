import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ChessStatsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess Data Analysis")
        self.geometry("800x600")

        self.df = None
        self.figures = []
        self.current_index = 0
        self.canvas = None

        btn_load = tk.Button(self, text="Load CSV", command=self.load_csv)
        btn_load.pack(pady=10)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        nav = tk.Frame(self)
        nav.pack(pady=10)

        self.btn_prev = tk.Button(nav, text="◀ Previous", command=self.show_prev, state="disabled")
        self.btn_prev.pack(side="left", padx=5)

        self.label_status = tk.Label(nav, text="")
        self.label_status.pack(side="left", padx=5)

        self.btn_next = tk.Button(nav, text="Next ▶", command=self.show_next, state="disabled")
        self.btn_next.pack(side="left", padx=5)

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        self.df = pd.read_csv(path)
        self.generate_figures()
        self.current_index = 0
        self.show_plot()
        self.update_buttons()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def generate_figures(self):
        self.figures.clear()
        df = self.df

        # 1. Histogram
        fig1, ax1 = plt.subplots()
        ax1.hist(df["avg_time_per_move_s"], bins=10)
        ax1.set_title("Time per Move (s)")
        ax1.set_xlabel("Seconds")
        ax1.set_ylabel("Frequency")
        self.figures.append(fig1)

        # 2. Pie Chart
        fig2, ax2 = plt.subplots()
        counts = df["result"].value_counts()
        ax2.pie(counts, labels=counts.index, autopct="%1.1f%%")
        ax2.set_title("Win/Draw/Loss Rate")
        self.figures.append(fig2)

        # 3. Line Graph
        fig3, ax3 = plt.subplots()
        ax3.plot(df.index, df["avg_material_balance"], marker="o")
        ax3.set_title("Material Balance Over Games")
        ax3.set_xlabel("Game Index")
        ax3.set_ylabel("Material Balance")
        self.figures.append(fig3)

        # 4. Summary Table
        fig4, ax4 = plt.subplots(figsize=(4, 2.5))
        ax4.axis("off")
        stats = df[["check_count", "checkmate_occurred"]].describe().T
        tbl = ax4.table(
            cellText=stats.round(2).values,
            rowLabels=stats.index,
            colLabels=stats.columns,
            loc='center'
        )
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(8)
        tbl.scale(1.0, 1.2)
        ax4.set_title("Checks & Checkmates Statistics", fontsize=10)
        self.figures.append(fig4)

        # 5. Scatter Plot
        fig5, ax5 = plt.subplots()
        ax5.scatter(df["moves"], df["duration_s"])
        ax5.set_title("Game Duration vs Moves")
        ax5.set_xlabel("Number of Moves")
        ax5.set_ylabel("Duration (s)")
        self.figures.append(fig5)

    def show_plot(self):
        self.clear_container()
        fig = self.figures[self.current_index]
        self.canvas = FigureCanvasTkAgg(fig, master=self.container)
        self.canvas.draw()
        widget = self.canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        self.label_status.config(text=f"Plot {self.current_index + 1} of {len(self.figures)}")

    def show_next(self):
        if self.current_index < len(self.figures) - 1:
            self.current_index += 1
            self.show_plot()
            self.update_buttons()

    def show_prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_plot()
            self.update_buttons()

    def update_buttons(self):
        self.btn_prev["state"] = "normal" if self.current_index > 0 else "disabled"
        self.btn_next["state"] = "normal" if self.current_index < len(self.figures) - 1 else "disabled"

if __name__ == "__main__":
    app = ChessStatsApp()
    app.mainloop()
