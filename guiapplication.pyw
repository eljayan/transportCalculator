from Tkinter import *
import tkMessageBox
from sqlite3 import connect
from ttk import Combobox
from tkintertable import TableModel, TableCanvas
from select_file import select_file

def main():
    root = Tk()
    root.title("Transport Cost Calculator")

    root.resizable(width=False, height=True)

    mainframe = Frame(root, width = 1600, height = 300, background="white")
    mainframe.grid(row = 0, column=0, padx = 10, pady = 5)
    mainframe.grid_propagate(0)

    pl_label = Label(mainframe, name="path", text="Select Packing List: ", width=25, anchor="w")
    pl_label.grid(row=0, column =0, padx=5, pady=5)

    filename = StringVar()
    filename_label = Label(mainframe, textvariable = filename, width = 45, anchor="w")
    filename_label.grid(row=0, column=3, padx=5, pady=5)

    pl_button = Button(mainframe, text="choose file", width=10,\
                       command=lambda: filename.set(select_file("Select Packinglist")))
    pl_button.grid(row=0, column=1, padx=5, sticky="w")

    origins_list_values = ["guayaquil", "quito"]
    origins_list_selected = StringVar(value="guayaquil")
    origin_label = Label(mainframe, text = "Select Origin: ", width = 25, anchor="w")
    origin_label.grid(row = 1, column = 0, padx=5, pady=5 )
    origins_combobox = Combobox(mainframe, textvariable = origins_list_selected, values = origins_list_values, width =10)
    origins_combobox.grid(row=1, column=1, padx =5, sticky = "w")

    destination_list = get_destinations()
    destination_selected = StringVar(value="local")
    destination_label = Label(mainframe, text = "Select Destination: ", width = 25, anchor="w")
    destination_label.grid(row =2, column = 0, padx=5, pady=5)
    destinations_combobox = Combobox(mainframe, textvariable = destination_selected, values = destination_list, width=20)
    destinations_combobox.grid(row=2, column=1, padx=5, sticky="w")

    product_line_list = ["wireless", "fixed", "transmission", "datacom", "core"]
    product_line_selected = StringVar(value="wireless")
    product_line_label = Label(mainframe, text= "Product Line: ", width=25, anchor="w")
    product_line_label.grid(row=3, column=0, padx=5, pady=5)
    product_line_combobox = Combobox(mainframe, textvariable =product_line_selected, \
                                     values = product_line_list, width = 10)
    product_line_combobox.grid(row=3, column=1, padx=5, sticky="w")

    extra_distance_label =  Label(mainframe, text = "Enter extra distance (optional): ", width = 25, anchor="w")
    extra_distance_label.grid(row=4, column =0, padx=5, pady=5)
    extra_distance_textbox = Text(mainframe, width = 5, height =1)
    extra_distance_textbox.grid(row=4, column=1, padx=5, sticky="w")

    stops_label = Label(mainframe, text = "Number of Stops: ", width = 25, anchor="w")
    stops_label.grid(row=5, column =0, padx=5, pady=5)
    stops_textbox = Text(mainframe, width=5, height=1)
    stops_textbox.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    #paso las variabes y widgets a una funcion externa para que extraiga sus valores
    variables={
        "filename":filename,
        "origins_list_selected":origins_list_selected,
        "destination_selected":destination_selected,
        "product_line_selected":product_line_selected,
        "extra_distance_textbox": extra_distance_textbox,
        "stops_textbox": stops_textbox
    }
    process_button = Button(mainframe, text="Calculate", command = lambda: update_tables(table, model, table_dict, variables))
    process_button.grid(row=6, column=1, padx = 5, pady=5, sticky = "w")

    table_dict = {'1': {'origin': '',
                        'destination':'',
                        'product line':'',
                        'supplier': '',
                        'distance':'',
                        'extra km':'',
                        'region':'',
                        'stops':'',
                        'base transport':'',
                        'add transport':'',
                        'manpower cost':'',
                        'forklift':'',
                        'total cost':''
                        }}
    # d={'1': {'origin': '', 'destination':'', 'supplier': ''}}

    tableframe = Frame(root, width=1600)
    tableframe.grid(row=1, column=0)
    model = TableModel()
    model.importDict(table_dict)
    table = TableCanvas(tableframe, model=model, width=1600)
    table.createTableFrame()

    root.mainloop()

def get_destinations():
    db = connect("db.db")
    cursor = db.execute("select destination from distances group by destination")
    return [destination[0] for destination in cursor]

def build_basic_data(variables):
    basic_data = {
        "path": variables["filename"].get(),
        "origin": variables["origins_list_selected"].get(),
        "destination": variables["destination_selected"].get(),
        "productline": variables["product_line_selected"].get(),
        "extradistance": variables["extra_distance_textbox"].get("1.0", "end-1c"),
        "stops": variables["stops_textbox"].get("1.0", "end-1c")
    }
    return  basic_data

def showrequest(request):
    tkMessageBox.showinfo(message=request)


def update_tables(table, model, table_dict, variables):
    basic_data = build_basic_data(variables)

    #pasar a la funcion calculator

    #actualizar el table_dict

    #pasar el table dict al model

    #redraw the table
    return

if __name__ == '__main__':
    main()
    