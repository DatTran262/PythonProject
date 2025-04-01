"""Common styles for the application UI components"""

# Common button styles
PRIMARY_BUTTON = """
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
"""

DANGER_BUTTON = """
    QPushButton {
        background-color: #f44336;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #da190b;
    }
"""

WARNING_BUTTON = """
    QPushButton {
        background-color: #FF9800;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #F57C00;
    }
"""

SMALL_DANGER_BUTTON = """
    QPushButton {
        background-color: #f44336;
        color: white;
        border: none;
        padding: 4px 8px;
        border-radius: 2px;
    }
    QPushButton:hover {
        background-color: #da190b;
    }
"""

SECONDARY_BUTTON = """
    QPushButton {
        background-color: #2196F3;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #1976D2;
    }
"""

# Menu item styles
MENU_ITEM_STYLE = """
    QFrame {
        background-color: white;
        border-radius: 8px;
        padding: 8px;
        margin: 5px;
    }
    QLabel {
        color: #333;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 4px;
        min-width: 60px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QSpinBox {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 2px;
    }
"""

# Header label styles
HEADER_LABEL = """
    QLabel {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        padding: 10px;
        background-color: #ecf0f1;
        border-radius: 4px;
        margin-bottom: 10px;
    }
"""

# Title label style
TITLE_LABEL = """
    font-size: 18px;
    font-weight: bold;
    margin: 10px;
"""

# Main window styles
MAIN_WINDOW = """
    QMainWindow {
        background-color: #f5f6fa;
    }
    QWidget {
        font-family: 'Segoe UI', Arial, sans-serif;
    }
"""

# Fixed width for standard buttons
BUTTON_FIXED_WIDTH = 100