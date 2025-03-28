from PyQt6.QtWidgets import QMessageBox

class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.setup_connections()

    def setup_connections(self):
        for i in range(3):
            for j in range(3):
                self.view.buttons[i][j].clicked.connect(
                    lambda checked, row=i, col=j: self.handle_move(row, col)
                )

    def handle_move(self, row, col):
        if self.model.make_move(row, col):
            # Update the button with current player's symbol
            self.view.update_button(row, col, self.model.board[row][col])
            
            if self.model.winner:
                self.view.update_status(f"Player {self.model.winner} Wins!")
                self.show_game_end_dialog(f"Player {self.model.winner} Wins!")
            elif self.model.game_over:
                self.view.update_status("Game Over - It's a Draw!")
                self.show_game_end_dialog("Game Over - It's a Draw!")
            else:
                self.view.update_status(f"Player {self.model.current_player}'s Turn")

    def show_game_end_dialog(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # If user clicks OK, reset the game
        if msg_box.exec() == QMessageBox.StandardButton.Ok:
            self.reset_game()

    def reset_game(self):
        self.model.reset_game()
        self.view.reset_board()
        self.view.update_status("Player X's Turn")