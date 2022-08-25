class Package:

    def __init__(self, id, address, delivery_deadline, mass, city, zip, notes="n/a", loading_time="n/a",
                 status="AT HUB"):
        self.id = id
        self.address = address
        self.delivery_deadline = delivery_deadline
        self.city = city
        self.zip = zip
        self.isDelivered = False
        self.mass = mass
        self.notes = notes
        self.loading_time = loading_time
        self.delivered_time = None
        self.status = status

    # Sets the package delivery status based on the input time
    # O(1)
    def package_delivery_status_at_time(self, requested_time):
        if requested_time < self.loading_time:
            self.status = "AT HUB"

        elif requested_time > self.delivered_time:
            self.status = "DELIVERED"

        elif requested_time > self.loading_time or self.delivered_time is None:
            self.status = "EN ROUTE"
