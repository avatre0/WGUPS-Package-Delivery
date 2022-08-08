import csv

from Package import Package
from hash_table import HashMap
from truck import Truck
from datetime import datetime, date, time, timedelta


def read_package_data(fileName):
    with open(fileName) as packageData:
        packages = csv.reader(packageData, delimiter=',')
        for p in packages:
            id = int(p[0])
            address = p[1]
            delivery_deadline = p[5]
            weight = p[6]
            note = p[7]

            new_package = Package(id, address, delivery_deadline, weight, note)

            packageHash.add(id, new_package)


def read_distance_data(fileName):
    with open(fileName) as distanceData:
        distanceList = list(csv.reader(distanceData, delimiter=','))
        return distanceList


def read_address_data(fileName):
    with open(fileName) as addressData:
        addressList = list(csv.reader(addressData, delimiter=','))
        return addressList


# Finds distance between two indexes on the distance table
# takes the addresses in as indexes of the table
def distance_between(row, col):
    distance = distanceList[row][col]
    # Since half of the CSV is blank need to check for the mirrored solution
    if distance == '':
        distance = distanceList[col][row]

    return float(distance)


def find_next_shortest_delivery(truck):
    package_list = truck.capacity
    current_address_index = addressDic.get(truck.location)
    shortest_package_address_index = addressDic.get(package_list[0].address)
    shortest_package = package_list[0]
    for package in package_list:
        next_package_address_index = addressDic.get(package.address)
        selected_package_distance = distance_between(int(current_address_index), int(shortest_package_address_index))
        next_package_distance = distance_between(int(current_address_index), int(next_package_address_index))

        if next_package_distance < selected_package_distance:
            shortest_package_address_index = next_package_address_index
            shortest_package = package

    return shortest_package


def create_address_dic():
    address_dic = {}
    for address in addressList:
        address_dic[address[2]] = address[0]
    return address_dic


def load_truck(truck, packages_to_load):
    for package in packages_to_load:
        truck.load_package(packageHash.get(package))
        packageHash.get(package).status = f"On {truck.name}"


# ToDo only accept Truck, pop next package  off truck's stack
# Todo remove package from truck once delivered
def deliver_package(truck):
    package = find_next_shortest_delivery(truck)

    delivery_address = package.address
    delivery_address_index = addressDic[delivery_address]

    truck_location_index = addressDic[truck.location]

    driving_distance = distance_between(int(delivery_address_index), int(truck_location_index))
    driving_time_delta = timedelta(hours=driving_distance / truck.speed)
    d = date.today()
    t = truck.current_time
    truck_departure_time = datetime.combine(d, t)
    truck_delivery_time = truck_departure_time + driving_time_delta

    truck.location = package.address
    truck.distance_driven += driving_distance
    truck.current_time = truck_delivery_time.time()
    package.delivered_time = truck.current_time
    package.isDelivered = True
    package.status = 'DELIVERED'
    truck.package_delivered(package)


def return_to_hub(truck):
    current_address = truck.location
    current_address_index = addressDic[current_address]

    driving_distance = distance_between(0, int(current_address_index))
    driving_time_delta = timedelta(hours=driving_distance / truck.speed)
    d = date.today()
    t = truck.current_time
    truck_departure_time = datetime.combine(d, t)
    truck_delivery_time = truck_departure_time + driving_time_delta
    truck.current_time = truck_delivery_time.time()


# ToDo make method to sort trucks delivery order Greedy algo?

packageHash = HashMap()

packageDataCSV = "data/package_data.csv"
distanceDataCSV = "data/distance_table.csv"
addressDataCSV = "data/address_data.csv"

read_package_data(packageDataCSV)
distanceList = read_distance_data(distanceDataCSV)
addressList = read_address_data(addressDataCSV)
addressDic = create_address_dic()

package_truck1_keys = [1, 13, 14, 15, 16, 20, 34, 37, 40, 29, 30, 21, 4, 5, 7, 8]
package_truck2_keys = [6, 25, 28, 32, 31, 3, 18, 36, 38, 26]
package_truck3_keys = [10, 11, 9, 23, 24, 27, 33, 35, 2, 12, 19, 17, 39, 22]

truck1 = Truck("truck1")
truck2 = Truck("truck2")
truck3 = Truck("truck3")

load_truck(truck1, package_truck1_keys)
load_truck(truck2, package_truck2_keys)
truck2.current_time = time(9, 5, 00)  # truck 2 leaves when the 9:05 deliveries arrive
load_truck(truck3, package_truck3_keys)

while len(truck1.capacity) != 0:
    deliver_package(truck1)
if len(truck1.capacity) == 0:
    return_to_hub(truck1)
    truck3.current_time = truck1.current_time  # truck 3 cant leave until a tuck gets back

while len(truck2.capacity) != 0:
    deliver_package(truck2)
if len(truck2.capacity) == 0:
    return_to_hub(truck2)

while len(truck3.capacity) != 0:
    deliver_package(truck3)
if len(truck3.capacity) == 0:
    return_to_hub(truck3)

print("Truck 1 stats")
print("{:.2f}".format(truck1.distance_driven))
print(truck1.current_time)
print("Truck 2 stats")
print("{:.2f}".format(truck2.distance_driven))
print(truck2.current_time)
print("Truck 3 stats")
print("{:.2f}".format(truck3.distance_driven))
print(truck3.current_time)
print("total miles driven")
print("{:.2f}".format(truck1.distance_driven + truck2.distance_driven + truck3.distance_driven))
