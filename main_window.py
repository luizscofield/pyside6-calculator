from sys import argv
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtGui import QIcon
from variables import ICON_PATH

class MainWindow(QMainWindow):
  def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
    super().__init__(parent, *args, **kwargs)

    # Layout configuration
    self.central_widget = QWidget()
    self.v_layout = QVBoxLayout()
    self.central_widget.setLayout(self.v_layout)
    self.setCentralWidget(self.central_widget)
    
    # Window Title
    self.setWindowTitle('Calculator')

  def adjust_fixed_size(self):
    # Window fixed size configurations
    self.adjustSize()
    self.setFixedSize(self.width(), self.height())

  def add_widget_to_vlayout(self, widget: QWidget):
    # Adds widgets to vertical layout
    self.v_layout.addWidget(widget)

  def make_msg_box(self):
    return QMessageBox(self)