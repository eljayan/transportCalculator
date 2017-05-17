'''
this module starts the view and sends the 
information to other modules
'''
import view
from readpl import readpl
from buildrequest import buildrequest
import flexnetprice

def main():
    basic_data = view.start()

    routeinfo = {"origin":basic_data["origin"], "destination":basic_data["destination"]}

    #read the pl
    plinfo = readpl(basic_data["path"])

    #build the request
    request = buildrequest(plinfo=plinfo, routeinfo=routeinfo)

    #send the request to flexnet calculator
    flexnet_cost = flexnetprice.calculate(request)

    print flexnet_cost

if __name__ == '__main__':
    main()
