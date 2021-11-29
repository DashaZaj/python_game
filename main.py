import logging
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.config import Config

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '300')


class CrossZeroApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_model()
        self.buttons = []

    def init_model(self):
        self.symbol = 'X'
        self.desk = [
            ['0', '1', '2'],
            ['3', '4', '5'],
            ['6', '7', '8']]

    def build(self):
        gl = GridLayout(cols=3, rows=3)
        for i in range(9):
            btn = Button(font_size=70, on_press=self.btn_press)
            btn.n = i
            gl.add_widget(btn)
            self.buttons.append(btn)
        fl = FloatLayout()
        fl.add_widget(Button(text='reset', size_hint=(.45, .5), pos=(10, 70), on_press=self.reset))
        fl.add_widget(Button(text='close', size_hint=(.45, .5), pos=(160, 70), on_press=self.close))
        self.popup = Popup(title="", content=fl, auto_dismiss=False)
        return gl

    def btn_press(self, button):
        if button.text != '':
            return
        button.text = self.symbol

        row = button.n // 3
        col = button.n % 3
        self.desk[row][col] = self.symbol
        win = self.is_win()
        logging.info("win: '" + win + "' (" + str(win != '') + ")")
        winner = 'Крестики' if win == 'X' else ('Нолики' if win == 'O' else '')
        if winner != '':
            self.finish(f"{winner} победили!")
        elif self.desk_is_filled():
            self.finish("Ничья!")
        self.symbol = 'O' if self.symbol == 'X' else 'X'

    def finish(self, title):
        self.popup.title = title
        self.popup.open()

    def reset(self, source_btn):
        for btn in self.buttons:
            btn.text = ''
        self.init_model()
        self.popup.dismiss()

    def close(self, source_btn):
        self.stop()

    def desk_is_filled(self):
        for i in range(3):
            for j in range(3):
                if self.desk[i][j] != 'X' and self.desk[i][j] != 'O':
                    return False
        return True

    def is_win_row(self, row):
        if self.desk[row][0] == self.desk[row][1] and self.desk[row][1] == self.desk[row][2]:
            return self.desk[row][0]
        else:
            return ''

    def is_win_col(self, col):
        if self.desk[0][col] == self.desk[1][col] and self.desk[1][col] == self.desk[2][col]:
            return self.desk[0][col]
        else:
            return ''

    def is_win_diagonal1(self):
        if self.desk[0][0] == self.desk[1][1] and self.desk[1][1] == self.desk[2][2]:
            return self.desk[0][0]
        else:
            return ''

    def is_win_diagonal2(self):
        if self.desk[0][2] == self.desk[1][1] and self.desk[1][1] == self.desk[2][0]:
            return self.desk[0][2]
        else:
            return ''

    def is_win(self):
        for i in range(3):
            win = self.is_win_row(i)
            if win != '':
                return win
        for i in range(3):
            win = self.is_win_col(i)
            if win != '':
                return win
        win = self.is_win_diagonal1()
        if win != '':
            return win
        win = self.is_win_diagonal2()
        if win != '':
            return win
        return ''


if __name__ == '__main__':
    CrossZeroApp().run()
