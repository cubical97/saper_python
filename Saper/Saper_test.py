from Saper import MyGui, PlayZone
import tkinter as tk
import unittest

class TestSaper(unittest.TestCase):
    
    def test_mygui_start(self):
        menu_1 = MyGui(tk.Tk())
        menu_1.start_try('spam','spam','spam')
        self.assertEqual(menu_1._MyGui__play, None)

        menu_2 = MyGui(tk.Tk())
        menu_2.start_try(8,8,12)
        self.assertEqual(type(menu_2._MyGui__play), PlayZone)

        menu_3 = MyGui(tk.Tk())
        menu_3.start_try(100,800,-1)
        self.assertEqual(menu_3._MyGui__play, None)
    pass

if __name__ == '__main__':
    unittest.main()