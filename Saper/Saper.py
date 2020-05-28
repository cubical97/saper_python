import tkinter as tk
from random import seed, randint
from time import time_ns

TILE_COLOR=('AntiqueWhite1', 'AntiqueWhite2', 'gray85', 'gray80', 'gray65')

######## pole
class Tile():
    def __init__(self, play_pack, column, row):
        self.__blockcolor = tk.StringVar()
        self.__blockcolor.set(TILE_COLOR[0])
        self._visible = False
        self.__column = column
        self.__row = row
        self.block=tk.Button(play_pack._okno, text = ' ', bg=self.__blockcolor.get(), height=1, width=2)
        self.block.bind('<Button-1>', lambda none: self.check_tile(self.__column, self.__row, play_pack))
        self.block.bind('<Button-3>', lambda none: self.set_flag(play_pack))
        self._mina=False
        self._flaga=False
        self._wartosc=0

    def set_visible(self, mode=False): #pokazanie wartości pola
        if not self._mina:
            if self._wartosc:
                self.block.configure(text=str(self._wartosc))
                self.block.configure(bg=TILE_COLOR[3])
            else:
                self.block.configure(text='')
                self.block.configure(bg=TILE_COLOR[2])
        else:
            if mode:
                self.block.configure(text='F')
                self.block.configure(bg=TILE_COLOR[4], fg='blue')
            else:
                self.block.configure(text='X')
                self.block.configure(bg=TILE_COLOR[4], fg='red')
        self._visible=True

    def set_flag(self, play_pack): #pokazanie wartości pola
        if not self._visible and not self._flaga:
            self._flaga=True
            self._visible=True
            play_pack._points_left.set(str(int(play_pack._points_left.get())-1))
            self.block.configure(text='F')
            self.block.configure(bg=TILE_COLOR[3], fg='blue')
            if self._mina:
                play_pack._points_left_real-=1
        elif self._visible and self._flaga:
            self._flaga=False
            self._visible=False
            play_pack._points_left.set(str(int(play_pack._points_left.get())+1))
            self.block.configure(text='')
            self.block.configure(bg=TILE_COLOR[0], fg='black')
            if self._mina:
                play_pack._points_left_real+=1
        if not play_pack._points_left_real or not play_pack._points_left_not:
            if int(play_pack._points_left.get()) == play_pack._points_left_real:
                play_pack._text.set('Udało się!')#STOP :>
                if not play_pack._stop:
                    play_pack._stop=True
                    for row in play_pack._play_zone:
                        for column_element in row:
                            column_element.set_visible(True)

    def check_tile(self, a, b, play_pack): #działanie po kliknięciu w pole
        if a>=0 and b>=0 and a<len(play_pack._play_zone) and b<len(play_pack._play_zone[0]):
            if not play_pack._play_zone[a][b]._visible:
                play_pack._play_zone[a][b].set_visible()
                if play_pack._play_zone[a][b]._wartosc or play_pack._play_zone[a][b]._mina: # sprawdzenie czy mina
                    if play_pack._play_zone[a][b]._mina:
                        play_pack._text.set('Przegrana!')#STOP :<
                        for row in play_pack._play_zone:
                            for column_element in row:
                                column_element.set_visible()
                    else:
                        play_pack._points_left_not-=1
                else: # sprawdzenie pól sąsiednich
                    play_pack._points_left_not-=1
                    self.check_tile(a-1,b-1,play_pack)
                    self.check_tile(a-1,b  ,play_pack)
                    self.check_tile(a-1,b+1,play_pack)
                    self.check_tile(a  ,b-1,play_pack)
                    self.check_tile(a  ,b+1,play_pack)
                    self.check_tile(a+1,b-1,play_pack)
                    self.check_tile(a+1,b  ,play_pack)
                    self.check_tile(a+1,b+1,play_pack)
        if ((not play_pack._points_left_real) or (not play_pack._points_left_not)):
            if (int(play_pack._points_left.get()) == play_pack._points_left_real):
                play_pack._text.set('Udało się!')#STOP :>
                if not play_pack._stop:
                    play_pack._stop=True
                    for row in play_pack._play_zone:
                        for column_element in row:
                            column_element.set_visible(True)

    def cheat2(self): #podejżenie min
        if not self._visible:
            if self._mina:
                self.block.configure(bg=TILE_COLOR[1])

