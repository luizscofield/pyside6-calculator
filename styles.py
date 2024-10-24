import qdarkstyle
from PySide6.QtWidgets import QApplication
from variables import (DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR,
                       PRIMARY_COLOR)
 
qss = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
        border-radius: 5px;
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
"""
 
 
def setup_theme(app: QApplication):
    # Apply Dark Theme
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
 
    # Using additional stylesheet
    app.setStyleSheet(app.styleSheet() + qss)