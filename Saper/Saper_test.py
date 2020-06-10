import unittest
import tkinter as tk
import Saper

class MyGuiTest(unittest.TestCase):
    def setUp(self):
        self.gui = Saper.MyGui(tk.Tk())
    
    def count_mines(self):
        count = 0
        for column_in_row in self.gui._MyGui__play._play_zone:
            for element_in_column in column_in_row:
                if element_in_column._mina:
                    count += 1
        return count

    def test_mygui_input_spam(self):
        self.setUp()
        self.gui.start_try('spam','spam','spam')
        self.assertEqual(self.gui._MyGui__play, None)

    def test_mygui_input_good_numbers(self):
        self.setUp()
        self.gui.start_try(8, 8, 12)
        self.assertEqual(type(self.gui._MyGui__play), Saper.PlayZone)

    def test_mygui_input_wrong_numbers(self):
        self.setUp()
        self.gui.start_try(100, -800, 1)
        self.assertEqual(self.gui._MyGui__play, None)

    def test_mygui_input_full_in_mines(self):
        self.setUp()
        self.gui.start_try(8, 8, 64)
        self.assertEqual(self.gui._MyGui__play, None)

    def test_playzone_start_square(self):
        self.setUp()
        self.gui.start_try(5, 5, 3)
        self.assertEqual(self.gui._MyGui__play._PlayZone__plansza_rows, 5)
        self.assertEqual(self.gui._MyGui__play._PlayZone__plansza_columns, 5)
        self.assertEqual(self.gui._MyGui__play._PlayZone__plansza_mines, 3)
        self.assertEqual(int(self.gui._MyGui__play._points_left.get()), 3)
        self.assertEqual(self.gui._MyGui__play._points_left_real, 3)
        self.assertEqual(self.gui._MyGui__play._points_left_not, 22)
        self.assertEqual(len(self.gui._MyGui__play._play_zone), 5)
        self.assertEqual(len(self.gui._MyGui__play._play_zone[0]), 5)
        self.assertEqual(self.count_mines(), 3)

    def test_playzone_start_rectangle(self): 
        self.setUp()
        self.gui.start_try(2, 7, 13)
        self.assertEqual(self.gui._MyGui__play._PlayZone__plansza_rows, 2)
        self.assertEqual(self.gui._MyGui__play._PlayZone__plansza_columns, 7)
        self.assertEqual(self.gui._MyGui__play._PlayZone__plansza_mines, 13)
        self.assertEqual(int(self.gui._MyGui__play._points_left.get()), 13)
        self.assertEqual(self.gui._MyGui__play._points_left_real, 13)
        self.assertEqual(self.gui._MyGui__play._points_left_not, 1)
        self.assertEqual(len(self.gui._MyGui__play._play_zone), 2)
        self.assertEqual(len(self.gui._MyGui__play._play_zone[0]), 7)
        self.assertEqual(self.count_mines(), 13)

    def test_playzone_play_flag(self):
        self.setUp()
        self.gui.start_try(5, 5, 3)

        for column_in_row in self.gui._MyGui__play._play_zone:
            for element_in_column in column_in_row:
                if element_in_column._mina:
                    element_in_column.set_flag(self.gui._MyGui__play)

        self.assertEqual(self.gui._MyGui__text.get(), 'Udało się!')
        for column_in_row in self.gui._MyGui__play._play_zone:
            for element_in_column in column_in_row:
                self.assertEqual(element_in_column._visible, True)
        self.assertEqual(self.gui._MyGui__play._stop, True)

    def test_playzone_play_check(self):
        self.setUp()
        self.gui.start_try(5, 5, 3)

        for column_in_row in self.gui._MyGui__play._play_zone:
            for element_in_column in column_in_row:
                if not element_in_column._mina:
                    element_in_column.check_tile(element_in_column._Tile__row,
                                                 element_in_column._Tile__column,
                                                 self.gui._MyGui__play)

        self.assertEqual(self.gui._MyGui__text.get(), 'Udało się!')
        for column_in_row in self.gui._MyGui__play._play_zone:
            for element_in_column in column_in_row:
                self.assertEqual(element_in_column._visible, True)
        self.assertEqual(self.gui._MyGui__play._stop, True)

    def test_playzone_play_fail(self):
        self.setUp()
        self.gui.start_try(5, 5, 3)

        for column_in_row in self.gui._MyGui__play._play_zone:
            if not self.gui._MyGui__play._stop:
                for element_in_column in column_in_row:
                    if element_in_column._mina:
                        element_in_column.check_tile(element_in_column._Tile__row,
                                                     element_in_column._Tile__column,
                                                     self.gui._MyGui__play)
                        break

        self.assertEqual(self.gui._MyGui__text.get(), 'Przegrana!')
        for column_in_row in self.gui._MyGui__play._play_zone:
            for element_in_column in column_in_row:
                self.assertEqual(element_in_column._visible, True)
        self.assertEqual(self.gui._MyGui__play._stop, True)

if __name__ == '__main__':
    unittest.main()
