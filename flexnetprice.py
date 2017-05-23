'''
input: a dictionary with the service request (biggest box, weight, volume
origin and destination point)
outpt: a dictionary representing the cost of transportation
'''
import trucktype
import manpower
from sqlite3 import connect

def calculate(request):
    transport_cost = 0
    db = connect("db.db")

    origin = request["origin"]
    destination = request["destination"]
    volume = request["total_volume"]
    biggest_box =  request["biggest_box"]
    weight = request["total_weight"]
    extradistance = request.get("extradistance", 0)
    productline = request.get("productline", "")

    ttype = trucktype.select(volume)
    mpower = manpower.calculate(biggest_case_weight=biggest_box, total_weight=weight, destination=destination)

    distance = db.execute("select distance from distances where origin=? and destination=?", (origin, destination))
    distance = distance.fetchone()[0]

    if extradistance:
        q = db.execute("select price from flexnet_km where ? >= min and ? <= max", (extradistance, extradistance))
        q_price =  q.fetchone()
        extradistance_price = q_price[0]
    else:
        extradistance_price = 0

    for t in ttype:
        query = db.execute("select %s from flexnet where origin = ? and destination = ?" %(t[1].lower()), (origin, destination))
        transport_cost += t[0] * float(query.fetchone()[0])

    mpower_cost = mpower * 55

    return {
        "supplier":"flexnet",
        "distance":distance,
        "extradistance": extradistance,
        "productline":productline,
        "truck_type":ttype,
        "base_transport_cost":transport_cost,
        "extra_distance_cost":extradistance_price,
        "manpower_cost":mpower_cost,
        "total_cost":transport_cost+extradistance_price+mpower_cost
    }

if __name__ == '__main__':
    r = calculate({"origin":"guayaquil",
               "destination":"quito",
               "total_volume":3.25,
               "biggest_box":84.3,
               "total_weight":256.38,
               "extradistance" : 100,
                "productline":"wireless"
                })


    print r