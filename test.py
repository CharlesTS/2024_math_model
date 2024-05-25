import generate_electricity

contain = 100
p = 50
battery = generate_electricity.BatterySystem(contain,p)

charge = 50
print(battery.battery_charge(charge))