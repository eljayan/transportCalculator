'''
Combines the information from the GUI and the PL. 
input: two dictionaries with plinfo and route info
output:a dictionary with the biggest box and total volume of the pl object, origin and destination.
'''
from sqlite3 import connect

def buildrequest(basic_data, plinfo):
    request = {}
    request["biggest_case"] = plinfo["biggest_case"]
    request["total_weight"] = plinfo["total_weight"]
    request["total_volume"] =  plinfo["total_volume"]
    request["origin"]=basic_data["origin"]
    request["destination"]= basic_data["destination"]
    if isinstance(basic_data["extradistance"], basestring):
        try:
            request["extradistance"]= float(basic_data["extradistance"])
        except:
            request["extradistance"] = 0
    else:
        request["extradistance"] = basic_data["extradistance"]

    request["productline"]=basic_data["productline"]
    request["region"] = find_region(basic_data["destination"])
    request["stops"] = basic_data["stops"]

    return request


def find_region(destination):
    db = connect("db.db")
    cursor = db.execute("select region from distances where destination = ?", (destination,))
    region = cursor.fetchone()[0]
    return region#############################

if __name__ == '__main__':
    basic_data = {
        "origin": "guayaquil",
        "destination": "quito",
        "productline": "1200",
        "extradistance":0,
        "stops":0
    }
    
    plinfo = {
        "biggest_case": 60,
        "total_weight": 100,
        "total_volume": 0.98
    }
    
    r = buildrequest(basic_data, plinfo)

    print r