import tkinter as tk
from random import seed, randint
from time import time_ns

TILE_COLOR=('AntiqueWhite1', 'AntiqueWhite2', 'gray85', 'gray80', 'gray65')

class Tile():
    """Przechowuje dane pola."""
    def __init__(self, play_pack, row, column):
        self._visible = False
        self.__row = row
        self.__column = column
        self._block = tk.Button(play_pack._okno, text = ' ', bg=TILE_COLOR[0], height=1, width=2)
        self._block.bind('<Button-1>', lambda none: self.check_tile(self.__row, self.__column, play_pack))
        self._block.bind('<Button-3>', lambda none: self.set_flag(play_pack))
        self._mina = False
        self._flaga = False
        self._wartosc = 0

    def set_visible(self, mode=False):
        """Zmienia widoczność pola.

        Jeśli (not self._mina), pokazuje liczbę sąsiednich min.
        Jeśli (self._mina), pokazuje minę.
        """
        if not self._mina:
            if self._wartosc:
                self._block.configure(text=str(self._wartosc))  
                self._block.configure(bg=TILE_COLOR[3])
            else:
                self._block.configure(text='')
                self._block.configure(bg=TILE_COLOR[2])
        else:
            if mode:
                self._block.configure(text='F')
                self._block.configure(bg=TILE_COLOR[4], fg='blue')
            else:
                self._block.configure(text='X')
                self._block.configure(bg=TILE_COLOR[4], fg='red')
        self._visible = True



    def set_flag(self, play_pack):
        """Ustawienie flagi - aktywowane poprzez kliknięcie.

        Zmienia wartośc licznika oznaczonych pól na planszy.
        Jeśli (self._mina), zmienia wartość licznika prawidłowo oznaczonych pól na planszy.
        """
        if not self._visible and not self._flaga:
            self._flaga = True
            self._visible = True
            play_pack._points_left.set(str(int(play_pack._points_left.get()) - 1))
            self._block.configure(text = 'F')
            self._block.configure(bg = TILE_COLOR[4], fg = 'blue')
            if self._mina:
                play_pack._points_left_real -= 1
        elif self._visible and self._flaga:
            self._flaga = False
            self._visible = False
            play_pack._points_left.set(str(int(play_pack._points_left.get())+1))
            self._block.configure(text='')
            self._block.configure(bg=TILE_COLOR[0], fg='black')
            if self._mina:
                play_pack._points_left_real += 1
        if not play_pack._points_left_real or not play_pack._points_left_not:
            if int(play_pack._points_left.get()) == play_pack._points_left_real:
                play_pack._text.set('Udało się!') #STOP
                if not play_pack._stop:
                    play_pack._stop = True
                    for column_in_row in play_pack._play_zone:
                        for element_in_column in column_in_row:
                            element_in_column.set_visible(True)

    def check_tile(self, row, column, play_pack):
        """Sprawdzenie pola - aktywowane poprzez kliknięcie.

        Jeśli (not self._mina), sprawdza sąsiednie pola.
        Zmienia wartość licznika pozostałych pól bez min.
        """
        if row >= 0 and column >= 0 and row < len(play_pack._play_zone) and column < len(play_pack._play_zone[0]):
            if not play_pack._play_zone[row][column]._visible:
                play_pack._play_zone[row][column].set_visible()
                if play_pack._play_zone[row][column]._wartosc or play_pack._play_zone[row][column]._mina: # sprawdzenie czy mina
                    if play_pack._play_zone[row][column]._mina:
                        play_pack._text.set('Przegrana!') #STOP
                        play_pack._stop = True
                        for column_in_row in play_pack._play_zone:
                            for element_in_column in column_in_row:
                                element_in_column.set_visible()
                    else:
                        play_pack._points_left_not -= 1
                else: # sprawdzenie pól sąsiednich
                    play_pack._points_left_not -= 1
                    self.check_tile(row-1, column-1, play_pack)
                    self.check_tile(row-1, column  , play_pack)
                    self.check_tile(row-1, column+1, play_pack)
                    self.check_tile(row  , column-1, play_pack)
                    self.check_tile(row  , column+1, play_pack)
                    self.check_tile(row+1, column-1, play_pack)
                    self.check_tile(row+1, column  , play_pack)
                    self.check_tile(row+1, column+1, play_pack)
        if ((not play_pack._points_left_real) or (not play_pack._points_left_not)):
            if (int(play_pack._points_left.get()) == play_pack._points_left_real):
                play_pack._text.set('Udało się!') #STOP
                if not play_pack._stop:
                    play_pack._stop = True
                    for column_in_row in play_pack._play_zone:
                        for element_in_column in column_in_row:
                            element_in_column.set_visible(True)

    def cheat2(self):
        """Zmienia kolor pola w trybie podglądania"""
        if not self._visible:
            if self._mina:
                self._block.configure(bg=TILE_COLOR[1])

