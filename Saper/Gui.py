from tkinter import *

class MyGui():
    def __init__(self, okno):
        self.__okno = okno
        self.__okno.title('Saper')
        self.__plansza_n = 8
        self.__plansza_m = 8
        self.__plansza_mina = 12

    def __str__(self):
        return self.__ret

    def Start(self, sx=8, sy=8, smina=12):
        try:
            sn=int(sx)
            sm=int(sy)
            smi=int(smina)

            if(sn<2 or sn>15):
                raise ValueError
            if(sm<2 or sn>15):
                raise ValueError
            if(smi<1 or smi>sm*sn-1):
                raise ValueError

        except ValueError as e:
            print('Błąd\nWpisz liczby od 2 do 15!')
        except Exception as e:
            print('Błąd\n')
            print(e.args)
            raise
        else:
            self.__plansza_n=sx
            self.__plansza_m=sy
            self.__plansza_mina=smina
            print(self.__plansza_n, self.__plansza_m, self.__plansza_mina)
        pass

    def Menu(self):
        n = StringVar()
        m = StringVar()
        mina = StringVar()

        label1 = Label(self.__okno, text = 'rozmiar:')
        label2 = Label(self.__okno, text = 'miny:')
        entry1 = Entry(self.__okno, textvariable = n)#, width = 25
        entry2 = Entry(self.__okno, textvariable = m)#, width = 25
        entry3 = Entry(self.__okno, textvariable = mina)#, width = 25
        button1 = Button(self.__okno, text = 'Start', command = lambda: self.Start(entry1.get(), entry2.get(), entry3.get()))
        button2 = Button(self.__okno, text = 'exit', command = self.__okno.destroy)

        label1.grid(row=0, column=0)
        entry1.grid(row=0, column=1)
        entry2.grid(row=0, column=2)
        label2.grid(row=1, column=0)
        entry3.grid(row=1, column=1)
        button1.grid(row=2, column=0)
        button2.grid(row=2, column=1)


