class Package:

    def __init__(self, id, address, delivery_deadline, mass, notes="n/a", status="AT HUB"):
        self.id = id
        self.address = address
        self.delivery_deadline = delivery_deadline
        self.isDelivered = False
        self.mass = mass
        self.notes = notes
        self.delivered_time = None
        self.status = status

    def __str__(self):
        return f'{self.id}\t {self.address}\t {self.delivered_time}\t {self.status}'