class PlayZone():
    """Przechowuje dane planszy."""
    def __init__(self, okno, column_start, points_left, text):
        self._okno = okno
        self.__plansza_columns = 0
        self.__plansza_rows = 0
        self.__plansza_mines = 0
        self._points_left = points_left #wyświetla pozostałe miny do oznaczenia
        self._points_left_real = 0      #pozostałe miny do oznaczenia, dla flagi, ukryte
        self._points_left_not = 0       #pozostałe miny do oznaczenia, dla wykopane, ukryte
        self._text = text
        self.__column_start = column_start # - miejsce rozpoczęcia rysowania planszy
        self._play_zone = None       # - przechowuje pola planszy
        self._stop = False           # - zapobiega przycinaniu dla Tile.check_tile(...)

    def remove_play_zone(self):
        """Usuwa dane planszy."""
        for i in self._play_zone:
            for j in i:
                j._block.destroy()
            i.clear()
        self._play_zone.clear()
        self.__plansza_rows = 0
        self.__plansza_columns = 0
        self._points_left.set('')

    def cheat1(self):
        """Aktywuje zmianę koloru wszystkich pól w trybie podglądania"""
        for i in self._play_zone:
            for j in i:
                j.cheat2()

    def set_mines(self):
        """Losowo ustawia miny na planszy"""
        def if_mine(i, j):
            if i >= 0 and i < self.__plansza_rows and j >= 0 and j < self.__plansza_columns:
                if self._play_zone[i][j]._mina:
                    return 1
            return 0
        i=0
        seed(time_ns())
        while i < self.__plansza_mines:
            x=randint(0, self.__plansza_rows -1) #wybiera losowo row
            y=randint(0, self.__plansza_columns -1) #wybiera losowo column
            if not self._play_zone[x][y]._mina:
                self._play_zone[x][y]._mina=True
                i+=1
        for i in range(0, self.__plansza_rows):
            j=0
            for j in range(0, self.__plansza_columns):
                otocznie = 0
                otocznie += if_mine(i-1, j-1)
                otocznie += if_mine(i-1, j  )
                otocznie += if_mine(i-1, j+1)
                otocznie += if_mine(i  , j-1)
                otocznie += if_mine(i  , j+1)
                otocznie += if_mine(i+1, j-1)
                otocznie += if_mine(i+1, j  )
                otocznie += if_mine(i+1, j+1)
                self._play_zone[i][j]._wartosc = otocznie

    def set_play_zone(self, rows, columns, mines):
        """Ustawia nową planszę."""
        if self._play_zone:
            self.remove_play_zone()
        self.__plansza_columns = rows
        self.__plansza_rows = columns
        self.__plansza_mines = mines
        self._points_left.set(mines)
        self._points_left_real = mines
        self._points_left_not = rows * columns - mines
        self._play_zone=[]

        for _row in range(0, self.__plansza_rows):
            wiersz=[]
            for _column in range(0, self.__plansza_columns):
                pole=Tile(self, _row, _column)
                pole._block.grid(row=_row, column=_column + self.__column_start)
                wiersz.append(pole)
            self._play_zone.append(wiersz)

        self.set_mines()
        self._stop = False

