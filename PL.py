"""
Loads a PL object from an excel file, or from a COM Workbook
"""
import os
import pythoncom
from win32com import client
from pprint import pprint
from copy import deepcopy
import re


class PL:
    def __init__(self, filepath, app):
        self.app = app
        self.xl_instance = None
        self.path = filepath
        self.filename = os.path.basename(filepath)
        self.set_workbook()
        self.set_last_row()
        self.set_headers_row()
        self.set_number()
        self.set_summary()
        self.set_gross_weight()
        self.set_net_weight()
        self.set_volume()
        self.set_cases()
        self.set_po()
        self.set_case_column()
        self.set_material_column()
        self.set_part_number_column()
        self.set_model_column()
        self.set_description_column()
        self.set_quantity_column()
        self.set_uom_column()
        self.set_unit_price_column()
        self.set_total_price_column()
        self.set_serial_column()
        self.set_gross_weight_column()
        self.set_net_weight_column()
        self.set_size_column()
        self.set_volume_column()
        self.set_note_column()
        self.set_boxname_column()
        self.set_date()
        self.set_contract()
        self.set_project()
        self.set_row_cases()
        self.set_row_material()
        self.set_row_gross_weight()
        self.set_row_net_weight()
        self.set_row_size()
        self.set_row_volume()
        self.set_row_note()
        self.set_row_boxname()
        self.set_items_range()
        self.set_items()
        self.set_line_items()
        self.total()


    def set_workbook(self):
        pythoncom.CoInitialize()
        xl = client.Dispatch("Excel.Application")
        self.xl_instance =  pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, xl)
        wb = xl.Workbooks.Open(self.path)
        self.workbook = wb

    def set_last_row(self):
        l = self.workbook.Sheets(1).Usedrange.Rows.Count

        for cel in range(1, l + 1):
            if re.search(r"total", unicode(self.workbook.Sheets(1).Range("A" + unicode(cel)).Value), flags=re.IGNORECASE):
                self.last_row = cel
                self.app.process_status.set( "last row: " + str(self.last_row))
                return

    def extract(self, stringpl):
        # print string
        patronNormal = r'0[\d\w][\d\w]\d{9}[\d\w]\w{4}\d[\d\w]\w\w?'  # 000218151109TPHWA01H 0002181405160FHWA09E
        patronSpareParts = r'00P\d{10}\w\d*'  # 00P2181507288J
        patronWT = r'WT\d{9}\w'  # WT150804196H
        patronExpress = r'\d{3}\d{9}\w{2}\d\d\w\d\d'  # 000218150316GM02E01

        patrones = [patronNormal, patronSpareParts, patronWT, patronExpress]
        for patron in patrones:
            if re.search(patron, stringpl):
                return re.search(patron, stringpl).group()

    def set_number(self):
        self.app.process_status.set("finding pl number...")
        pattern = re.compile(r'P/L\s[Nn][Oo]')
        for cel in self.workbook.Sheets(1).Usedrange:
            if pattern.search(unicode(cel.Value)):
                self.number =  self.extract(unicode(cel.Value))
                return
        self.number = "Not Found"

    def set_summary(self):
        self.app.process_status.set("setting summary...")
        self.summary = self.workbook.Sheets(1).Range("A" + unicode(self.last_row)).Value

    def set_row_cases(self):
        '''creates a dictionary of {rows, case number}'''
        self.app.process_status.set("creating dictionary of rows and case numbers...")
        row_cases ={}
        case_number = 1 #this is the control variable
        sheet = self.workbook.Sheets(1)

        #for loop por la columna de numero de cases
        for r in range(self.HEADERSROW+1, self.last_row):
            cell = sheet.Cells(r, self.CASECOL)
            if cell.Mergecells: #test si la celda es merged
                if cell.Value == None or cell.Value == "" or cell.Value == unicode("%mergetop%"):
                    #si el valor es None:
                    #toma el row y lo asocia al case number
                    row_cases.update({str(r):str(case_number)})

                else:
                    case_number = int(cell.Value)
                    #toma el row y lo asocia al case number
                    row_cases.update({str(r): str(case_number)})
            else:
                case_number = int(cell.Value)
                #toma el row y lo asocia al control variable
                row_cases.update({str(r): str(case_number)})

        self.row_cases = row_cases

    def set_row_material(self):
        '''creates a dictionary of {rows, case material}'''
        self.app.process_status.set("creating dictionary of rows and case materials")
        row_material ={}
        material = "Carton" #this is the control variable
        sheet = self.workbook.Sheets(1)

        #for loop por la columna de MATERIALES
        for r in range(self.HEADERSROW+1, self.last_row):
            cell = sheet.Cells(r, self.MATERIALCOL)
            if cell.Mergecells: #test si la celda es merged
                if cell.Value == None or cell.Value == "" or cell.Value == unicode("%mergetop%"):
                    #si el valor es None:
                    #toma el row y lo asocia al case number
                    row_material.update({str(r):str(material)})

                else:
                    material = unicode(cell.Value)
                    #toma el row y lo asocia al case number
                    row_material.update({str(r): str(material)})
            else:
                material = unicode(cell.Value)
                #toma el row y lo asocia al control variable
                row_material.update({str(r): str(material)})

        self.row_material = row_material

    def set_row_note(self):
        '''creates a dictionary of {rows, note}'''
        self.app.process_status.set("creating dictionary of rows and notes")
        row_note ={}
        note = "" #this is the control variable
        sheet = self.workbook.Sheets(1)

        #for loop por la columna de note
        for r in range(self.HEADERSROW+1, self.last_row):
            cell = sheet.Cells(r, self.NOTECOLUMN)
            if cell.Mergecells: #test si la celda es merged
                if cell.Value == None or cell.Value == "" or cell.Value == unicode("%mergetop%"):
                    #si el valor es None:
                    #toma el row y lo asocia al note
                    row_note.update({str(r):str(note)})

                else:
                    note = unicode(cell.Value)
                    #toma el row y lo asocia al note
                    if note:
                        row_note.update({str(r): str(note)})
                    else:
                        row_note.update("")
            else:
                note = unicode(cell.Value)
                #toma el row y lo asocia al control variable
                if note:
                    row_note.update({str(r): unicode(note)})
                else:
                    row_note.update("")

        self.row_note = row_note

    def set_row_boxname(self):
        '''creates a dictionary of {rows, boxname}'''
        self.app.process_status.set("creating dictionary of rows and boxnames...")

        if not self.BOXNAMECOLUMN:
            self.row_boxname = {}
            return

        row_boxname ={}
        boxname = "" #this is the control variable
        sheet = self.workbook.Sheets(1)

        #for loop por la columna de note
        for r in range(self.HEADERSROW+1, self.last_row):
            cell = sheet.Cells(r, self.BOXNAMECOLUMN)
            if cell.Mergecells: #test si la celda es merged
                if cell.Value == None or cell.Value == "" or cell.Value == unicode("%mergetop%"):
                    #si el valor es None:
                    #toma el row y lo asocia al case number
                    row_boxname.update({str(r):str(boxname)})

                else:
                    boxname = unicode(cell.Value)
                    #toma el row y lo asocia al case number
                    row_boxname.update({str(r): str(boxname)})
            else:
                boxname = unicode(cell.Value)
                #toma el row y lo asocia al control variable
                row_boxname.update({str(r): str(boxname)})

        self.row_boxname = row_boxname

    def set_row_gross_weight(self):
        '''creates a dictionary of {rows, item gross weight}'''
        self.app.process_status.set("creating dictionary of rows and gross weights...")
        row_gross_weight ={}
        gross_weight = 0 #this is the control variable
        sheet = self.workbook.Sheets(1)

        #for loop por la columna de numero de cases
        for r in range(self.HEADERSROW+1, self.last_row):
            cell = sheet.Cells(r, self.GROSSWEIGHTCOL)
            if cell.Mergecells: #test si la celda es merged
                if cell.Value == None or cell.Value == "" or cell.Value == unicode("%mergetop%"):
                    #si el valor es None:
                    #toma el row y lo asocia al gross weight
                    row_gross_weight.update({str(r):float(gross_weight)})

                else:
                    gross_weight = float(cell.Value)
                    #toma el row y lo asocia al case number
                    row_gross_weight.update({str(r): float(gross_weight)})
            else:
                gross_weight = float(cell.Value)
                #toma el row y lo asocia al control variable
                row_gross_weight.update({str(r): float(gross_weight)})

        self.row_gross_weight = row_gross_weight

    def set_row_net_weight(self):
        '''creates a dictionary of {rows, item gross weight}'''
        self.app.process_status.set("creating dictionary of rows and new weights..")
        row_net_weight ={}
        net_weight = float(0) #this is the control variable
        sheet = self.workbook.Sheets(1)

        #for loop por la columna de numero de cases
        for r in range(self.HEADERSROW+1, self.last_row):
            cell = sheet.Cells(r, self.NETWEIGHTCOL)
            if cell.Mergecells: #test si la celda es merged
                if cell.Value == None or cell.Value == "" or cell.Value == unicode("%mergetop%"):
                    #si el valor es None:
                    #toma el row y lo asocia al gross weight
                    row_net_weight.update({str(r):float(net_weight)})

                else:
                    net_weight = float(cell.Value)
                    #toma el row y lo asocia al case number
                    row_net_weight.update({str(r): float(net_weight)})
            else:
                net_weight = float(cell.Value)
                #toma el row y lo asocia al control variable
                row_net_weight.update({str(r): float(net_weight)})

        self.row_net_weight = row_net_weight

    def set_row_size(self):
        '''creates a dictionary of {rows, item gross weight}'''
        self.app.process_status.set( "creating dictionary of rows and gross weights...")
        row_size ={}
        size = 0 #this is the control variable
        sheet = self.workbook.Sheets(1)

        #for loop por la columna de numero de cases
        for r in range(self.HEADERSROW+1, self.last_row):
            cell = sheet.Cells(r, self.SIZECOL)
            if cell.Mergecells: #test si la celda es merged
                if cell.Value == None or cell.Value == "" or cell.Value == unicode("%mergetop%"):
                    #si el valor es None:
                    #toma el row y lo asocia al gross weight
                    row_size.update({str(r):str(size)})

                else:
                    size = str(cell.Value)
                    #toma el row y lo asocia al case number
                    row_size.update({str(r): str(size)})
            else:
                size = str(cell.Value)
                #toma el row y lo asocia al control variable
                row_size.update({str(r): str(size)})

        self.row_size = row_size

    def set_row_volume(self):
        '''creates a dictionary of {rows, item volume}'''
        self.app.process_status.set("creating dictionary of rows and volumes...")
        row_volume ={}
        volume = 0 #this is the control variable
        sheet = self.workbook.Sheets(1)

        #for loop por la columna de numero de cases
        for r in range(self.HEADERSROW+1, self.last_row):
            cell = sheet.Cells(r, self.VOLUMECOL)
            if cell.Mergecells: #test si la celda es merged
                if cell.Value == None or cell.Value == "" or cell.Value == unicode("%mergetop%"):
                    #si el valor es None:
                    #toma el row y lo asocia al gross weight
                    row_volume.update({str(r):float(volume)})

                else:
                    volume = float(cell.Value)
                    #toma el row y lo asocia al case number
                    row_volume.update({str(r): float(volume)})
            else:
                volume = float(cell.Value)
                #toma el row y lo asocia al control variable
                row_volume.update({str(r): float(volume)})

        self.row_volume = row_volume

    def set_gross_weight(self):
        self.app.process_status.set("setting gross weights...")
        text = self.summary
        pattern = re.compile(r'gross\swe\w+\s?\(\w+\)\:\d*\.?\d*\s', flags=re.IGNORECASE)
        if pattern.search(text):
            subString = pattern.search(text).group()
            if re.search(r'\d+\.?\d*', subString):
                self.gross_weight = re.search(r'\d+\.?\d*', subString).group()
        else:
            self.gross_weight = 0

    def set_net_weight(self):
        self.app.process_status.set("setting net weights...")
        text = self.summary
        pattern = re.compile(r'[Nn].+\s[Ww][Ee].+\(\w+\):\d*\.?\d*\s')
        if pattern.search(text):
            subString = pattern.search(text).group()
            self.net_weight = re.search(r'\d+\.?\d*\s', subString).group()
        else:
            self.net_weight = 0

    def set_volume(self):
        self.app.process_status.set("setting volumes...")
        text = self.summary
        pattern = re.compile(r'volume\s?\(\w\w\w\):\d*\.?\d*', flags=re.IGNORECASE)
        if pattern.search(text):
            subString = pattern.search(text).group()
            self.volume = re.search(r'\d+\.?\d*', subString).group()
        else:
            self.volume = 0

    def set_cases(self):
        self.app.process_status.set("setting case numbers...")
        # Total:5CASES    gross weight(KG):241.9    net weight(KG):176.07    volume(CBM):1.44
        text = self.summary
        pattern = re.compile(r'[Tt][Oo][Tt][Aa][Ll]\:\d+\w*\s')
        if pattern.search(text):
            subString = pattern.search(text).group()
            self.cases = re.search(r'\d+\.?\d*', subString).group()
        else:
            self.cases = 0

    def patternSearch(self, columnNamePattern):
        # seraches a pattern in used rage and returns column number

        compiledPattern = re.compile(pattern=columnNamePattern, flags=re.IGNORECASE)

        # iterates rows and cells in a row
        for row in self.workbook.Sheets(1).UsedRange.Rows:
            rowNumber = row.Row

            # some files have many unused rows, this breaks the unnecessary loops.
            if rowNumber > self.last_row:
                return None

            for cell in row.Cells:
                if cell.Column > 20:
                    break
                if compiledPattern.search(unicode(cell.Value)):
                    return cell.Column

    def set_case_column(self):
        self.app.process_status.set("setting case column...")
        pattern = r"case"
        self.CASECOL = self.patternSearch(columnNamePattern=pattern)

    def set_material_column(self):
        self.app.process_status.set("setting materials column...")
        pattern = r"material"
        self.MATERIALCOL = self.patternSearch(columnNamePattern=pattern)

    def set_part_number_column(self):
        self.app.process_status.set("setting part number column...")
        pattern = r"part\s+number"
        self.PARTNUMBERCOL = self.patternSearch(columnNamePattern=pattern)

    def set_model_column(self):
        self.app.process_status.set("setting models column...")
        pattern = r"model"
        self.MODELCOL = self.patternSearch(columnNamePattern=pattern)

    def set_description_column(self):
        self.app.process_status.set("setting description columns...")
        pattern = r"description"
        self.DESCRIPTIONCOL = self.patternSearch(columnNamePattern=pattern)

    def set_quantity_column(self):
        self.app.process_status.set("setting qty column...")
        pattern = r"qty"
        self.QTYCOL = self.patternSearch(columnNamePattern=pattern)

    def set_uom_column(self):
        self.app.process_status.set("setting uom column...")
        pattern = r"uom"
        self.UOMCOL = self.patternSearch(columnNamePattern=pattern)

    def set_unit_price_column(self):
        self.app.process_status.set("setting unit price column...")
        pattern = r"unit\sprice"
        self.UNITPRICECOL = self.patternSearch(columnNamePattern=pattern)

    def set_total_price_column(self):
        self.app.process_status.set("setting total price column...")
        pattern = r"total\sprice"
        self.TOTALPRICECOL = self.patternSearch(columnNamePattern=pattern)

    def set_serial_column(self):
        self.app.process_status.set("setting serial column...")
        pattern = r'serial'
        self.SERIALCOL = self.patternSearch(columnNamePattern=pattern)

    def set_headers_row(self):
        self.app.process_status.set("setting headers column...")
        pattern = r"case\.*"
        compiledPattern = re.compile(pattern=pattern, flags=re.IGNORECASE)
        for row in self.workbook.Sheets(1).UsedRange.Rows:
            for cell in row.Cells:
                if cell.Column > 20:
                    break
                if compiledPattern.search(unicode(cell.Value)):
                    self.HEADERSROW = cell.Row
                    return

    def set_date(self):
        self.app.process_status.set("setting date...")
        pattern = re.compile(r'[Dd][Aa][Tt][Ee]')
        datePattern = re.compile(r'\d+-\d+-\d+')
        columnCount = self.workbook.Sheets(1).Usedrange.Columns.Count
        for cel in self.workbook.Sheets(1).Usedrange:
            if pattern.search(unicode(cel.Value)):
                moveRight = 2
                while moveRight < columnCount:
                    moveCel = cel.Offset(1, moveRight).Value
                    if datePattern.search(unicode(moveCel)):
                        self.date = datePattern.search(unicode(moveCel)).group()
                    moveRight += 1
                break

    def set_contract(self):
        self.app.process_status.set("setting contract number...")
        pattern = re.compile(r'[Cc][Oo][Nn][Tt][Rr][Aa][Cc][Tt]\s[Nn][Oo]\.:.+')
        for cel in self.workbook.Sheets(1).Usedrange:
            if pattern.search(unicode(cel.Value)):
                p = cel.Value.find(':')
                contract = cel.Value[p + 1:]
                self.contract = contract
                return
        self.contract = None

    def set_po(self): ####
        self.app.process_status.set("setting po number...")
        pattern = re.compile(r'p\/?o no\.:?\d*', flags=re.IGNORECASE)
        for cel in self.workbook.Sheets(1).Usedrange:
            if cel.column > 20:
                continue
            if pattern.search(unicode(cel.Value)):
                #p = cel.Value.find(':')
                #po = cel.Value[p + 1:]
                #self.po = po
                self.po = cel.Value
                return
        self.po = None

    def set_project(self):
        self.app.process_status.set("setting project name...")
        pattern = re.compile(r'project\.*:\s*', flags=re.IGNORECASE)
        for cel in self.workbook.Sheets(1).Usedrange:
            if cel.column > 20:
                continue
            if pattern.search(unicode(cel.Value)):
                p= cel.Value.find(":")
                project = cel.Value[p+1:]
                self.project = project
                return
        self.project = None

    def set_items_range(self):
        self.app.process_status.set("setting items range")
        rangeStart = self.workbook.Sheets(1).Cells(self.HEADERSROW + 1, self.PARTNUMBERCOL).Address
        rangeEnd = self.workbook.Sheets(1).Cells(self.last_row - 1, self.PARTNUMBERCOL).Address
        self.items_range = self.workbook.Sheets(1).Range(rangeStart, rangeEnd)

    def set_gross_weight_column(self):
        self.app.process_status.set("setting gross weight column")
        pattern = r'gw\n?\s?\(kg\)'
        self.GROSSWEIGHTCOL = self.patternSearch(columnNamePattern=pattern)

    def set_net_weight_column(self):
        self.app.process_status.set("setting net weight column...")
        pattern = r'nw\n?\s?\(kg\)'
        self.NETWEIGHTCOL = self.patternSearch(columnNamePattern=pattern)

    def set_size_column(self):
        self.app.process_status.set("setting size column...")
        pattern = r'size\n?\s?\(mm\)'
        self.SIZECOL = self.patternSearch(columnNamePattern=pattern)

    def set_volume_column(self):
        self.app.process_status.set("setting volume column...")
        pattern = r'volume'
        self.VOLUMECOL = self.patternSearch(columnNamePattern=pattern)

    def set_note_column(self):
        self.app.process_status.set("setting note column...")
        pattern = r'note'
        self.NOTECOLUMN = self.patternSearch(columnNamePattern=pattern)

    def set_boxname_column(self):
        self.app.process_status.set("setting boxname column...")
        pattern = r'box name'
        self.BOXNAMECOLUMN = self.patternSearch(columnNamePattern=pattern)

    def set_items(self):
        self.app.process_status.set("setting items...")
        sheet = self.workbook.Sheets(1)
        dataRange = self.items_range
        items_list = []
        item_number = 1
        unique_items = []
        backedBomCodes = set()
        row_cases = self.row_cases
        row_material = self.row_material
        row_gross_weight = self.row_gross_weight
        row_net_weight = self.row_net_weight
        row_size = self.row_size
        row_volume = self.row_volume
        row_note = self.row_note
        row_boxname = self.row_boxname

        for cel in dataRange:
            #si comienza con .. es un subitem
            if str(cel.Value).startswith(".."):
                subItem = Item()
                parentItem = items_list[-1] #toma el ultimo item agregado a la lista

                subItem.part = unicode(cel.Value)
                subItem.case_number = row_cases.get(str(cel.Row))
                subItem.quantity = int(sheet.Cells(cel.Row, self.QTYCOL).Value)
                subItem.description = sheet.Cells(cel.Row, self.DESCRIPTIONCOL).Value
                subItem.model = sheet.Cells(cel.Row, self.MODELCOL).Value
                subItem.uom = sheet.Cells(cel.Row, self.UOMCOL).Value
                try:
                    subItem.tprice = float(sheet.Cells(cel.Row, self.TOTALPRICECOL).Value)
                    parentItem.tprice += subItem.tprice
                except:
                    subItem.tprice = 0

                try:
                    subItem.case_number = self.row_cases.get(str(cel.Value))

                except:
                    subItem.case_number = 0

                try:
                    serialValue = sheet.Cells(cel.Row, self.SERIALCOL).Value
                except:
                    serialValue = None

                if serialValue:
                    subItem.serial = serialValue
                    # if not parentItem.serial: #only adds serial to parent if none exists
                    #     parentItem.serial += subItem.serial + "\s"
                else:
                    subItem.serial = ""

                parentItem.sub_items.append(subItem)

            else:
                item = Item()  # create item object

                item.number = item_number

                item.part = unicode(cel.Value)
                item.case_number = row_cases.get(str(cel.Row))
                item.material = row_material.get(str(cel.Row))

                try:
                    item.uprice = float(sheet.Cells(cel.Row, self.UNITPRICECOL).Value)
                except:
                    item.uprice = 0

                item.quantity = int(sheet.Cells(cel.Row, self.QTYCOL).Value)

                item.description = sheet.Cells(cel.Row, self.DESCRIPTIONCOL).Value

                item.gross_weight = row_gross_weight.get(str(cel.Row))

                item.net_weight = row_net_weight.get(str(cel.Row))

                item.size = row_size.get(str(cel.Row))

                item.volume = row_volume.get(str(cel.Row))

                item.note = row_note.get(str(cel.Row))

                item.box_name = row_boxname.get(str(cel.Row), "")

                try:
                    item.model = sheet.Cells(cel.Row, self.MODELCOL).Value
                except:
                    item.model = None

                item.uom = sheet.Cells(cel.Row, self.UOMCOL).Value

                try:
                    item.tprice = float(sheet.Cells(cel.Row, self.TOTALPRICECOL).Value)
                except:
                    item.tprice = 0

                try:
                    serialValue = sheet.Cells(cel.Row, self.SERIALCOL).Value
                except:
                    serialValue = None

                if serialValue:
                    item.serial = serialValue
                else:
                    item.serial = ""


                item_number += 1

                items_list.append(item)

        #asigns the subserials to the parent item
        for item in items_list:
            if item.serial == "":
                for subItem in item.sub_items:
                    item.serial += subItem.serial + " "

        #populates the unique items list
        for item in items_list:
            partNumber = item.part
            if partNumber in backedBomCodes:
                for it in unique_items:
                    if it.part == item.part:
                        it.quantity += item.quantity
                        it.tprice += item.tprice
                        it.serial += item.serial


            else:
                backedBomCodes.add(partNumber)
                unique_items.append(deepcopy(item))


        self.items_list = items_list
        self.unique_items = unique_items

    def set_line_items(self):
        '''creates one line per item quantity'''
        self.app.process_status.set("setting line items...")
        self.line_items = []
        for item in self.items_list:
            if item.serial != "":
                item.serial = item.serial.replace("\n", " ")
                item.serial = item.serial.replace("\t", " ")
                item_serial_strings = filter(None, item.serial.split())

                for serial in item_serial_strings:
                    line_item = Item()
                    line_item.serial = serial
                    line_item.number = item.number
                    line_item.case_number = item.case_number
                    line_item.material = item.material
                    line_item.part  = item.part
                    line_item.uprice = item.uprice
                    line_item.tprice = item.uprice
                    line_item.quantity = 1
                    line_item.description = item.description
                    line_item.model = item.model
                    line_item.uom = item.uom
                    line_item.gross_weight = item.gross_weight
                    line_item.net_weight = item.net_weight
                    line_item.size = item.size
                    line_item.volume = item.volume
                    line_item.sap  = item.sap
                    self.line_items.append(line_item)
            else:
                for i in range(item.quantity):
                    line_item = Item()
                    #line_item.serial = serial
                    line_item.serial = ""
                    line_item.number = item.number
                    line_item.case_number = item.case_number
                    line_item.material = item.material
                    line_item.part = item.part
                    line_item.uprice = item.uprice
                    line_item.tprice = item.uprice
                    line_item.quantity = 1
                    line_item.description = item.description
                    line_item.model = item.model
                    line_item.uom = item.uom
                    line_item.gross_weight = item.gross_weight
                    line_item.net_weight = item.net_weight
                    line_item.size = item.size
                    line_item.volume = item.volume
                    line_item.sap = item.sap
                    self.line_items.append(line_item)

    def total(self):
        total_qty = 0
        total_value = 0
        for item in self.unique_items:
            total_qty += item.quantity
            total_value += item.tprice

        self.total_qty = total_qty
        self.total_value = total_value

    def export(self):
        return

class Item:
    def __init__(self):
        self.number = None
        self.case_number = None
        self.material = None
        self.part = None
        self.sub_items = []
        self.uprice = None
        self.tprice = None
        self.quantity = None
        self.description = None
        self.model = None
        self.uom = None
        self.serial = ""
        self.gross_weight = None
        self.net_weight = None
        self.size = None
        self.volume = None
        self.note = None
        self.box_name = None
        self.sap = None
        self.order = None


if __name__ == "__main__":
    packing = PL("D:/myScripts/ClaroDatabase/samples/PL 0002181606030AHWA01Q.xlsx")

    # print packing.total_qty

    # print packing.GROSSWEIGHTCOL
    # print packing.NETWEIGHTCOL
    # print packing.SIZECOL
    # print packing.VOLUMECOL


    # for i in packing.line_items:
    #     pprint (vars(i))
