from Saper import MyGui, PlayZone, Tile
import tkinter as tk
import unittest

class TestSaper(unittest.TestCase):
    
    def test_mygui_start(self):
        menu_1 = MyGui(tk.Tk())
        menu_1.start_try('spam','spam','spam')
        self.assertEqual(menu_1._MyGui__play, None)

        menu_2 = MyGui(tk.Tk())
        menu_2.start_try(8, 8, 12)
        self.assertEqual(type(menu_2._MyGui__play), PlayZone)

        menu_3 = MyGui(tk.Tk())
        menu_3.start_try(100, 800, -1)
        self.assertEqual(menu_3._MyGui__play, None)
    pass

    def test_playzone_start(self):
        def count_mines(play_zone):
            w = 0
            for column_in_row in play_zone._play_zone:
                for element_in_column in column_in_row:
                    if element_in_column._mina:
                        w += 1
            return w

        menu_4 = MyGui(tk.Tk())
        menu_4.start_try(5, 5, 3)
        self.assertEqual(menu_4._MyGui__play._PlayZone__plansza_rows, 5)
        self.assertEqual(menu_4._MyGui__play._PlayZone__plansza_columns, 5)
        self.assertEqual(menu_4._MyGui__play._PlayZone__plansza_mines, 3)
        self.assertEqual(int(menu_4._MyGui__play._points_left.get()), 3)
        self.assertEqual(menu_4._MyGui__play._points_left_real, 3)
        self.assertEqual(menu_4._MyGui__play._points_left_not, 22)
        self.assertEqual(len(menu_4._MyGui__play._play_zone), 5)
        self.assertEqual(len(menu_4._MyGui__play._play_zone[0]), 5)
        self.assertEqual(count_mines(menu_4._MyGui__play), 3)

        menu_5 = MyGui(tk.Tk())
        menu_5.start_try(2, 7, 13)
        self.assertEqual(menu_5._MyGui__play._PlayZone__plansza_rows, 2)
        self.assertEqual(menu_5._MyGui__play._PlayZone__plansza_columns, 7)
        self.assertEqual(menu_5._MyGui__play._PlayZone__plansza_mines, 13)
        self.assertEqual(int(menu_5._MyGui__play._points_left.get()), 13)
        self.assertEqual(menu_5._MyGui__play._points_left_real, 13)
        self.assertEqual(menu_5._MyGui__play._points_left_not, 1)
        self.assertEqual(len(menu_5._MyGui__play._play_zone), 2)
        self.assertEqual(len(menu_5._MyGui__play._play_zone[0]), 7)
        self.assertEqual(count_mines(menu_5._MyGui__play), 13)

    def test_playzone_play_flag(self):
        menu_6 = MyGui(tk.Tk())
        menu_6.start_try(5, 5, 3)

        for column_in_row in menu_6._MyGui__play._play_zone:
            for element_in_column in column_in_row:
                if element_in_column._mina:
                    element_in_column.set_flag(menu_6._MyGui__play)

        self.assertEqual(menu_6._MyGui__text.get(), 'Udało się!')
        for column_in_row in menu_6._MyGui__play._play_zone:
            for element_in_column in column_in_row:
                self.assertEqual(element_in_column._visible, True)
        self.assertEqual(menu_6._MyGui__play._stop, True)

    def test_playzone_play_check(self):
        menu_7 = MyGui(tk.Tk())
        menu_7.start_try(5, 5, 3)

        for column_in_row in menu_7._MyGui__play._play_zone:
            for element_in_column in column_in_row:
                if not element_in_column._mina:
                    element_in_column.check_tile(element_in_column._Tile__row, element_in_column._Tile__column, menu_7._MyGui__play)

        self.assertEqual(menu_7._MyGui__text.get(), 'Udało się!')
        for column_in_row in menu_7._MyGui__play._play_zone:
            for element_in_column in column_in_row:
                self.assertEqual(element_in_column._visible, True)
        self.assertEqual(menu_7._MyGui__play._stop, True)

    def test_playzone_play_fail(self):
        menu_8 = MyGui(tk.Tk())
        menu_8.start_try(5, 5, 3)

        for column_in_row in menu_8._MyGui__play._play_zone:
            if not menu_8._MyGui__play._stop:
                for element_in_column in column_in_row:
                    if element_in_column._mina:
                        element_in_column.check_tile(element_in_column._Tile__row, element_in_column._Tile__column, menu_8._MyGui__play)
                        break

        self.assertEqual(menu_8._MyGui__text.get(), 'Przegrana!')
        for column_in_row in menu_8._MyGui__play._play_zone:
            for element_in_column in column_in_row:
                self.assertEqual(element_in_column._visible, True)
        self.assertEqual(menu_8._MyGui__play._stop, True)

if __name__ == '__main__':
    unittest.main()