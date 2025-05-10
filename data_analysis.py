import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ChessStatsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess Data Analysis")
        self.geometry("1200x800")
        
        # ปุ่มโหลด CSV
        btn = tk.Button(self, text="Load CSV", command=self.load_csv)
        btn.pack(pady=10)
        
        # แท็บหรือเฟรมสำหรับกราฟ
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        df = pd.read_csv(path)
        self.show_all_plots(df)
    
    def clear_container(self):
        for w in self.container.winfo_children():
            w.destroy()
    
    def show_all_plots(self, df):
        self.clear_container()
        figs = []
        
        # 1. Histogram: avg_time_per_move_s
        fig1, ax1 = plt.subplots(figsize=(4,3))
        ax1.hist(df["avg_time_per_move_s"], bins=10)
        ax1.set_title("Time per Move (s)")
        figs.append(fig1)
        
        # 2. Pie chart: result
        fig2, ax2 = plt.subplots(figsize=(4,3))
        counts = df["result"].value_counts()
        ax2.pie(counts, labels=counts.index, autopct="%1.1f%%")
        ax2.set_title("Win/Draw/Loss Rate")
        figs.append(fig2)
        
        # 3. Line graph: avg_material_balance
        fig3, ax3 = plt.subplots(figsize=(4,3))
        ax3.plot(df.index, df["avg_material_balance"], marker="o")
        ax3.set_title("Material Balance Over Games")
        figs.append(fig3)
        
        # 4. Summary table: check_count & checkmate_occurred
        stats = df[["check_count","checkmate_occurred"]].describe().T
        fig4, ax4 = plt.subplots(figsize=(4,3))
        ax4.axis('off')
        tbl = ax4.table(cellText=stats.round(2).values,
                        rowLabels=stats.index,
                        colLabels=stats.columns, loc='center')
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(8)
        ax4.set_title("Checks & Checkmates Statistics")
        figs.append(fig4)
        
        # 5. Scatter plot: duration_s vs moves (จะวางด้านขวามือ)
        fig5, ax5 = plt.subplots(figsize=(4,6))  # สูงกว่านิดเพื่อความเหมาะสม
        ax5.scatter(df["moves"], df["duration_s"])
        ax5.set_title("Game Duration vs Moves")
        figs.append(fig5)
        
        # วางกราฟ: 4 กราฟแรกใน 2x2 grid, กราฟสุดท้ายยืดด้านขวา
        for i, fig in enumerate(figs):
            canvas = FigureCanvasTkAgg(fig, master=self.container)
            canvas.draw()
            widget = canvas.get_tk_widget()
            if i < 4:
                widget.grid(row=i//2, column=i%2, padx=10, pady=10)
            else:
                # Position the last figure on the right side spanning two rows
                widget.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

if __name__ == "__main__":
    app = ChessStatsApp()
    app.mainloop()