class MyGui():
    """Menu aplikacji.
    
    Przechowuje okno wygenerowane w Tkinter.
    Zawiera pola z wprowaczeniem danych do gry.
    Zawiera pole komunikatu tekstowego.
    """
    def __init__(self, okno):
        self.__okno = okno
        self.__okno.title('Saper')
        self.__plansza_columns = 0
        self.__plansza_rows = 0
        self.__plansza_mines = 0
        self.__play=None

        self.__text = tk.StringVar()
        self.__text.set("Wpisz wartości")
        self.__points_left = tk.StringVar()

    def start_try(self, sx, sy, smina):
        """Sprawdza poprawność wprowadzonych danych"""
        MAX_ROWS = 15
        MAX_COLUMNS = 20
        COLUMN_START = 5 #miejsce rozpoczęcia rysowania planszy
        try:
            sn=int(sx)
            sm=int(sy)
            smi=int(smina)
            if(sn < 2 or sn > MAX_ROWS):
                self.__text.set(f'Wpisz wartość rzędu od 2 do {MAX_ROWS}')
                return
            if(sm < 2 or sm > MAX_COLUMNS):
                self.__text.set(f'Wpisz wartość kolumn od 2 do {MAX_COLUMNS}')
                return
            if(smi < 1 or smi > sm*sn-1):
                self.__text.set(f'Wpisz wartość min od 1 do {sn*sm-1}')
                return
        except ValueError as e:
            self.__text.set('Wpisz liczby!')
        except Exception as e:
            self.__text.set('Błąd')
            print('Błąd')
            print(e.args)
            raise e
        else:
            self.__plansza_columns = sm
            self.__plansza_rows = sn
            self.__plansza_mines = smi
            #plansza
            if not self.__play:
                self.__play=PlayZone(self.__okno, COLUMN_START, self.__points_left, self.__text)
            self.__play.set_play_zone(self.__plansza_columns, self.__plansza_rows, self.__plansza_mines)
            self.__points_left.set(self.__plansza_mines)
            self.__text.set("Start!")

    def cheat(self):
        """Aktywuje tryb podglądania.
        
        Oznacza pola z minami.
        """
        if self.__play:
            self.__play.cheat1()

    def menu(self):
        """Tworzy interfejs.

        Tworzy pola komunikatów, wprowadzania danych i przyciski, następnie ustawia je w oknie.
        """
        label1 = tk.Label(self.__okno, text='rozmiar:')
        label2 = tk.Label(self.__okno, text='miny:')
        label3 = tk.Label(self.__okno, textvariable=self.__text)
        label4 = tk.Label(self.__okno, text='pozostało:')
        label5 = tk.Label(self.__okno, textvariable=self.__points_left)

        entry1 = tk.Entry(self.__okno, textvariable=tk.StringVar(value=''))
        entry2 = tk.Entry(self.__okno, textvariable=tk.StringVar(value=''))
        entry3 = tk.Entry(self.__okno, textvariable=tk.StringVar(value=''))

        button1 = tk.Button(self.__okno, text='Start', width=15)
        button1.configure(command=lambda: self.start_try(entry1.get(), entry2.get(), entry3.get()))
        button2 = tk.Button(self.__okno, text='Exit', width=15, command=self.__okno.destroy)
        button3 = tk.Button(self.__okno, text='Cheat', bg='pink1', command=lambda: self.cheat())

        label1.grid(row=0, column=0)
        entry1.grid(row=0, column=1)
        entry2.grid(row=1, column=1)
        label2.grid(row=2, column=0)
        entry3.grid(row=2, column=1)
        button1.grid(row=3, column=0)
        button2.grid(row=3, column=1)
        label3.grid(row=4, column=0, columnspan=2)
        label4.grid(row=5, column=0, sticky=tk.E) 
        label5.grid(row=5, column=1, sticky=tk.W) 
        button3.grid(row=7, column=0)

def main():
    """Start aplikacji."""
    okno=tk.Tk()
    gui=MyGui(okno)
    gui.menu()
    okno.mainloop()

if __name__ == '__main__':
    main()
