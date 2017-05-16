import time
import re
from selenium import webdriver
from win32com import client

#globals
url = "http://es.distancias.himmera.com/buscar/"
driver = webdriver.Chrome()
driver.get(url)


def main():
    #iterate workbook
    xl = client.Dispatch("Excel.Application")
    wb = xl.Workbooks.Open("D:/myScripts/transportCalculator/sample/Ecuador_Distancias.xls")
    sh = wb.Sheets("Sheet1")

    for cell in sh.Range("A265:A273"):
        origin = cell.Value
        destination = cell.Offset(1,2).Value
        try:
            distance = request_distance(origin, destination + " ecuador")
            cell.Offset(1,3).Value = distance
        except:
            cell.Offset(1, 3).Value = 0

def request_distance(origin_string, destination_string):
    #find the elements
    origin = driver.find_element_by_id("dela")
    destination = driver.find_element_by_id("spre")
    button = driver.find_element_by_id("srchbtn")

    #clear the default values
    origin.clear()
    destination.clear()

    origin.send_keys(origin_string)
    destination.send_keys(destination_string)
    button.click()

    time.sleep(3)

    data =  driver.find_element_by_id("km_").text

    return parse_response(data)

def parse_response(data_string):
    #pase and get the data
    if not isinstance(data_string, basestring):
        return ''

    pattern = re.compile(r'\d+\.?\d*')
    match = pattern.search(data_string)
    if match:
        return match.group()
    else:
        return ''


if __name__ == '__main__':
    #print request_distance("guayaquil", "manta ecuador")
    main()
