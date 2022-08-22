# WGU C950 Paul Overfelt 009278142

import csv

from Package import Package
from hash_table import HashMap
from truck import Truck
from datetime import datetime, date, time, timedelta


# Reads package data from a supplied CSV File
# O(n)
def read_package_data(fileName):
    # Open the file
    with open(fileName) as packageData:
        packages = csv.reader(packageData, delimiter=',')
        # Loop through the file and create a package object for each line
        for p in packages:
            id = int(p[0])
            address = p[1]
            city = p[2]
            zip = p[4]
            delivery_deadline = p[5]
            weight = p[6]
            note = p[7]

            new_package = Package(id, address, delivery_deadline, weight, city, zip, note)

            # Add the package to the hash
            packageHash.add(id, new_package)


# opens the distance file and turns it into a addressable 2d list
# O(1)
def read_distance_data(fileName):
    with open(fileName) as distanceData:
        distanceList = list(csv.reader(distanceData, delimiter=','))
        return distanceList


# opens the address list file and turns it into a addressable 2d list
# O(1)
def read_address_data(fileName):
    with open(fileName) as addressData:
        addressList = list(csv.reader(addressData, delimiter=','))
        return addressList


# Finds distance between two indexes on the distance table
# takes the addresses in as indexes of the table
# O(1)
def distance_between(row, col):
    distance = distanceList[row][col]
    # Since half of the CSV is blank need to check for the mirrored solution
    if distance == '':
        distance = distanceList[col][row]

    return float(distance)


# Greedy algo implementation
# Takes in a truck object and returns the next package that should be delivered that is in the truck)
# O(n)
def find_next_shortest_delivery(truck):
    package_list = truck.capacity  # List of packages on the truck
    current_address_index = addressDic.get(truck.location)  # Gets the index of the current truck location
    shortest_package_address_index = addressDic.get(
        package_list[0].address)  # gets the first package from the package list
    shortest_package = package_list[0]  # sets that as the shortest package
    # Loop through packages on the truck
    for package in package_list:
        next_package_address_index = addressDic.get(package.address)  # gets the package index
        # Finds distance between current address and the currently selected shortest package address
        selected_package_distance = distance_between(int(current_address_index), int(shortest_package_address_index))
        # Finds the distance between the current address and the next package in the list
        next_package_distance = distance_between(int(current_address_index), int(next_package_address_index))

        # If the next package distance is shorter than the currently selected shortest package distance
        # Set that package as the shortest distance
        if next_package_distance < selected_package_distance:
            shortest_package_address_index = next_package_address_index
            shortest_package = package

    return shortest_package


# Creates a dictionary of addresses and address indexes
# Address : address index
# O(n)
def create_address_dic():
    address_dic = {}
    for address in addressList:
        address_dic[address[2]] = address[0]
    return address_dic


# Loads the truck with the list of package id's
# O(n)
def load_truck(truck, packages_to_load):
    for package in packages_to_load:
        truck.load_package(packageHash.get(package))
        packageHash.get(package).loading_time = truck.current_time
        packageHash.get(package).status = f"En route"


# Delivers a package on the passed in truck
# O(1)
def deliver_package(truck):
    # Finds the next shortest Delivery on the truck ( Greedy Algo)
    package = find_next_shortest_delivery(truck)

    # Finds the delivery index of the package's address
    delivery_address = package.address
    delivery_address_index = addressDic[delivery_address]

    # Finds the index of the trucks current address
    truck_location_index = addressDic[truck.location]

    # Finds the distance between the two addresses
    driving_distance = distance_between(int(delivery_address_index), int(truck_location_index))
    # Finds the time it take to get to the new address
    driving_time_delta = timedelta(hours=driving_distance / truck.speed)
    d = date.today()
    t = truck.current_time
    truck_departure_time = datetime.combine(d, t)
    # When the truck left its last stop + how long it took to get there
    truck_delivery_time = truck_departure_time + driving_time_delta

    # Updates the trucks address
    truck.location = package.address
    # Adds the driving distance for the total
    truck.distance_driven += driving_distance
    # Sets the current time for delivery
    truck.current_time = truck_delivery_time.time()
    # Sets when the package was delivered
    package.delivered_time = truck.current_time
    # Sets that the package was delivered
    package.isDelivered = True
    package.status = 'DELIVERED'
    # Removes the package from the truck
    truck.package_delivered(package)


# Returns the truck to the hub
# O(1)
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


# Star of the main program
print("WGUPS Package System")
print("Delivering Packages")

# Creates an empty hashmap
packageHash = HashMap()

# Locations of CSV Files
packageDataCSV = "data/package_data.csv"
distanceDataCSV = "data/distance_table.csv"
addressDataCSV = "data/address_data.csv"

