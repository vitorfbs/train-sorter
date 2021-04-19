from random import randrange
from time import sleep

from clock import Clock

from line import Line
from train import Train

from maintenance_yard import MaintenanceYard
from maintenance_cart import MaintenanceCart

lines_data = {
    0: {
        "id": 0,
        "name": "Rubi",
        "length": 27,
        "maintenance_exit": 0
    },
    1: {
        "id": 1,
        "name": "Diamante",
        "length": 28,
        "maintenance_exit": 1
    },
    2: {
        "id": 2,
        "name": "Esmeralda",
        "length": 27,
        "maintenance_exit": 1
    },
    3: {
        "id": 3,
        "name": "Turquesa",
        "length": 27,
        "maintenance_exit": 0
    },
    4: {
        "id": 4,
        "name": "Coral",
        "length": 31,
        "maintenance_exit": 2
    },
    5: {
        "id": 5,
        "name": "Safira",
        "length": 19,
        "maintenance_exit": 2
    },
    6: {
        "id": 6,
        "name": "Jade",
        "length": 8,
        "maintenance_exit": 2
    }

}

maintenance_yard_data = {
    0: {
        "id": 0,
        "name": "Lapa",
        "exits": 4,
        "line_exits": [7,10],
        "maintenance_cart_number": 16
    },
    1: {
        "id": 1,
        "name": "Altino",
        "exits":2,
        "line_exits": [8,9],
        "maintenance_cart_number": 12
    },
    2: {
        "id": 2,
        "name": "Calmon Viana",
        "exits": 3,
        "line_exits": [11, 12, 13],
        "maintenance_cart_number": 16
    },
}

clock = Clock()

time_randomizer = 10

exit_hours = 3
exit_minutes = 30

class Main:
    def __init__(self):
        self.time_skip = 1
        
        self.lines = []
        self.generate_lines()

        self.maintenance_yards = []
        self.generate_yards()

        
        for line in self.lines:
            print(f"Line {line.name} is online. This line is added to the maintenance schedule")
        
        print("----------------------------")

        for yard in self.maintenance_yards:
            print(f"Yard {yard.name} is created. This maintenance yard will schedule maintenance for the lines it is responsible:")
            for line_exit in yard.line_exits:
                print(f"Line: {line_exit}")
        
    def generate_lines(self):
        for i in range(7):
            new_line = Line(
                lines_data[i]["id"],
                lines_data[i]["name"],
                lines_data[i]["length"],
                lines_data[i]["maintenance_exit"]
            )
            new_line.generate_trains()
            self.lines.append(new_line)

    def generate_yards(self):
        for i in range(3):
            new_yard = MaintenanceYard(
                maintenance_yard_data[i]["id"],
                maintenance_yard_data[i]["name"],
                maintenance_yard_data[i]["exits"],
                maintenance_yard_data[i]["line_exits"],
                maintenance_yard_data[i]["maintenance_cart_number"],
            )
            new_yard.generate_maintenance_carts()
            self.maintenance_yards.append(new_yard)
    
    def manage_yards(self):
        print("----------------------------")
        for line in self.lines:
            print(self.maintenance_yards[line.maintenance_exit].busy_exits)
            print(self.maintenance_yards[line.maintenance_exit].exits)

            if (clock.hours < 1):
                if(self.maintenance_yards[line.maintenance_exit].busy_exits < self.maintenance_yards[line.maintenance_exit].exits):
                    print(f"Line {line.name} is sending a train for maintenance now.")
                    self.send_train_to_maintenance(self.lines.index(line))
                else:
                    print(f"The maintenance exit is busy now. Standby.")

            else:
                if (self.maintenance_yards[line.maintenance_exit].busy_exits < self.maintenance_yards[line.maintenance_exit].exits):
                    if(len(line.trains) >= line.length):
                        print(f"Line {line.name} is currently on capacity. Standby for freeing line.")
                        print(line.length)
                        print(len(line.trains))
                        print(line.trains)
                        
                        self.send_train_to_maintenance(self.lines.index(line))
                    else:                    
                        print(f"Line {line.name} is free for receiving maintanance cart. Managing...")
                        # sleep(1)
                        
                        if(line.maintenance_check < 8):
                            if(self.check_priority(line)):
                                print(f"Prioritizing {line.name} maintenance. Sending cart.")
                                # sleep(1)
                                self.send_maintenance_cart_to_line(self.lines.index(line))
                                print(self.lines.index(line))
                        else:
                            print(f"Line {line.name} is already up to maintenance needs. Sending a cart to the maintenance yard.")
                            self.send_train_to_maintenance(self.lines.index(line))
                    self.maintenance_yards[line.maintenance_exit].busy_exits += 1
                else:
                    print(f"The maintenance exit for the line {line.name} is currently full. Standby for freeing the maintenance exit.")
            print("")

    def check_priority(self, line):
        if(line.maintenance_check > 0):
            return True
        else:
            return False

    def send_train_to_maintenance(self, line):
        if(len(self.lines[line].trains) > 0):
            train = self.lines[line].trains.pop(0)
            if(isinstance(train, Train)):
                self.maintenance_yards[self.lines[line].maintenance_exit].stack.append(train)
                self.lines[line].maintenance_check += 1
            else:
                self.maintenance_yards[self.lines[line].maintenance_exit].secondary_stack.append(train)
            print(self.maintenance_yards[self.lines[line].maintenance_exit].stack)
        else:
            print(f"There are no more trains to send to maintenace. Standby.")


    def send_maintenance_cart_to_line(self, line):
        if(len(self.maintenance_yards[self.lines[line].maintenance_exit].secondary_stack) > 0):
            print(f"Sending cart from {self.maintenance_yards[self.lines[line].maintenance_exit].name} to {self.lines[line].name} for scheduled maintenance.")
            cart = self.maintenance_yards[self.lines[line].maintenance_exit].secondary_stack.pop()
            self.lines[line].trains.append(cart)
        else:
            print(f"There are no more carts for maintenance. Standby.")

    def reset_maintenance_yard_exits(self):
        for yard in self.maintenance_yards:
            self.maintenance_yards[self.maintenance_yards.index(yard)].busy_exits = 0

    def maintenance_countdown_increments(self):
        for yard in self.maintenance_yards:
            if(len(self.maintenance_yards[self.maintenance_yards.index(yard)].stack) > 0):
                for train in self.maintenance_yards[self.maintenance_yards.index(yard)].stack:
                    train_index = self.maintenance_yards[self.maintenance_yards.index(yard)].stack.index(train)
                    self.maintenance_yards[self.maintenance_yards.index(yard)].stack[train_index].maintenance_countdown += self.time_skip

    def send_trains_to_lines(self):
        empty_yards = 0
        for yard in self.maintenance_yards:
            if(len(yard.stack) == 0):
                empty_yards +=1
            elif(yard.stack[-1].maintenance_countdown >= 120):
                print(f"Sending trains from {yard.name}.")
                while(yard.busy_exits < yard.exits):
                    for i in range(len(yard.line_exits)):
                        if(len(yard.stack) > 0):
                            print(f"Sending train back to line {self.lines[i]}.")
                            train = yard.stack.pop()
                            self.lines[i].trains.append(train)
                            yard.busy_exits += 1
                        else:
                            yard.busy_exits = yard.exits
            else:
                print("Waiting for last train to complete maintenance")
        print("")
        return empty_yards

    def randomize_time_skip(self):
        self.time_skip = randrange(1, time_randomizer)

    def check_lines(self):
        for line in self.lines:
            for train in line.trains:
                if(isinstance(train, Train)):
                    return True
        return False


