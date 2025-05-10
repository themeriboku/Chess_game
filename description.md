Chess Game
Project Overview
This project is a digital chess game that incorporates data analytics to enhance the player experience and game analysis. The game tracks various metrics, such as time per move, material balance, and checkmate frequency, to provide insights into player performance and strategic improvements. The implementation uses object-oriented programming (OOP) principles, ensuring modularity and scalability.

Project Review
A review of existing chess applications, such as Lichess and Chess.com, highlights areas for improvement. While these platforms provide analytics, this project aims to enhance data tracking by incorporating statistical analysis and visualization to help players understand their gameplay better.

Key Improvements:
More detailed in-game statistics.
Real-time tracking of game events.
Improved visual representation of player performance.
Programming Development
The chess game simulates a traditional chess match with additional features for analysis.

Game Concept
Mechanics: Turn-based play with strict rule enforcement; support for local (two players).
Objectives: Achieve checkmate while optimizing play based on real-time statistics.
Key Selling Points:
Detailed tracking of gameplay data.
A post-game analysis report with graphs and statistics to help players improve.
Object-Oriented Programming Implementation
The project employs several classes to encapsulate game components. Below are the core classes:

Main
Role: Manages the game loop and initializes Pygame.
Key Attributes:
screen: The Pygame display surface.
game: An instance of the Game class managing game state.
Key Methods:
mainloop(): Runs the main event loop for the game.
Game
Role: Acts as the central controller of the game state (handling the board, pieces, and turn management).
Key Attributes:
board: The game board that stores squares and pieces.
next_player: Indicates which player's turn is next (e.g., 'white' or 'black').
dragger: Manages the dragging of pieces on the board.
Key Methods:
show_back_ground(): Displays the game’s background.
show_piece(): Renders the chess pieces on the board.
next_turn(): Switches the turn between players.
reset(): Resets the game to its initial state.
Board
Role: Stores the board’s squares and pieces, and handles the application of moves.
Key Attributes:
board: A 2D array of squares representing the layout of the chessboard.
history: A record of previous moves for undo functionality.
Key Methods:
_create_board(): Initializes the board layout.
apply_move(): Applies a given move to update the board state.
is_in_check(): Determines if a player's king is in check.
move_piece(): Moves a piece from one square to another.
Piece (Abstract Base Class)
Role: Serves as the base class for all chess pieces (such as Pawn, Rook, Knight, etc.).
Key Attributes:
name: The name/type of the piece (e.g., "pawn", "knight").
color: The color of the piece ('white' or 'black').
value: A numerical value representing the piece’s relative strength.
Key Methods:
get_moves(): An abstract method to generate possible moves for the piece (must be implemented in subclasses).
valid_moves(): Filters moves to ensure they are valid and do not cause check.
Square
Role: Represents an individual square on the chessboard.
Key Attributes:
row, col: The position of the square on the board.
piece: The piece currently occupying the square (if any).
Key Methods:
has_piece(): Determines if the square contains a piece.
isempty(): Checks if the square is empty.
has_team_piece(color): Checks if the square contains a piece of the given team/color.
has_enemy_piece(color): Checks if the square contains an enemy piece.
DragHandler (or Dragger)
Role: Manages the dragging functionality of a chess piece on the board.
Key Attributes:
piece: The current piece being dragged.
dragging: Boolean flag indicating if a drag is in progress.
mouseX, mouseY: The current mouse coordinates.
Key Methods:
update_blit(): Updates the display for the dragged piece.
update_mouse(): Updates mouse coordinates during dragging.
drag_piece(): Initiates the dragging process for a given piece.
undrag_piece(): Stops the dragging process and resets relevant attributes.
Clock
Role: Manages timing for game events, such as move timing and overall game duration.
Key Attributes:
time_limit: The overall time limit set for a game or move.
remaining_time: The current remaining time.
turn: Indicates which player's time is being tracked.
Key Methods:
start(): Begins the timing process.
stop(): Stops the timing process.
reset(): Resets the clock to its initial state.
time_record(): Records the elapsed time for game data analysis.
Algorithms Involved
Move Validation Algorithm: Ensures only legal moves are allowed.
Check and Checkmate Detection: Identifies game-ending scenarios.
Material Balance Calculation: Tracks piece value differences.
Statistical Data (Prop Stats)
Data Features
The following gameplay metrics will be tracked:

Feature	Purpose	Data Collection Method	Display Format
Time per move (s)	Analyze player speed and decision-making	Collected from Clock class	Histogram
Win/Draw/Loss Rate	Track player success rate	Collected from Game class	Pie chart
Material Balance	Evaluate positional advantage	Collected from Board class	Line Graph
Checks & Checkmates	Identify attacking strategies	Collected from Board class	Summary Table
Game Duration	Measure overall game pacing	Collected from Clock class	Scatter Plot
Data Recording Method
Data will be stored in CSV format for easy analysis and visualization.
Data Analysis Report
Time per move (s):

Displayed as: Histogram.
Analysis: Illustrates the distribution of move times, providing insights into player speed and decision-making patterns.
Win/Draw/Loss Rate:

Displayed as: Pie Chart.
Analysis: Shows the proportion of wins, draws, and losses, effectively tracking the overall player success rate.
Material Balance:

Displayed as: Line Graph.
Analysis: Visualizes changes in material balance over time, allowing for evaluation of positional advantage throughout the game.
Checks & Checkmates:

Presented as: Summary Statistics/Table.
Analysis: Summarizes the occurrences of checks and checkmates per game, highlighting attacking strategies and defensive effectiveness.
Game Duration / Moves:

Displayed as: Scatter Plot.
Analysis: Depicts the relationship between game duration and the number of moves, providing insights into overall game pacing.
Graphs Specification
Feature	Graph Type	Purpose
Time per move (s)	Histogram	To illustrate the distribution of move times.
Material Balance	Line Graph	To visualize changes in material advantage over time.
Game Duration / Moves	Scatter Plot	To analyze the relationship between game duration and number of moves.
Statistical Values for Checks & Checkmates
For this feature, the following values will be computed and presented in a summary table:

Total Count: The total number of check events (including checkmates) per game.
Average per Game: The mean number of checks per game.
Maximum: The highest number of checks recorded in any game.
Standard Deviation (SD): The variation in the number of checks across games.
These values will help highlight attacking strategies and defensive effectiveness.