class Flight():

  def __init__(self, capacity):
    self.capacity = capacity
    self.passangers = []
  
  def add_passangers(self, name):
    if not self.open_seats():
      return False
    self.passangers.append(name)
    return True

  def open_seats(self):
    return self.capacity - len(self.passangers)
  



flight = Flight(3)

people = ["Harry", "Ron", "Hermione", "Ginny"]

for person in people:
  if flight.add_passangers(person):
    print(f"Added {person} to flight successfully")
  else:
    print(f"No seats availabe for {person}")



'''
Added Harry to flight successfully
Added Ron to flight successfully
Added Hermione to flight successfully
No seats availabe for Ginny
'''