import csv

from Package import Package
from hash_table import HashMap
import csvHandler


def read_package_data(fileName):
    with open(fileName) as packageData:
        packages = csv.reader(packageData, delimiter=",")
        for p in packages:
            id = int(p[0])
            address = p[1] + p[2] + p[3] + p[4]
            delivery_deadline = p[5]
            weight = p[6]
            note = p[7]

            new_package = Package(id, address, delivery_deadline, weight, note)

            packageHash.add(id, new_package)


packageHash = HashMap

packageDataCSV = "data/package_data.csv"

read_package_data(packageDataCSV)

packageHash.print()
