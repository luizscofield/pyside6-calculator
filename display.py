from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from utils import is_number_or_dot
from variables import BIG_FONT_SIZE, TEXT_MARGIN, MININUM_WIDTH

class Display(QLineEdit):
  equal_triggered = Signal()
  delete_triggered = Signal()
  clear_triggered = Signal()
  operator_triggered = Signal(str)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.config_style()

  def config_style(self) -> None:
    self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
    self.setMinimumHeight(BIG_FONT_SIZE * 2)
    self.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.setMinimumWidth(MININUM_WIDTH)

    margins = [TEXT_MARGIN for _ in range(4)]
    self.setTextMargins(*margins)

  def keyPressEvent(self, event: QKeyEvent) -> None:
    key = event.key()
    text = event.text().strip()
    KEYS = Qt.Key

    is_negative_number = True if self.text() == '' and text == '-' else False

    is_enter = key in (KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal)
    is_delete = key in (KEYS.Key_Backspace, KEYS.Key_Delete, KEYS.Key_D)
    is_clear = key in (KEYS.Key_Escape, KEYS.Key_C)
    is_operator = text in '+-x/^'

    if is_enter:
      self.equal_triggered.emit()
      return event.ignore()

    if is_delete:
      self.delete_triggered.emit()
      return event.ignore()

    if is_clear:
      self.clear_triggered.emit()
      return event.ignore()

    if text == '':
      return event.ignore()
    
    if is_number_or_dot(text):
      
      if '.' in self.text() and '.' in text:
        return event.ignore()
      
      return super().keyPressEvent(event)
    
    if is_operator:
      self.operator_triggered.emit(text)

    # The line below is commented on purpose.
    # The keyPressEvent method is being overwritten here.
    # Since the original function is not being returned, 
    # the keys will not be written to the display.
    # But we can still react to the pressing of keys.
    # return super().keyPressEvent(event)