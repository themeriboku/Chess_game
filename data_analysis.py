import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ChessStatsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess Data Analysis")
        self.geometry("1000x800")
        
        # ปุ่มโหลด CSV
        btn = tk.Button(self, text="Load CSV", command=self.load_csv)
        btn.pack(pady=10)
        
        # พื้นที่สำหรับแสดงกราฟ
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        df = pd.read_csv(path)
        self.show_all_plots(df)

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_all_plots(self, df):
        self.clear_container()
        figs = []

        # 1. Histogram: avg_time_per_move_s
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.hist(df["avg_time_per_move_s"], bins=10)
        ax1.set_title("Time per Move (s)")
        ax1.set_xlabel("Seconds")
        ax1.set_ylabel("Frequency")
        figs.append(fig1)

        # 2. Pie Chart: result
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        counts = df["result"].value_counts()
        ax2.pie(counts, labels=counts.index, autopct="%1.1f%%")
        ax2.set_title("Win/Draw/Loss Rate")
        figs.append(fig2)

        # 3. Line Graph: avg_material_balance
        fig3, ax3 = plt.subplots(figsize=(4, 3))
        ax3.plot(df.index, df["avg_material_balance"], marker="o")
        ax3.set_title("Material Balance Over Games")
        ax3.set_xlabel("Game Index")
        ax3.set_ylabel("Material Balance")
        figs.append(fig3)

        # 4. Summary Table: check_count & checkmate_occurred
        fig4, ax4 = plt.subplots(figsize=(3.5, 2.5))  # ปรับขนาดให้เล็กลง
        ax4.axis("off")
        stats = df[["check_count", "checkmate_occurred"]].describe().T
        tbl = ax4.table(
            cellText=stats.round(2).values,
            rowLabels=stats.index,
            colLabels=stats.columns,
            loc='center'
        )
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(6)  # ลดขนาดฟอนต์
        tbl.scale(1.0, 1.2)  # ปรับสเกลตารางให้เล็กลง
        ax4.set_title("Checks & Checkmates Statistics", fontsize=10)
        figs.append(fig4)

        # 5. Scatter Plot: duration_s vs moves
        fig5, ax5 = plt.subplots(figsize=(4, 3))
        ax5.scatter(df["moves"], df["duration_s"])
        ax5.set_title("Game Duration vs Moves")
        ax5.set_xlabel("Number of Moves")
        ax5.set_ylabel("Duration (s)")
        figs.append(fig5)

        # วางกราฟแบบ Grid 2x3 ให้อันสุดท้ายอยู่ขวาบน ไม่หลุดจอ
        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2)]  # แถว-คอลัมน์
        for i, fig in enumerate(figs):
            canvas = FigureCanvasTkAgg(fig, master=self.container)
            canvas.draw()
            widget = canvas.get_tk_widget()
            row, col = positions[i]
            widget.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # ทำให้แต่ละช่องขยายได้
        for i in range(3):
            self.container.columnconfigure(i, weight=1)
        for i in range(2):
            self.container.rowconfigure(i, weight=1)

if __name__ == "__main__":
    app = ChessStatsApp()
    app.mainloop()
