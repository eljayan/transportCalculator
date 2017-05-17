import Tkinter as tk
from tkFileDialog import askopenfilename


def select_file(filecathegory):
    root = tk.Tk()
    root.withdraw()
    filepath = askopenfilename(title="Please select "+ filecathegory, \
                               filetypes=[("Excel Files Only", "*.xls*")])
    return filepath

if __name__ == '__main__':
    f = select_file("Packing List")
    print f