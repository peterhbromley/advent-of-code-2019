# PART 1

def fuel_from_mass(mass):
    return mass // 3 - 2

def part_1():
    with open('input.txt') as f:
        total_fuel = sum(
            fuel_from_mass(int(mass)) for mass in f
        )
    print("Answer to part 1: {}".format(total_fuel))


# PART 2

def fuel_from_module_and_fuel(mass):
    fuel = fuel_from_mass(mass)
    if fuel < 1:
        return 0
    else:
        return fuel + fuel_from_module_and_fuel(fuel)

def part_2():
    with open('input.txt') as f:
        total_fuel = sum(
            fuel_from_module_and_fuel(int(mass)) for mass in f
        )
    print("Answer to part 2: {}".format(total_fuel))

part_1()
part_2()