######### plansza
class PlayZone():
    def __init__(self, okno, column, points_left, text):
        self._okno = okno
        self.__plansza_columns = 0
        self.__plansza_rows = 0
        self.__plansza_mina = 0
        self._points_left = points_left #wyświetla pozostałe miny do oznaczenia
        self._points_left_real = 0      #pozostałe miny do oznaczenia, dla flagi, ukryte
        self._points_left_not = 0       #pozostałe miny do oznaczenia, dla wykopane, ukryte
        self._text = text
        self.__column_start=column      # - miejsce rozpoczęcia rysowania planszy
        self._play_zone=None            # - przechowuje pola planszy
        self._stop=False                # - zapobiega przycinaniu dla Tile.check_tile(...)

    def remove_play_zone(self): #usunięcie planszy
        for i in self._play_zone:
            for j in i:
                j.block.destroy()
            i.clear()
        self._play_zone.clear()
        self.__plansza_rows = 0
        self.__plansza_columns = 0
        self._points_left.set('')

    def cheat1(self):
        for i in self._play_zone:
            for j in i:
                j.cheat2() #widzenie min

    def set_mines(self): #ustawienie min
        def add_war(i, j):
            if i >= 0 and i < self.__plansza_rows and j >= 0 and j < self.__plansza_columns:
                if self._play_zone[i][j]._mina:
                    return 1
            return 0
        i=0
        seed(time_ns())
        while i<self.__plansza_mina:
            x=randint(0, self.__plansza_rows -1) #wybiera losowo row
            y=randint(0, self.__plansza_columns -1) #wybiera losowo column
            if not self._play_zone[x][y]._mina:
                self._play_zone[x][y]._mina=True
                i+=1
        for i in range(0, self.__plansza_rows):
            j=0
            for j in range(0, self.__plansza_columns):
                otocznie = 0
                otocznie += add_war( i-1, j -1)
                otocznie += add_war( i-1, j   )
                otocznie += add_war( i-1, j +1)
                otocznie += add_war( i  , j -1)
                otocznie += add_war( i  , j +1)
                otocznie += add_war( i+1, j -1)
                otocznie += add_war( i+1, j   )
                otocznie += add_war( i+1, j +1)
                self._play_zone[i][j]._wartosc = otocznie

    def set_play_zone(self, n, m, miny): #ustawienie nowej planszy / resetowanie planszy
        if self._play_zone:
            self.remove_play_zone()
        self.__plansza_columns = n
        self.__plansza_rows = m
        self.__plansza_mina = miny
        self._points_left_real = miny
        self._points_left_not = n*m-miny
        self._play_zone=[]
        for _row in range(0, self.__plansza_rows):
            wiersz=[]
            for _column in range(0, self.__plansza_columns):
                pole=Tile(self, _row, _column)
                pole.block.grid(row=_row, column = _column+self.__column_start)
                wiersz.append(pole)
            self._play_zone.append(wiersz)
        self.set_mines()
        self._stop=False

######### menu
class MyGui():
    def __init__(self, okno):
        self.__okno = okno
        self.__okno.title('Saper')
        self.__plansza_columns = 0
        self.__plansza_rows = 0
        self.__plansza_mina = 0
        self.__play=None

        self.__text = tk.StringVar()
        self.__text.set("Wpisz wartości")
        self.__points_left = tk.StringVar()

    def start_play(self): #rozpoczęcie
        COLUMN_START=5
        if not self.__play:
            self.__play=PlayZone(self.__okno, COLUMN_START, self.__points_left, self.__text)
        self.__play.set_play_zone(self.__plansza_columns, self.__plansza_rows, self.__plansza_mina)
        self.__points_left.set(self.__plansza_mina)

    def start_try(self, sx=8, sy=8, smina=12): #sprawdzenie przed rozpoczęciem
        MAX_ROWS = 15
        MAX_COLUMNS = 20
        try:
            sn=int(sx)
            sm=int(sy)
            smi=int(smina)
            if(sn<2 or sn>MAX_ROWS):
                self.__text.set(f'Wpisz wartość rzędu od 2 do {MAX_ROWS}')
                return
            if(sm<2 or sm>MAX_COLUMNS):
                self.__text.set(f'Wpisz wartość kolumn od 2 do {MAX_COLUMNS}')
                return
            if(smi<1 or smi>sm*sn-1):
                self.__text.set(f'Wpisz wartość min od 1 do {sn*sm-1}')
                return
        except ValueError as e:
            self.__text.set('Wpisz liczby!')
        except Exception as e:
            self.__text.set('Błąd')
            print('Błąd\n')
            print(e.args)
            raise e
        else:
            self.__plansza_columns=sm
            self.__plansza_rows=sn
            self.__plansza_mina=smi
            #plansza
            self.start_play()
            self.__text.set("Start!")

    def cheat(self):
        if self.__play:
            self.__play.cheat1()

    def menu(self): ##główne okno
        label1 = tk.Label(self.__okno, text = 'rozmiar:')
        label2 = tk.Label(self.__okno, text = 'miny:')
        label3 = tk.Label(self.__okno, textvariable=self.__text)
        label4 = tk.Label(self.__okno, text = 'pozostało:')
        label5 = tk.Label(self.__okno, textvariable=self.__points_left)

        entry1 = tk.Entry(self.__okno, textvariable=tk.StringVar(value=''))
        entry2 = tk.Entry(self.__okno, textvariable=tk.StringVar(value=''))
        entry3 = tk.Entry(self.__okno, textvariable=tk.StringVar(value=''))

        button1 = tk.Button(self.__okno, text = 'Start', width=15)
        button1.configure(command = lambda: self.start_try(entry1.get(), entry2.get(), entry3.get()))
        button2 = tk.Button(self.__okno, text = 'Exit', width=15, command = self.__okno.destroy)
        button3 = tk.Button(self.__okno, text = 'Cheat', bg='pink1', command = lambda: self.cheat())

        label1.grid(row=0, column=0)
        entry1.grid(row=0, column=1)
        entry2.grid(row=1, column=1)
        label2.grid(row=2, column=0)
        entry3.grid(row=2, column=1)
        button1.grid(row=3, column=0)
        button2.grid(row=3, column=1)
        label3.grid(row=4, column=0, columnspan=2)
        label4.grid(row=5, column=0, sticky = tk.E) 
        label5.grid(row=5, column=1, sticky = tk.W) 
        button3.grid(row=7, column=0)

def main(): #start aplikacji
    okno=tk.Tk()
    gui=MyGui(okno)
    gui.menu()
    okno.mainloop()

if __name__ == '__main__':
    main()
