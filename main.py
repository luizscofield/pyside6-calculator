from sys import argv
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from main_window import MainWindow
from display import Display
from info import Info
from styles import setup_theme
from buttons import Button, ButtonGrid
from variables import ICON_PATH

if __name__ == '__main__':

  # Setting up application window
  app = QApplication(argv)
  setup_theme(app)
  window = MainWindow()

  # Icon
  icon = QIcon(str(ICON_PATH))
  window.setWindowIcon(icon)
  app.setWindowIcon(icon)

  # Info
  info = Info('')
  window.add_widget_to_vlayout(info)

  # Display
  display = Display('')
  display.setPlaceholderText('Type here...')
  window.add_widget_to_vlayout(display)

  # Grid
  button_grid = ButtonGrid(display=display, info=info, window=window)
  window.v_layout.addLayout(button_grid)

  # Execute application
  window.adjust_fixed_size()
  window.show()
  app.exec()