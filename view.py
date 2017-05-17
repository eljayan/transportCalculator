'''
collects data from the user like
pl path,
origin
destination
'''
from select_file import select_file

def start():
    pl = select_file("packing list")
    origin = raw_input("enter origin: ")
    destination = raw_input("enter destination: ")

    return {"path":pl,
            "origin":origin,
            "destination":destination}

if __name__ == '__main__':
    print start()