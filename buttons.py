from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from math import pow
from utils import is_number_or_dot, is_valid_number
from variables import MEDIUM_FONT_SIZE

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from display import Display
  from info import Info
  from main_window import MainWindow

class Button(QPushButton):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.config_style()

  def config_style(self):
    font = self.font()
    font.setPixelSize(MEDIUM_FONT_SIZE)
    self.setFont(font)
    self.setMinimumSize(75,75)

class ButtonGrid(QGridLayout):
  def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow', *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._grid_mask = [
      [ 'C', '◀', '^',  '/' ],
      [ '7', '8',  '9',  'x' ],
      [ '4', '5',  '6',  '-' ],
      [ '1', '2',  '3',  '+' ],
      [ '',  '0',  '.',  '=' ],
    ]
    self._display = display
    self._info = info
    self._equation = ''
    self._num_left = None
    self._num_right = None
    self._operator = None
    self._window = window
    self.make_grid()

  def make_grid(self):
    self._display.equal_triggered.connect(self.equal_action)
    self._display.delete_triggered.connect(self._display.backspace)
    self._display.clear_triggered.connect(self.clear_action)
    self._display.operator_triggered.connect(self.operator_action)

    for i,row in enumerate(self._grid_mask):
      for j,column in enumerate(row):
        button = (Button(column))

        if not is_number_or_dot(column):
          button.setProperty('cssClass', 'specialButton')
          self.config_special_button(button)
        
        if column == '':
          pass
        elif column == '0':
          self.addWidget(button, 4, 0, 1, 2)
        else:
          self.addWidget(button, i, j)

        slot = self.make_slot(
          self.number_button_action,
          button_text=button.text()
        )
        self.button_clicked(button, slot)

  @property
  def equation(self):
    return self._equation
  
  @equation.setter
  def equation(self, value):
    self._equation = value
    self._info.setText(value)
    
  def config_special_button(self, button):
    button_text = button.text()
    
    if button_text == 'C':
      self.button_clicked(button, self.clear_action)

    elif button_text in ('+-x/^'):
      self.button_clicked(
        button,
        self.make_slot(
          self.operator_action,
          button_text,
        )
      )

    elif button_text == '=':
      self.button_clicked(
        button,
        self.make_slot(
          self.equal_action
        )
      )

    elif button_text == '◀':
      self.button_clicked(
        button,
        self._display.backspace
      )

  def make_slot(self, func, *args, **kwargs):
    @Slot(bool)
    def real_slot():
      func(*args, **kwargs)
    return real_slot
  
  def button_clicked(self, button: Button, slot):
    button.clicked.connect(slot)

  def number_button_action(self, button_text):

    new_display_value = self._display.text() + button_text

    if new_display_value == '-' and self.equation == '':
      pass
    elif not is_valid_number(new_display_value):
      return

    self._display.insert(button_text)

  def clear_action(self):
    self._equation = ''
    self._num_left = None
    self._num_right = None
    self._operator = None
    self.equation = ''
    self._display.clear()

  @Slot()
  def operator_action(self, text):
    is_negative_number = True if self._display.text() == '' and text == '-' else False
    if is_negative_number:
      self.number_button_action(text)
      return

    display_text = self._display.text()
    self.clear_action()

    # If there is no number defined prior to the operator
    if not is_valid_number(display_text) and self._num_left is None:
      return
    
    # Sets the left number and partial equation
    if self._num_left is None:
      self._num_left = float(display_text)

    self._operator = text

    self.equation = f'{self._num_left} {self._operator} ??'
  
  @Slot()
  def equal_action(self):

    if self._num_left == None:
      return

    display_text = self._display.text()

    if not is_valid_number(display_text):
      return
    
    self._num_right = float(display_text)
    self.equation = f'{self._num_left} {self._operator} {self._num_right}'

    result = 'error'
    try:
      if self._operator == 'x':
        result = self._num_left * self._num_right
      elif self._operator == '^':
        result = pow(self._num_left, self._num_right)
      else:
        result = eval(self.equation)
    except ZeroDivisionError:
      result = 'error'
      self.show_error('Division by zero.')
    except OverflowError:
      result = 'error'
      self.show_error('Result is too big. Overflow error.')

    if result == 'error':
      self._left = None
      return
    
    result = round(result, 5)
    self._num_left = result
    self._display.setText(str(result))
    self._info.setText(f'{self.equation} = {result}')
  
  def show_error(self, text):
    msg_box = self._window.make_msg_box()
    msg_box.setText(text)
    msg_box.setIcon(msg_box.Icon.Critical)
    msg_box.setStandardButtons(
      msg_box.StandardButton.Ok
    )
    msg_box.exec()