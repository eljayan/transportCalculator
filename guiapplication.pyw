from Tkinter import *
from threading import Thread
import tkMessageBox
import calculator
from sqlite3 import connect
from ttk import Combobox
from tkintertable import TableModel, TableCanvas
from select_file import select_file

class App():
    def __init__(self):
        self.root = Tk()
        self.results = None

        self.root.title("Transport Cost Calculator")

        self.root.resizable(width=False, height=True)

        self.mainframe = Frame(self.root, width = 1600, height = 300, background="white")
        self.mainframe.grid(row = 0, column=0, padx = 10, pady = 5)
        self.mainframe.grid_propagate(0)  #evita que el frame se colapse al tamano de los widgets

        self.pl_label = Label(self.mainframe, name="path", text="Select Packing List: ", width=25, anchor="w")
        self.pl_label.grid(row=0, column =0, padx=5, pady=5)

        self.filename = StringVar()
        self.filename_label = Label(self.mainframe, textvariable = self.filename, width = 45, anchor="w")
        self.filename_label.grid(row=0, column=3, padx=5, pady=5)

        self.pl_button = Button(self.mainframe, text="choose file", width=10,\
                           command=lambda: self.filename.set(select_file("Select Packinglist")))
        self.pl_button.grid(row=0, column=1, padx=5, sticky="w")

        self.origins_list_values = ["guayaquil", "quito"]
        self.origins_list_selected = StringVar(value="guayaquil")
        self.origin_label = Label(self.mainframe, text = "Select Origin: ", width = 25, anchor="w")
        self.origin_label.grid(row = 1, column = 0, padx=5, pady=5 )
        self.origins_combobox = Combobox(self.mainframe, textvariable = self.origins_list_selected, values = self.origins_list_values, width =10)
        self.origins_combobox.grid(row=1, column=1, padx =5, sticky = "w")

        self.destination_list = self.get_destinations()
        self.destination_selected = StringVar(value="local")
        self.destination_label = Label(self.mainframe, text = "Select Destination: ", width = 25, anchor="w")
        self.destination_label.grid(row =2, column = 0, padx=5, pady=5)
        self.destinations_combobox = Combobox(self.mainframe, textvariable = self.destination_selected, values = self.destination_list, width=20)
        self.destinations_combobox.grid(row=2, column=1, padx=5, sticky="w")

        self.product_line_list = ["wireless", "fixed", "transmission", "datacom", "core"]
        self.product_line_selected = StringVar(value="wireless")
        self.product_line_label = Label(self.mainframe, text= "Product Line: ", width=25, anchor="w")
        self.product_line_label.grid(row=3, column=0, padx=5, pady=5)
        self.product_line_combobox = Combobox(self.mainframe, textvariable =self.product_line_selected, \
                                         values = self.product_line_list, width = 10)
        self.product_line_combobox.grid(row=3, column=1, padx=5, sticky="w")

        self.extra_distance_label =  Label(self.mainframe, text = "Enter extra distance (optional): ", width = 25, anchor="w")
        self.extra_distance_label.grid(row=4, column =0, padx=5, pady=5)
        self.extra_distance_textbox = Text(self.mainframe, width = 5, height =1)
        self.extra_distance_textbox.grid(row=4, column=1, padx=5, sticky="w")

        self.stops_label = Label(self.mainframe, text = "Number of Stops: ", width = 25, anchor="w")
        self.stops_label.grid(row=5, column =0, padx=5, pady=5)
        self.stops_textbox = Text(self.mainframe, width=5, height=1)
        self.stops_textbox.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        #paso las variabes y widgets a una funcion externa para que extraiga sus valores
        self.variables={
            "filename":self.filename,
            "origins_list_selected":self.origins_list_selected,
            "destination_selected":self.destination_selected,
            "product_line_selected":self.product_line_selected,
            "extra_distance_textbox": self.extra_distance_textbox,
            "stops_textbox": self.stops_textbox
        }

        #esta es la parte interesante. Para que la aplicacion se actualice mientras se
        #ejecuta el proceso, es necesario crear un nuevo thread. De lo contrario los
        #cambios no se visualizaran porque el programa se estancaria en esta parte y no
        #avanzaria hasta el mainloop, que es donde se reescribe el contenid de la pantalla

        self.process_thread = Thread(target=self.update_tables) #este es el thread que iniciara al hacer click
        self.process_status = StringVar()
        self.process_button = Button(self.mainframe, text="Calculate", command = self.process_thread.start)
        self.process_button.grid(row=6, column=1, padx = 5, pady=5, sticky = "w")
        self.process_status_label = Label(self.mainframe, textvariable=self.process_status, width=45, anchor="w")
        self.process_status_label.grid(row=6, column=3, padx=5)

        self.table_dict = {'1': {'supplier':'',
                            'origin': '',
                            'destination':'',
                            'distance': '',
                            'product line':'',
                            'region':'',
                            'extra km':'',
                            'stops':'',
                            'truck type':'',
                            'base transport':'',
                            'add transport':'',
                            'manpower cost':'',
                            'forklift':'',
                            'stops cost':'',
                            'total cost':''
                            }}

        self.tableframe = Frame(self.root, width=1600)
        self.tableframe.grid(row=1, column=0)
        self.model = TableModel()
        self.model.importDict(self.table_dict)
        self.table = TableCanvas(self.tableframe, model=self.model, width=1600)
        self.table.createTableFrame()

        self.root.mainloop()

    def get_destinations(self):
        db = connect("db.db")
        cursor = db.execute("select destination from distances group by destination")
        return [destination[0] for destination in cursor]

    def build_basic_data(self):
        basic_data = {
            "path": self.variables["filename"].get(),
            "origin": self.variables["origins_list_selected"].get(),
            "destination": self.variables["destination_selected"].get(),
            "productline": self.variables["product_line_selected"].get(),
            "extradistance": self.variables["extra_distance_textbox"].get("1.0", "end-1c"),
            "stops": self.variables["stops_textbox"].get("1.0", "end-1c")
        }
        return  basic_data

    def showrequest(request):
        tkMessageBox.showinfo(message=request)


    def update_tables(self):
        basic_data = self.build_basic_data()

        #realizar el proceso en un nuevo thread
        calculator.calculator(self, basic_data)

        # pasar a la funcion calculator
        # result  = calculator.calculator(basic_data, status)

        #actualizar el table_dict

        #pasar el table dict al model

        #redraw the table

        self.model.importDict(self.results)
        self.table.redrawTable()
        self.process_status.set("Process completed.")
        return

if __name__ == '__main__':
    App()
    