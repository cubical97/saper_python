from tkinter import *

class MyGui():
    def __init__(self, okno):
        self.__okno = okno
        self.__okno.title('Saper')

    def __str__(self):
        return self.__ret

    def Start(self,sx=0,sy=0):
        x=sx
        y=sy
        print(x,y)
        pass

    def Menu(self):
        label1 = Label(self.__okno, text = 'rozmiar:')
        label2 = Label(self.__okno, text = 'miny:')
        entry1 = Entry(self.__okno, width = 50)
        entry2 = Entry(self.__okno, width = 50)
        entry3 = Entry(self.__okno, width = 50)
        button1 = Button(self.__okno, text = 'Start', command = lambda: self.Start())
        button2 = Button(self.__okno, text = 'exit', command = self.__okno.destroy)

        label1.pack()
        entry1.pack()
        entry2.pack()
        label2.pack()
        entry3.pack()
        button1.pack()
        button2.pack()


