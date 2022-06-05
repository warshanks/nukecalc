# Calculator for nuclear power setups in Factorio
from math import ceil

def round_up_to_even(f):
    return ceil(f / 2.) * 2

mode = ""
while True:
    mode = input("[A] Normal Mode\n[B] EZ Mode (Vanilla Only)\n")
    mode = mode.lower()
    if mode not in ("a", "b"):
        print("Invalid input.")
    else:
        break

if mode == "a":
    modset = ""
    while True:
        modset = input("Which mod set are you using?\n[A] Bob's Mods\n[B] Space Exploration\n[C] Vanilla/Angel's\n(Bob's Power overwrites Angel's nuclear if used together)\n")
        modset = modset.lower()
        if modset not in ("a", "b", "c"):
            print("Invalid input.")
        else:
            break

    basepower = 0
    while basepower == 0:
        basepower = input("Base Power Output: ")
        basepower = int(basepower)

    reactorcount = 0
    while reactorcount <= 0:
        reactorcount = input("Number of Reactors (2 x X): ")
        reactorcount = int(reactorcount)
        reactorcount = reactorcount * 2

    exchangerlevel = 0

    if modset == "a":
        while exchangerlevel != 1 or 2 or 3:
            exchangerlevel = input("Heat Exchanger Tier (1-3): ")
            exchangerlevel = int(exchangerlevel)
            if 0 < exchangerlevel < 4:
                break

        if exchangerlevel == 1:
            exchangerconsumption = 10.8

        if exchangerlevel == 2:
            exchangerconsumption = 14.4

        if exchangerlevel == 3:
            exchangerconsumption = 18.0

        turbinelevel = 0
        while turbinelevel != 1 or 2 or 3:
            turbinelevel = input("Steam Turbine Tier (1-3): ")
            turbinelevel = int(turbinelevel)
            if 0 < turbinelevel < 4:
                break

        if turbinelevel == 1:
            turbineconsumption = 5.4

        if turbinelevel == 2:
            turbineconsumption = 7.2

        if turbinelevel == 3:
            turbineconsumption = 9.0

        if reactorcount <= 4:
            neighborbonus = (basepower * 2) * reactorcount

        if reactorcount >= 6:
            reactorcount = reactorcount - 4
            neighborbonus = ((basepower * 4) * reactorcount) + ((basepower * 3) * 4)

        neededexchangers = neighborbonus / exchangerconsumption
        neededturbines = neighborbonus / turbineconsumption
        neededpumps = (neededexchangers * 120) / 1200
        exchangermodules = neededexchangers / 20

        print("Total Reactor Output: ", neighborbonus)
        print("Total Tier", exchangerlevel, "Exchangers Needed: ", round_up_to_even(neededexchangers))
        print("Total Tier", turbinelevel, "Turbines Needed: ", round_up_to_even(neededturbines))
        print("Total Offshore Pumps Needed:", round_up_to_even(neededpumps))
        print("You will need", ceil(exchangermodules), "groups of 20 heat exchangers (2x10)")

    if modset == "b":
        while exchangerlevel != 1 or 2:
            exchangerlevel = input("Heat Exchanger Tier (1-2): ")
            exchangerlevel = int(exchangerlevel)
            if 0 < exchangerlevel < 3:
                break

        if exchangerlevel == 1:
            exchangerconsumption = 10

        if exchangerlevel == 2:
            exchangerconsumption = 560

        turbinelevel = 0
        while turbinelevel != 1 or 2:
            turbinelevel = input("Steam Turbine Tier (1-2): ")
            turbinelevel = int(turbinelevel)
            if 0 < turbinelevel < 3:
                break

        if turbinelevel == 1:
            turbineconsumption = 5.82

        if turbinelevel == 2:
            turbineconsumption = 1000

        if reactorcount <= 4:
            neighborbonus = (basepower * 2) * reactorcount

        if reactorcount >= 6:
            reactorcount = reactorcount - 4
            neighborbonus = ((basepower * 4) * reactorcount) + ((basepower * 3) * 4)

        neededexchangers = neighborbonus / exchangerconsumption
        neededturbines = neighborbonus / turbineconsumption
        neededpumps = (neededexchangers * 103) / 1200
        exchangermodules = neededexchangers / 22

        print("Total Reactor Output: ", neighborbonus)
        print("Total Tier", exchangerlevel, "Exchangers Needed: ", round_up_to_even(neededexchangers))
        print("Total Tier", turbinelevel, "Turbines Needed: ", round_up_to_even(neededturbines))

        if exchangerlevel == 1:
            print("You will need", ceil(exchangermodules), "groups of 22 heat exchangers (2x11)")
            print("Total Offshore Pumps Needed:", round_up_to_even(neededpumps))

    if modset == "c":
        exchangerlevel == 1
        exchangerconsumption = 10

        turbinelevel = 1
        turbineconsumption = 5.82

        if reactorcount <= 4:
            neighborbonus = (basepower * 2) * reactorcount

        if reactorcount >= 6:
            reactorcount = reactorcount - 4
            neighborbonus = ((basepower * 4) * reactorcount) + ((basepower * 3) * 4)

        neededexchangers = neighborbonus / exchangerconsumption
        neededturbines = neighborbonus / turbineconsumption
        neededpumps = (neededexchangers * 103) / 1200
        exchangermodules = neededexchangers / 22

        print("Total Reactor Output: ", neighborbonus)
        print("Total Exchangers Needed: ", round_up_to_even(neededexchangers))
        print("Total Turbines Needed: ", round_up_to_even(neededturbines))
        print("You will need", ceil(exchangermodules), "groups of 22 heat exchangers (2x11)")
        print("Total Offshore Pumps Needed:", round_up_to_even(neededpumps))

if mode == "b":
    powerneeded = input("Total desired power output in MW: ")
    powerneeded = float(powerneeded)

    if powerneeded <= 160:
        print("You will need a 2x1 reactor setup")
        print("You will need 16 heat exchangers (2x8) and 2 offshore pumps")
        print("You will need 28 steam turbines")
        print("This setup will make 160MW")

    if 160 < powerneeded <= 320:
        print("You will need a 2x2 reactor setup")
        print("You will need 32 heat exchangers (2x8) and 4 offshore pumps")
        print("You will need 56 steam turbines")
        print("This setup will make 320MW")

    if 320 < powerneeded <= 800:
        print("You will need a 2x3 reactor setup")
        print("You will need 80 heat exchangers (2x8) and 10 offshore pumps")
        print("You will need 138 steam turbines")
        print("This setup will make 800MW")

    if 800 < powerneeded <= 1120:
        print("You will need a 2x4 reactor setup")
        print("You will need 112 heat exchangers (2x8) and 14 offshore pumps")
        print("You will need 194 steam turbines")
        print("This setup will make 1120MW")

    if powerneeded > 1120:
        print("Use Normal Mode and leave me alone.")            