read_package_data(packageDataCSV)  # inserts package data into hash map
distanceList = read_distance_data(distanceDataCSV)  # reads distance data
addressList = read_address_data(addressDataCSV)  # reads address data
addressDic = create_address_dic()  # creates a dictionary of address data

# List of packages ID's to be loaded on trucks
package_truck1_keys = [1, 13, 14, 15, 16, 20, 34, 37, 40, 29, 30, 21, 4, 5, 7, 8]
package_truck2_keys = [6, 25, 28, 32, 31, 3, 18, 36, 38, 26]
package_truck3_keys = [10, 11, 9, 23, 24, 27, 33, 35, 2, 12, 19, 17, 39, 22]

# Creation of truck objects
truck1 = Truck("truck1")
truck2 = Truck("truck2")
truck3 = Truck("truck3")

# Load and deliver the first trucks packages
load_truck(truck1, package_truck1_keys)
while len(truck1.capacity) != 0:
    deliver_package(truck1)
if len(truck1.capacity) == 0:
    return_to_hub(truck1)
    truck3.current_time = truck1.current_time  # truck 3 cant leave until a tuck gets back

print(f"Truck 1 has finished its route and returned to the hub at {truck1.current_time}")
print(f"Truck 1 drove {truck1.distance_driven:.2f} miles")

# Load and deliver the second trucks packages
truck2.current_time = time(9, 5, 00)  # truck 2 leaves when the 9:05 deliveries arrive
load_truck(truck2, package_truck2_keys)
while len(truck2.capacity) != 0:
    deliver_package(truck2)
if len(truck2.capacity) == 0:
    return_to_hub(truck2)

print(f"Truck 2 has finished its route and returned to the hub at {truck2.current_time}")
print(f"Truck 2 drove {truck2.distance_driven:.2f} miles")

# Load and deliver the 3rd truck after the first truck comes back to the hub
load_truck(truck3, package_truck3_keys)
while len(truck3.capacity) != 0:
    deliver_package(truck3)
if len(truck3.capacity) == 0:
    return_to_hub(truck3)

print(f"Truck 3 has finished its route and returned to the hub at {truck3.current_time}")
print(f"Truck 3 drove {truck3.distance_driven:.2f} miles")

total_distance_driven = truck1.distance_driven + truck2.distance_driven + truck3.distance_driven
print(f"Total Distance Driven is: {total_distance_driven:.2f} miles")

# User Menu to lookup package status at a time
user_input = ''
while user_input != "3":

    # Main display Menu
    print("-------------------------------------------------")
    print("Please select from the options below:")
    print("1. Get Status for single package")
    print("2. Get Status of all Packages at a time")
    print("3. Quit")

    user_input = input("Enter Your Selection: ")

    # If he user wants to get view a single package
    if user_input == "1":
        # What time do they want to view
        input_time = input("Enter a time (HH:MM:SS) in 24H format: ")
        # Split the input into 3 vars
        (hrs, mins, secs) = input_time.split(":")
        # Make a time object
        user_time = time(int(hrs), int(mins), int(secs))
        # Find the Package ID
        user_package_key = input("Enter Package ID to Display: ")
        # Get that package
        user_package_selection = packageHash.get(int(user_package_key))
        # Set the delivery status to what it would be at that time
        user_package_selection.package_delivery_status_at_time(user_time)
        # Print the status for that package
        print("Package ID ".ljust(15) + "Package Address".ljust(40) + "Deadline".ljust(10) + "Delivery Time".ljust(
            15) + "Status".ljust(10))
        print(str(user_package_selection.id).ljust(15) + user_package_selection.address.ljust(40) + str(
            user_package_selection.delivery_deadline).ljust(10) + str(user_package_selection.delivered_time).ljust(
            15) + user_package_selection.status)

    # If the user wants to see all packages
    if user_input == "2":
        # What time do they want to view
        input_time = input("Enter a time (HH:MM:SS) in 24H format: ")
        # Split the input into 3 vars
        (hrs, mins, secs) = input_time.split(":")
        # Make a time object
        user_time = time(int(hrs), int(mins), int(secs))
        # Get all the packages from the hash table
        all_package_list = packageHash.return_all_items()
        # Print the header
        print("Package ID ".ljust(15) + "Package Address".ljust(40) + "Deadline".ljust(10) + "Delivery Time".ljust(
            415) + "Status".ljust(10))
        # Loop through all the packages and print the status out at that time
        for package in all_package_list:
            package.package_delivery_status_at_time(user_time)
            print(
                str(package.id).ljust(15) + package.address.ljust(40) + str(package.delivery_deadline).ljust(10) + str(
                    package.delivered_time).ljust(15) + package.status)
