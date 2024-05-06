import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror

colors = {
    1: '#2c5d96', # синий
    2: '#31ad23', # зеленый
    3: '#c91c2e', # красный
    4: '#28119c', # темно-синий
    5: '#6b0a4e', # темно-розовый
    6: '#299693', # бирюзовый
    7: '#521f91', # фиолетовый
    8: '#38121a'  # бордовый
}

class MyButton(tk.Button):
    # Класс MyButton представляет кнопку в игре.

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        # Инициализация кнопки.
        super(MyButton, self).__init__(master, width=3, font='Calibri 20 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.cnt_bomb = 0
        self.config(background='#f0d1ef')
        self.is_open = False

    def __repr__(self):
        # Возвращает строковое представление кнопки.
        return f'MyButton {self.x} {self.y} {self.number} {self.is_mine}'


class MineSweeper:
    # Основной класс игры "Сапер".

    window = tk.Tk()
    row = 7
    columns = 10
    mines = 10
    is_game_over = False
    is_first_click = True
    window.title('MineSweeper')
    window.iconbitmap('C:/Users/Anastasia/PycharmProjects/pythonProject/images/icon1.ico')

    def __init__(self):
        # Инициализация игры.
        self.buttons = []

        for i in range(MineSweeper.row + 2):
            temp = []
            for j in range(MineSweeper.columns + 2):
                btn = MyButton(MineSweeper.window, x=i, y=j, )
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind('<Button-3>', self.right_click)  # правая кнопка (выбор бомбы)
                temp.append(btn)

            self.buttons.append(temp)

            self.flags = 0  # Инициализация счетчика флажков

            # Создаем фрейм для счетчиков мин и флажков
            self.bottom_frame = tk.Frame(self.window)
            self.bottom_frame.grid(row=MineSweeper.row + 2, columnspan=MineSweeper.columns + 2)

            # Метка "Мины"
            self.mines_label = tk.Label(self.bottom_frame, text="Мины:")
            self.mines_label.grid(row=0, column=0)

            # Метка для отображения количества мин
            self.mines_count_label = tk.Label(self.bottom_frame, text=MineSweeper.mines)
            self.mines_count_label.grid(row=0, column=1)

            # Метка "Флажки"
            self.flags_label = tk.Label(self.bottom_frame, text="Флажки:")
            self.flags_label.grid(row=0, column=2)

            # Метка для отображения количества флажков
            self.flags_count_label = tk.Label(self.bottom_frame, text="0")
            self.flags_count_label.grid(row=0, column=3)

    def right_click(self, event):
        # Обработка события правого клика мыши на кнопку.
        if MineSweeper.is_game_over:
            return
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
            cur_btn['disabledforeground'] = 'red'
            self.flags += 1  # Увеличиваем счетчик флажков у текущего экземпляра MineSweeper
            self.flags_count_label.config(text=str(self.flags))  # Обновляем отображение количества флажков
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'
            self.flags -= 1  # Уменьшаем счетчик флажков у текущего экземпляра MineSweeper
            self.flags_count_label.config(text=str(self.flags))  # Обновляем отображение количества флажков

    def check_win(self):
        # Проверка условия победы.
        safe_cells_count = (MineSweeper.row * MineSweeper.columns) - MineSweeper.mines
        opened_safe_cells = sum(1 for i in range(1, MineSweeper.row + 1) for j in range(1, MineSweeper.columns + 1) if
                                self.buttons[i][j].is_open and not self.buttons[i][j].is_mine)
        if safe_cells_count == opened_safe_cells:
            showinfo('ПОБЕДА!', 'Поздравляем, вы победили!')
            MineSweeper.is_game_over = True

    def change_settings(self, row_entry, column_entry, mines_entry):
        # Метод для изменения настроек игры.
        try:
            new_row = int(row_entry.get())
            new_column = int(column_entry.get())
            new_mines = int(mines_entry.get())

            if new_row < 1 or new_column < 1 or new_mines < 1:
                raise ValueError("Значения должны быть больше нуля")

            if new_mines >= new_row * new_column:
                raise ValueError("Количество мин должно быть меньше, чем общее количество ячеек")

            MineSweeper.row = new_row
            MineSweeper.columns = new_column
            MineSweeper.mines = new_mines

            # Перезапуск игры с новыми настройками
            self.reload()
        except ValueError as e:
            showerror("Ошибка", str(e))
    def click(self, clicked_bt: MyButton):
        # Обработка клика на кнопку.
        if MineSweeper.is_game_over:
            return None

        if MineSweeper.is_first_click:
            self.insert_mines(clicked_bt.number)
            self.cnt_mines_in()
            self.print_bt()
            MineSweeper.is_first_click = False

        if clicked_bt.is_mine:
            clicked_bt.config(text='💥', disabledforeground='black', background='red')
            clicked_bt.is_open = True
            MineSweeper.is_game_over = True
            showinfo('GAME OVER', 'Ой, кажется вы програли!')
            for i in range(1, MineSweeper.row + 1):
                for j in range(1, MineSweeper.columns + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '💥'
        else:
            color = colors.get(clicked_bt.cnt_bomb, "black")
            if clicked_bt.cnt_bomb:
                clicked_bt.config(text=clicked_bt.cnt_bomb, disabledforeground=color)
                clicked_bt.is_open = True
            else:
                self.breadth_search(clicked_bt)

        clicked_bt.config(state='disabled')  # чтобы кнопка нажималась один раз
        clicked_bt.config(relief=tk.SUNKEN)

        if not MineSweeper.is_game_over:
            self.check_win()

    def breadth_search(self, btn: MyButton):
        # чтобы пустые места открывались сразу
        queue = [btn]  # очередь из кнопок
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.cnt_bomb, "black")
            if cur_btn.cnt_bomb:
                cur_btn.config(text=cur_btn.cnt_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground='black')
            cur_btn.is_open = True
            cur_btn.config(state='disabled')  # чтобы кнопка нажималась один раз
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.cnt_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:  # проверяем только четыре ближайших соседа
                    for dy in [-1, 0, 1]:
                        if not abs(dx - dy) == 1:
                            continue

                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.row and \
                                1 <= next_btn.y <= MineSweeper.columns and next_btn not in queue:
                            queue.append(next_btn)
                self.check_win()

    def reload(self):
        # Перезагрузка игры.
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.creat_wdg()
        MineSweeper.is_first_click = True
        MineSweeper.is_game_over = False
        MineSweeper.flags = 0  # Обнуляем количество флажков
        self.flags_count_label.config(text=str(MineSweeper.flags))  # Обновляем отображение количества флажков
        self.mines_count_label.config(text=str(MineSweeper.mines))  # Обновляем отображение количества мин

    def create_settings(self):
        # Создание окна настроек.
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Настройки')
        tk.Label(win_settings, text='Количество строк').grid()
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, MineSweeper.row)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количество столбцов').grid()
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, MineSweeper.columns)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количество мин').grid()
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, MineSweeper.mines)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        save_btn = tk.Button(win_settings, text='Применить',
                             command=lambda: self.change_settings(row_entry, column_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20,)

    def creat_wdg(self):
        # Создает виджеты для отображения игрового поля и добавляет меню с командами.
        # Создание меню
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.create_settings)
        settings_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Файл', menu=settings_menu)

        # Создание кнопок игрового поля
        count = 1
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.columns + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='NWES')
                count += 1

        # Настройка геометрии для расширения игрового поля
        for i in range(1, MineSweeper.row + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)
        for i in range(1, MineSweeper.columns + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)

    def open_all_bt(self):
        # Открывает все кнопки игрового поля, отображая бомбы и цифры.
        for i in range(MineSweeper.row + 2):
            for j in range(MineSweeper.columns + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='💥', disabledforeground='black', background='red')
                elif btn.cnt_bomb in colors:
                    color = colors.get(btn.cnt_bomb, "black")
                    btn.config(text=btn.cnt_bomb, fg=color)

    def start(self):
        # Запускает игру, создавая виджеты и запуская основной цикл программы.
        self.creat_wdg()
        MineSweeper.window.mainloop()

    def print_bt(self):
        # Выводит текущее состояние игрового поля в консоль.
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.columns + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end=' ')
                else:
                    print(btn.cnt_bomb, end=' ')
            print()

    def insert_mines(self, number: int):
        # Размещает мины на игровом поле, исключая клетку с заданным номером.
        index_mines = self.get_mines_pl(number)
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.columns + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True

    def cnt_mines_in(self):
        # Вычисляет количество мин вокруг каждой клетки и сохраняет это значение в соответствующем атрибуте кнопки.
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.columns + 1):
                btn = self.buttons[i][j]
                cnt_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                cnt_bomb += 1
                btn.cnt_bomb = cnt_bomb

    @staticmethod
    def get_mines_pl(exclude_number: int):
        # Возвращает список индексов клеток, на которых будут размещены мины, исключая указанный номер клетки.
        indexes = list(range(1, MineSweeper.columns * MineSweeper.row + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:MineSweeper.mines]

game = MineSweeper()
game.start()
