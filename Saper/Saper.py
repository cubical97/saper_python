import tkinter as tk
import random as rd
import time as tm

######## pole
class Tile():
    def __init__(self, okno):
        self.__blockcolor = tk.StringVar()
        self.__blockcolor.set('light yellow')
        self.__visible = 0
        self.block=tk.Button(okno, text = ' ', bg=self.__blockcolor.get(), height=1 , width=2)
        self.mina=0
        self.check=0
        self.war=0

    def Set_visible(self): #pokazanie wartości sąsiedztwa
        if not self.mina:
            self.block.configure(text=str(self.war))
        else:
            self.block.configure(text='X')

    def Cheat2(self, color='light yellow'): #podejżenie min
        if not self.__visible:
            if self.mina:
                self.block.configure(bg='yellow')
            self.__visible=1
        else:
            self.block.configure(bg='light yellow')
            self.__visible=0

######### plansza
class PlayZone():
    def __init__(self, okno, column):
        self.__okno = okno
        self.__plansza_n = 0
        self.__plansza_m = 0
        self.__plansza_mina = 0
        self.__column_start=column    # column - miejsce rozpoczęcia rysowania planszy
        self.__play_zone=None         # przechowuje pola

    def Remove_play_zone(self): #usunięcie planszy
        for i in self.__play_zone:
            for j in i:
                j.block.destroy()
            i.clear()
        self.__play_zone.clear() 

    def Cheat1(self):
        for i in self.__play_zone:
            for j in i:
                j.Cheat2() #widzenie min
                #j.Set_visible()

    def Set_mines(self): #ustawienie min
        def add_war(i, j):
            if i > 0 and i < self.__plansza_m and j > 0 and j < self.__plansza_n:
                if self.__play_zone[i][j].mina:
                    return 1
            return 0

        i=0
        while i<self.__plansza_mina:
            x=rd.randint(0, self.__plansza_m -1) #ustawienie losowo min
            y=rd.randint(0, self.__plansza_n -1) #ustawienie losowo min
            if not self.__play_zone[x][y].mina:
                self.__play_zone[x][y].mina=1
                i+=1
        i=0
        while i<self.__plansza_m:
            j=0
            while j<self.__plansza_n:
                war=0
                war+=add_war( i-1, j -1)
                war+=add_war( i-1, j   )
                war+=add_war( i-1, j +1)
                war+=add_war( i  , j -1)
                war+=add_war( i  , j +1)
                war+=add_war( i+1, j -1)
                war+=add_war( i+1, j   )
                war+=add_war( i+1, j +1)

                self.__play_zone[i][j].war=war
                j+=1
            i+=1

    def Set_play_zone(self, n, m, miny): #ustawienie nowej planszy / resetowanie planszy
        self.__plansza_n = n
        self.__plansza_m = m
        self.__plansza_mina = miny

        if self.__play_zone:
            self.Remove_play_zone()
        self.__play_zone=[]
        p1=0
        for i in range(0, self.__plansza_m):
            p2=0
            self.__play_zone.append([])
            for j in range(0, self.__plansza_n):
                self.__play_zone[p1].append(Tile(self.__okno))
                self.__play_zone[p1][p2].block.grid(row=i, column = j+self.__column_start)
                p2 += 1
            p1 += 1
        self.Set_mines()

    def Check_tile(self, a, b): #działanie po kliknięciu w pole
        # sprawdzenie czy mina

        # sprawdzenie pól sąsiednich

        pass

######### menu
class MyGui():
    def __init__(self, okno):
        self.__okno = okno
        self.__okno.title('Saper')
        self.__plansza_n = 8      #default n = 8
        self.__plansza_m = 8      #default m = 8
        self.__plansza_mina = 12  #default mines = 12
        self.__play=None

        self.__text = tk.StringVar()
        self.__text.set("Wpisz wartości")

    def StartPlay(self): #rozpoczęcie
        COLUMN_SET=5
        if not self.__play:
            self.__play=PlayZone(self.__okno, COLUMN_SET)
        self.__play.Set_play_zone(self.__plansza_n, self.__plansza_m, self.__plansza_mina)

    def StartTry(self, sx=8, sy=8, smina=12): #sprawdzenie przed rozpoczęciem
        try:
            sn=int(sx)
            sm=int(sy)
            smi=int(smina)
            if(sn<2 or sn>15):
                self.__text.set('Wpisz wartość rozmiaru od 2 do 15')
                return
            if(sm<2 or sm>15):
                self.__text.set('Wpisz wartość rozmiaru od 2 do 15')
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
            raise
        else:
            self.__plansza_n=int(sx)
            self.__plansza_m=int(sy)
            self.__plansza_mina=int(smina)

            #plansza
            self.StartPlay()
            self.__text.set("Start!")
        pass

    def Cheat(self):
        if self.__play:
            self.__play.Cheat1()

    def Menu(self): ##główne okno
        str_e1=tk.StringVar(value='')
        str_e2=tk.StringVar(value='')
        str_e3=tk.StringVar(value='')

        label1 = tk.Label(self.__okno, text = 'rozmiar:')
        label2 = tk.Label(self.__okno, text = 'miny:')
        label3 = tk.Label(self.__okno, textvariable=self.__text)

        entry1 = tk.Entry(self.__okno, textvariable=str_e1)
        entry2 = tk.Entry(self.__okno, textvariable=str_e2)
        entry3 = tk.Entry(self.__okno, textvariable=str_e3)

        button1 = tk.Button(self.__okno, text = 'Start', width=15, command = lambda: self.StartTry(entry1.get(), entry2.get(), entry3.get()))
        button2 = tk.Button(self.__okno, text = 'Exit', width=15, command = self.__okno.destroy)
        button3 = tk.Button(self.__okno, text = 'Cheat', bg='pink1', command = lambda: self.Cheat())

        label1.grid(row=0, column=0)
        entry1.grid(row=0, column=1)
        entry2.grid(row=1, column=1)
        label2.grid(row=2, column=0)
        entry3.grid(row=2, column=1)
        button1.grid(row=3, column=0)
        button2.grid(row=3, column=1)
        label3.grid(row=4, column=0, columnspan=2) 
        button3.grid(row=5, column=0)

def main(): #start aplikacji

    okno=tk.Tk()
    gui=MyGui(okno)

    gui.Menu()

    okno.mainloop()


if __name__ == '__main__':
    main()
