import os

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to print the game board
def print_board(board):
    print("  0 1 2")
    for i, row in enumerate(board):
        print(f"{i} {' '.join(row)}")

# Function to check if there is a winner
def check_winner(board, player):
    win_conditions = [
        [(0, 0), (0, 1), (0, 2)],  # Top row
        [(1, 0), (1, 1), (1, 2)],  # Middle row
        [(2, 0), (2, 1), (2, 2)],  # Bottom row
        [(0, 0), (1, 0), (2, 0)],  # Left column
        [(0, 1), (1, 1), (2, 1)],  # Middle column
        [(0, 2), (1, 2), (2, 2)],  # Right column
        [(0, 0), (1, 1), (2, 2)],  # Diagonal
        [(0, 2), (1, 1), (2, 0)]   # Anti-diagonal
    ]
    for condition in win_conditions:
        if all(board[x][y] == player for x, y in condition):
            return True
    return False

# Function to check if the board is full
def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    
    while True:
        clear_screen()
        print_board(board)
        print(f"player {current_player}'s turn")
        
        try:
            row = int(input("enter the row (0, 1, 2): "))
            col = int(input("enter the column (0, 1, 2): "))
        except ValueError:
            print("invalid input. please enter numbers only.")
            continue
        
        if row not in [0, 1, 2] or col not in [0, 1, 2]:
            print("invalid coordinates. please enter 0, 1, or 2.")
            continue
        
        if board[row][col] != ' ':
            print("cell already taken. please choose another one.")
            continue
        
        board[row][col] = current_player
        
        if check_winner(board, current_player):
            clear_screen()
            print_board(board)
            print(f"player {current_player} wins!")
            break
        
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("it's a draw!")
            break
        
        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    main()
