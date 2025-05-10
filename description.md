# Chess Game

## Project Overview
This project is a digital chess game with integrated data analytics to enhance player experience and post‐game analysis. It tracks metrics such as move time, material balance, and checkmate frequency, then presents insights via charts and tables. The implementation uses object-oriented design for modularity and scalability.

---

## Project Review
Existing platforms like Lichess and Chess.com offer analytics, but this project adds:
- **Deeper in-game statistics**  
- **Real-time event tracking**  
- **Enhanced visualizations** for player performance

---

## Programming Development

### Game Concept
- **Mechanics**: Turn-based play, full rule enforcement, local two-player support  
- **Objectives**: Achieve checkmate while optimizing play guided by live statistics  
- **Key Selling Points**  
  - Detailed in-game metrics  
  - Post-game analysis reports (graphs & tables)  

### OOP Implementation

#### `Main`
- **Role**: Manages the Pygame loop  
- **Key Attributes**:  
  - `screen`: Pygame display  
  - `game`: `Game` instance  
- **Key Method**:  
  - `mainloop()`

#### `Game`
- **Role**: Central game controller (board, pieces, turns)  
- **Key Attributes**:  
  - `board`: `Board` instance  
  - `next_player`: `'white'` or `'black'`  
  - `dragger`: Drag-and-drop handler  
  - `white_clock`/`black_clock`: Clocks  
  - `game_over`, `winner`  
- **Key Methods**:  
  - `show_background()`, `show_piece()`, `show_available_moves()`, `show_clocks()`  
  - `next_turn()`, `reset()`, `check_game_over()`

#### `Board`
- **Role**: Stores squares & pieces, applies moves  
- **Key Attributes**:  
  - `board`: 8×8 array of `Square`  
  - `history`: Move history for undo  
- **Key Methods**:  
  - `_create_board()`, `_place_pieces()`  
  - `apply_move()`, `move_piece()`, `is_in_check()`, `is_checkmate()`

#### `Piece` (ABC)
- **Role**: Base for all pieces (`Pawn`, `Knight`, etc.)  
- **Key Attributes**:  
  - `name`, `color`, `value`, `moved`, `texture`  
- **Key Methods**:  
  - `get_moves()`, `valid_moves()`, `move()`

#### `Square`
- **Role**: Represents a board cell  
- **Key Attributes**:  
  - `row`, `col`, `piece`  
- **Key Methods**:  
  - `has_piece()`, `is_empty()`, `has_team_piece()`, `has_enemy_piece()`

#### `DragHandler`
- **Role**: Manages drag-and-drop of pieces  
- **Key Attributes**:  
  - `piece`, `dragging`, `mouseX`, `mouseY`, `initial_row/col`  
- **Key Methods**:  
  - `drag_piece()`, `undrag_piece()`, `update_mouse()`, `update_blit()`

#### `Clock`
- **Role**: Tracks move and game time  
- **Key Attributes**:  
  - `time_limit`, `remaining_time`, `turn`  
- **Key Methods**:  
  - `start()`, `stop()`, `reset()`, `time_record()`

---

## Algorithms Involved
1. **Move Validation**: Ensures legality  
2. **Check & Checkmate Detection**  
3. **Material Balance Calculation**

---

## Statistical Data (Prop Stats)

| Feature               | Purpose                                | Collection Method          | Display Format |
|-----------------------|----------------------------------------|----------------------------|----------------|
| **Time per move (s)** | Analyze speed & decision-making        | `Clock` class              | Histogram      |
| **Win/Draw/Loss Rate**| Track overall success rate             | `Game` class               | Pie chart      |
| **Material Balance**  | Evaluate positional advantage          | `Board` class              | Line graph     |
| **Checks & Checkmates**| Identify attacking strategies         | `Board` (`is_checkmate`)   | Summary table  |
| **Game Duration**     | Measure overall pacing                | `Clock` class              | Scatter plot   |

- **Data Recording**: CSV format for analysis & visualization

---

## Data Analysis Report

### 1. Time per move (s)  
- **Displayed as**: Histogram  
- **Analysis**: Distribution of move times, revealing speed and decision patterns

### 2. Win/Draw/Loss Rate  
- **Displayed as**: Pie Chart  
- **Analysis**: Proportions of wins, draws, and losses

### 3. Material Balance  
- **Displayed as**: Line Graph  
- **Analysis**: Positional advantage over time

### 4. Checks & Checkmates  
- **Displayed as**: Summary Statistics/Table  
- **Analysis**:  
  | Metric             | Value                |
  |--------------------|----------------------|
  | Total Checks       | _sum of `check_count`_   |
  | Average Checks/Game| _mean of `check_count`_  |
  | Max Checks/Game    | _max `check_count`_       |
  | SD of Checks       | _std dev of `check_count`_|
  | Checkmates Occurred| _count of games with checkmate_ |

### 5. Game Duration vs Moves  
- **Displayed as**: Scatter Plot  
- **Analysis**: Relationship between game length and number of moves

---

## Graphs Specification

| Feature                    | Graph Type   | Purpose                                           |
|----------------------------|--------------|---------------------------------------------------|
| Time per move (s)          | Histogram    | Illustrate distribution of move times             |
| Material Balance           | Line Graph   | Visualize changes in material advantage over time |
| Game Duration vs Moves     | Scatter Plot | Analyze pacing relative to move count             |

---

## Link for present<br>
    https://youtu.be/DCgnFQHeYTw

## License
MIT © _Your Name_

