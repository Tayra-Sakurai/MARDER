from pathlib import Path
import unittest
from marder import load_csv_as_tex
from tkinter import filedialog

class Test_test_1(unittest.TestCase):
    def test_A(self):
        path = filedialog.askopenfilename(
            title='Picker',
            filetypes=(
                (
                    'Comma-Separated Values',
                    '*.csv'
                ),
            ),
            initialdir=Path('\\\\ThinkPadX13\\C$\\Users\\taira\\OneDrive')
        )
        self.fail(load_csv_as_tex(open(path, encoding='utf_8_sig')))

if __name__ == '__main__':
    unittest.main()
