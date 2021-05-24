
import sys
import pandas as pd
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from enum import Enum
from datetime import datetime

CLEAR = "Clear"
BACKSPACE = "Backspace"
EVALUATE = "Evaluate"
CSV_HEADER = ["timestamp", "key", "input_type"]

ALLOWED_KEYS = "0123456789+-*/,."
app = QtWidgets.QApplication(sys.argv)


class InputType(Enum):
    """
    enum used to differentiate between the two input methods
    """
    BUTTON = 1
    KEYBOARD = 2


class Logger:

    df = ()

    def __init__(self):
        super().__init__()
        self.init_dataframe()
        self.experiment_running = False

    def init_dataframe(self):
        self.df = pd.DataFrame(columns=CSV_HEADER)

    def add_log_entry(self, user_input, input_type):

        if not self.experiment_running:
            self.experiment_running = True
            self.df = self.df.append({
                'timestamp': datetime.now(),
                'key': "EXPERIMENT_START",
                'input_type': input_type.name
            }, ignore_index=True)

        if user_input == CLEAR:
            self.experiment_running = False
            self.df = self.df.append({
                'timestamp': datetime.now(),
                'key': "EXPERIMENT_END",
                'input_type': input_type.name
            }, ignore_index=True)

        else:
            self.df = self.df.append({
                'timestamp': datetime.now(),
                'key': user_input,
                'input_type': input_type.name
            }, ignore_index=True)

    def print_logs(self):
        self.df.to_csv(sys.stdout, index=False)


class Calculator(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.win = uic.loadUi("calculator.ui")
        self.logger = Logger()
        self.set_click_listeners()
        self.add_background_color()
        self.win.show()
        self.win.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.win.keyPressEvent = self.keyPressEvent
        self.win.closeEvent = self.closeEvent

    def backspace(self, input_type):
        self.win.eval_text.setText(self.win.eval_text.toPlainText()[:-1])
        self.logger.add_log_entry(BACKSPACE, input_type)

    def clear(self, input_type):
        self.win.eval_text.setText("")
        self.logger.add_log_entry(CLEAR, input_type)

    def add_input_to_text(self, user_input, input_type):
        self.win.eval_text.setText(self.win.eval_text.toPlainText() + str(user_input))
        self.logger.add_log_entry(user_input, input_type)

    def evaluate(self, input_type):
        # replace ',' with '.'
        expression = self.win.eval_text.toPlainText().replace(",", ".")

        self.logger.add_log_entry(EVALUATE, input_type)

        try:
            self.win.eval_text.setText(str(eval(expression)))
        except (SyntaxError, NameError):
            sys.stderr.write("No valid statement. Please check your input!")

    def set_click_listeners(self):
        """
        sets the click listeners for all buttons
        """
        self.win.button_0.clicked.connect(lambda: self.add_input_to_text(0, InputType.BUTTON))
        self.win.button_1.clicked.connect(lambda: self.add_input_to_text(1, InputType.BUTTON))
        self.win.button_2.clicked.connect(lambda: self.add_input_to_text(2, InputType.BUTTON))
        self.win.button_3.clicked.connect(lambda: self.add_input_to_text(3, InputType.BUTTON))
        self.win.button_4.clicked.connect(lambda: self.add_input_to_text(4, InputType.BUTTON))
        self.win.button_5.clicked.connect(lambda: self.add_input_to_text(5, InputType.BUTTON))
        self.win.button_6.clicked.connect(lambda: self.add_input_to_text(6, InputType.BUTTON))
        self.win.button_7.clicked.connect(lambda: self.add_input_to_text(7, InputType.BUTTON))
        self.win.button_8.clicked.connect(lambda: self.add_input_to_text(8, InputType.BUTTON))
        self.win.button_9.clicked.connect(lambda: self.add_input_to_text(9, InputType.BUTTON))
        self.win.button_decimal.clicked.connect(lambda: self.add_input_to_text(".", InputType.BUTTON))

        self.win.button_multiply.clicked.connect(lambda: self.add_input_to_text('*', InputType.BUTTON))
        self.win.button_divide.clicked.connect(lambda: self.add_input_to_text('/', InputType.BUTTON))
        self.win.button_subtract.clicked.connect(lambda: self.add_input_to_text('-', InputType.BUTTON))
        self.win.button_add.clicked.connect(lambda: self.add_input_to_text('+', InputType.BUTTON))

        self.win.button_clear.clicked.connect(lambda: self.clear(InputType.BUTTON))
        self.win.button_backspace.clicked.connect(lambda: self.backspace(InputType.BUTTON))
        self.win.button_evaluate.clicked.connect(lambda: self.evaluate(InputType.BUTTON))

    def keyPressEvent(self, event):
        """
        checks for key presses and reacts accordingly
        """

        if QtGui.QKeySequence(event.key()).toString() in ALLOWED_KEYS:
            self.add_input_to_text(QtGui.QKeySequence(event.key()).toString(), InputType.KEYBOARD)

        # Key_Return = "Normal" Enter, Key_Enter = NumPad Enter
        elif event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.evaluate(InputType.KEYBOARD)
        elif event.key() == QtCore.Qt.Key_Backspace:
            self.backspace(InputType.KEYBOARD)

    def closeEvent(self, event):
        self.logger.print_logs()
        event.accept()

    def add_background_color(self):
        """
        Adds some background color to the buttons
        """
        self.win.button_0.setStyleSheet("background-color: lightblue")
        self.win.button_1.setStyleSheet("background-color: lightblue")
        self.win.button_2.setStyleSheet("background-color: lightblue")
        self.win.button_3.setStyleSheet("background-color: lightblue")
        self.win.button_4.setStyleSheet("background-color: lightblue")
        self.win.button_5.setStyleSheet("background-color: lightblue")
        self.win.button_6.setStyleSheet("background-color: lightblue")
        self.win.button_7.setStyleSheet("background-color: lightblue")
        self.win.button_8.setStyleSheet("background-color: lightblue")
        self.win.button_9.setStyleSheet("background-color: lightblue")
        self.win.button_decimal.setStyleSheet("background-color: lightblue")
        self.win.button_evaluate.setStyleSheet("background-color: orange")
        self.win.button_clear.setStyleSheet("background-color: red")


if __name__ == "__main__":
    calculator = Calculator()
    app.exec()
