from Tkinter import *
from ttk import Combobox
from select_file import select_file

def main():
    root = Tk()
    root.title("Transport Cost Calculator")

    root.resizable(width=False, height=True)

    mainframe = Frame(root, width = 600, height = 800)
    mainframe.grid(row = 0, column=0, padx = 10, pady = 5)
    mainframe.grid_propagate(0)

    destination_list =[]

    pl_label = Label(mainframe, text="Select Packing List: ", width=25, anchor="w")
    pl_label.grid(row=0, column =0, padx=5, pady=5)

    filename = StringVar()
    filename_label = Label(mainframe, textvariable = filename, width = 25, anchor="w")
    filename_label.grid(row=0, column=3, padx=5, pady=5)

    pl_button = Button(mainframe, text="choose file", width=10,\
                       command=lambda: filename.set(select_file("Select Packinglist")))
    pl_button.grid(row=0, column=1, padx=3, sticky="w")

    origins_list_values = ["guayaquil", "quito"]
    origins_list_selected = StringVar(value="guayaquil")
    origin_label = Label(mainframe, text = "Select Origin: ", width = 25, anchor="w")
    origin_label.grid(row = 1, column = 0, padx=5, pady=5 )
    origins_combobox = Combobox(mainframe, textvariable = origins_list_selected, values = origins_list_values, width =10)
    origins_combobox.grid(row=1, column=1, padx =3, sticky = "w")

    destination_label = Label(mainframe, text = "Select Destination: ", width = 25, anchor="w")
    destination_label.grid(row =2, column = 0, padx=5, pady=5)

    product_line_list = ["wireless", "fixed", "transmission", "datacom", "core"]
    product_line_selected = StringVar(value="wireless")
    product_line_label = Label(mainframe, text= "Product Line: ", width=25, anchor="w")
    product_line_label.grid(row=3, column=0, padx=5, pady=5)
    product_line_combobox = Combobox(mainframe, textvariable =product_line_selected, \
                                     values = product_line_list, width = 10)
    product_line_combobox.grid(row=3, column=1, sticky="w")

    extra_distance_label =  Label(mainframe, text = "Enter extra distance (optional): ", width = 25, anchor="w")
    extra_distance_label.grid(row=4, column =0, padx=5, pady=5)
    extra_distance_textbox = Text(mainframe, width = 5, height =1)
    extra_distance_textbox.grid(row=4, column=1, sticky="w")

    stops_label = Label(mainframe, text = "Number of Stops: ", width = 25, anchor="w")
    stops_label.grid(row=5, column =0, padx=5, pady=5)




    process_button = Button(mainframe, text="Calculate")
    process_button.grid(row=5, column=1)

    root.mainloop()

if __name__ == '__main__':
    main()