main = Main()

while((clock.hours*60) + clock.minutes < (exit_hours*60 + exit_minutes)
      and main.check_lines()):
    main.randomize_time_skip()

    if (clock.minutes + main.time_skip >= 59):
        clock.hours += 1
        clock.minutes += main.time_skip - clock.minutes
    else:
        clock.minutes += main.time_skip

    print(f"{clock.hours}:{clock.minutes}")

    main.manage_yards()
    main.maintenance_countdown_increments()
    main.reset_maintenance_yard_exits()

    # sleep(1)

for m in main.maintenance_yards:
    print(m.name)
    print(m.stack)

while((clock.hours*60) + clock.minutes < (5*60)):
    print(f"{clock.hours}:{clock.minutes}")
    if (clock.minutes == 59):
        clock.hours += 1
        clock.minutes = 0
    else:
        clock.minutes += 1

trains_to_exit = True

while(trains_to_exit):
    main.randomize_time_skip()
    if (clock.minutes + main.time_skip >= 59):
        clock.hours += 1
        clock.minutes += main.time_skip - clock.minutes
    else:
        clock.minutes += main.time_skip

    print(f"{clock.hours}:{clock.minutes}")
    
    check = main.send_trains_to_lines()
    main.maintenance_countdown_increments()
    main.reset_maintenance_yard_exits()
    if(check >= 3):
        trains_to_exit = False

for m in main.maintenance_yards:
    print(m.name)
    print(m.stack)

print("------------------")
print("Birds flying high")
print("You know how I feel")
print("Sun in the sky")
print("You know how I feel")
print("Breeze driftin' on by")
print("You know how I feel")
print("It's a new dawn")
print("It's a new day")
print("It's a new life")
print("For me")
print("And I'm feeling good")
print("I'm feeling good")