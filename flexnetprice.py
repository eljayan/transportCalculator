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

    ttype = trucktype.select(volume)
    mpower = manpower.calculate(biggest_case_weight=biggest_box, total_weight=weight)

    distance = db.execute("select distance from distances where origin=? and destination=?", (origin, destination))
    distance = distance.fetchone()[0]

    for t in ttype:
        query = db.execute("select %s from flexnet where origin = ? and destination = ?" %(t[1].lower()), (origin, destination))
        transport_cost += t[0] * float(query.fetchone()[0])

    mpower_cost = mpower * 55

    return {
        "supplier":"flexnet",
        "distance":distance,
        "truck_type":ttype,
        "transport_cost":transport_cost,
        "manpower_cost":mpower_cost
    }

if __name__ == '__main__':
    calculate({"origin":"guayaquil",
               "destination":"quito",
               "total_volume":3.25,
               "biggest_box":84.3,
               "total_weight":256.38})