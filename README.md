# Chess Game with Data Analytics

A digital, two-player chess game built with Pygame and Python, augmented by real-time data tracking and post-game analysis.  Track metrics like move time, material balance, and checkmate frequency, then view histograms, pie charts, line graphs, tables, and scatter plots to gain insights into your play.

---

## 🔑 Features

- Classic turn-based chess mechanics  
- Drag-and-drop piece movement  
- Full rule enforcement (including castling, en-passant, pawn promotion)  
- Dual clocks with customizable time limits  
- Real-time highlights of legal moves  
- Game state persistence & undo support  
- **Data analytics**:  
  - **Time per move** (Histogram)  
  - **Win/Draw/Loss rate** (Pie chart)  
  - **Material balance** (Line graph)  
  - **Checks & checkmates** (Summary table)  
  - **Game duration vs. moves** (Scatter plot)  

---

## 📋 Prerequisites

- **Python** 3.7 or higher  
- **Pygame** 2.0+  
- **Pandas**  
- **Matplotlib**

---

## Installation

1. **Download the ZIP (v1.0)**  
   Download the latest release (version 1.0) from our GitHub releases page:  

2. **Extract the archive**  
   ```bash
   unzip chess_game-v1.0.zip
   cd Chess_game-v1.0

3. **Create a virtual environment (recommended)**
  bash
  python -m venv venv
  macOS/Linux
  source venv/bin/activate
  Windows (PowerShell)
  .\venv\Scripts\Activate.ps1

4. **install pygame**
  pip install pygame or pip3 install pygame

5. **run game**
  python main.py