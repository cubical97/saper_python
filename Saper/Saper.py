import tkinter as tk
#import Gui as mygui

class MyGui():
    def __init__(self, okno):
        self.__okno = okno
        self.__okno.title('Saper')
        self.__plansza_n = 8      #default n = 8
        self.__plansza_m = 8      #default m = 8
        self.__plansza_mina = 12  #default mines = 12
        self.__play=None

        self.__text = tk.StringVar()#######
        self.__text.set("Wpisz wartości")############

    def __str__(self):
        return 'MyGui'

    def PlayZone(self):
        if self.__play:
            for i in self.__play:
                i.destroy()
            self.__play.clear() 
        self.__play=[]
        __COLUMN_SET=5
        p=0
        for i in range(0, self.__plansza_m):
            for j in range(0, self.__plansza_n):
                self.__play.append(tk.Button(self.__okno, text = ' ', bg='light yellow', height=1 , width=2))
                self.__play[p].grid(row=i, column = j+__COLUMN_SET)
                p += 1
        pass

    def StartTry(self, sx=8, sy=8, smina=12):
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
            print('Błąd\n')
            print(e.args)
            raise
        else:
            self.__plansza_n=int(sx)
            self.__plansza_m=int(sy)
            self.__plansza_mina=int(smina)

            #plansza
            self.PlayZone()
            self.__text.set("Start!")
        pass

    def Menu(self):
        str_e1=tk.StringVar(value='')
        str_e2=tk.StringVar(value='')
        str_e3=tk.StringVar(value='')

        label1 = tk.Label(self.__okno, text = 'rozmiar:')
        label2 = tk.Label(self.__okno, text = 'miny:')
        label3 = tk.Label(self.__okno, textvariable=self.__text)

        entry1 = tk.Entry(self.__okno, textvariable=str_e1)
        entry2 = tk.Entry(self.__okno, textvariable=str_e2)
        entry3 = tk.Entry(self.__okno, textvariable=str_e3)

        button1 = tk.Button(self.__okno, text = 'Start', command = lambda: self.StartTry(entry1.get(), entry2.get(), entry3.get()))
        button2 = tk.Button(self.__okno, text = 'Exit', command = self.__okno.destroy)

        label1.grid(row=0, column=0)
        entry1.grid(row=0, column=1)
        entry2.grid(row=1, column=1)
        label2.grid(row=2, column=0)
        entry3.grid(row=2, column=1)
        button1.grid(row=3, column=0)
        button2.grid(row=3, column=1)
        label3.grid(row=4, column=0)       

def main():

    okno=tk.Tk()
    gui=MyGui(okno)

    gui.Menu()

    okno.mainloop()


if __name__ == '__main__':
    main()
