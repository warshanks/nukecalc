# Calculator for nuclear power setups in Factorio with Bob's Power Mod and Plutonium Energy
from math import ceil

# Configuration Data
REACTOR_OUTPUTS = {
    1: 54,
    2: 72,
    3: 90,
    "MOX": 20,
    "Breeder": 20
}

EXCHANGER_CONSUMPTION = {
    1: 7.2,
    2: 10.8,
    3: 14.4,
    4: 18.0
}

TURBINE_OUTPUT = {
    1: 5.4,
    2: 7.2,
    3: 9.0
}


def round_up_to_even(f):
    """Rounds a number up to the nearest even integer."""
    return ceil(f / 2.) * 2


def get_layout_options(total_count):
    """
    Returns a list of string layouts 'RxC' where R * C == total_count.
    Only allows layouts where R and C are integers.
    Excludes 1xN calculations (where R or C is 1).
    """
    layouts = []
    for r in range(2, int(total_count**0.5) + 1):  # Start from 2 to exclude 1xN
        if total_count % r == 0:
            c = total_count // r
            # Add both RxC and CxR
            layouts.append(f"{r}x{c}")
            if r != c:
                layouts.append(f"{c}x{r}")

    # Sort by number of rows for consistency
    layouts.sort(key=lambda s: int(s.split('x')[0]))
    return layouts


def get_valid_input(prompt, valid_options, transform=int):
    """
    Prompts the user for input until a valid option is provided.

    Args:
        prompt (str): The prompt to display to the user.
        valid_options (container): A container (set, list, range) of valid values.
        transform (func): A function to transform the input string (default: int).

    Returns:
        The transformed valid input.
    """
    while True:
        try:
            user_input = input(prompt)
            value = transform(user_input)
            if value in valid_options:
                return value
            else:
                print(f"Invalid input. Please enter one of: {sorted(list(valid_options), key=str)}")
        except ValueError:
            print("Invalid input. Please enter a number.")


def calculate_nuclear_setup(reactor_tier, reactor_count, exchanger_tier, turbine_tier):
    """
    Calculates the requirements for a nuclear setup.

    Args:
        reactor_tier (int): The tier of the reactor (1-3).
        reactor_count (int): The number of reactors.
        exchanger_tier (int): The tier of the heat exchanger (1-4).
        turbine_tier (int): The tier of the steam turbine (1-3).

    Returns:
        dict: A dictionary containing the calculation results.
    """
    reactor_output_per_unit = REACTOR_OUTPUTS[reactor_tier]
    exchanger_consumption = EXCHANGER_CONSUMPTION[exchanger_tier]
    turbine_output_per_unit = TURBINE_OUTPUT[turbine_tier]

    # Calculate Neighbor Bonus
    # Calculate Neighbor Bonus
    if str(reactor_tier).upper() == "MOX":
        neighbor_bonus = 1.5
    elif str(reactor_tier).capitalize() == "Breeder":
        neighbor_bonus = 0.5
    else:
        neighbor_bonus = 1.0

    if reactor_count == 1:
        total_output = reactor_output_per_unit
    elif reactor_count == 2:
        # Each reactor has 1 neighbor -> (1 + 1 * bonus)
        multiplier = 1 + neighbor_bonus
        total_output = reactor_count * reactor_output_per_unit * multiplier
    else:
        # Logic for 2xN layout where N >= 2
        # 4 corners get (1 + 2 * bonus) multiplier
        # The rest (reactor_count - 4) get (1 + 3 * bonus) multiplier
        corner_multiplier = 1 + (2 * neighbor_bonus)
        middle_multiplier = 1 + (3 * neighbor_bonus)

        total_output = (4 * reactor_output_per_unit * corner_multiplier) + \
                       ((reactor_count - 4) * reactor_output_per_unit * middle_multiplier)

    needed_exchangers = total_output / exchanger_consumption
    needed_turbines = total_output / turbine_output_per_unit
    needed_pumps = (needed_exchangers * 12) / 1200
    exchanger_modules = needed_exchangers / 20

    return {
        "total_output": total_output,
        "needed_exchangers": needed_exchangers,
        "needed_turbines": needed_turbines,
        "needed_pumps": needed_pumps,
        "exchanger_modules": exchanger_modules
    }


def main():
    print("--- Bob's Mods & Plutonium Energy Nuclear Power Calculator ---")

    def parse_reactor_tier(val):
        if val.lower() == "mox":
            return "MOX"
        if val.lower() == "breeder":
            return "Breeder"
        return int(val)

    reactor_tier = get_valid_input("Reactor Tier (1-3, 'MOX', or 'Breeder'): ", [1, 2, 3, "MOX", "Breeder"], transform=parse_reactor_tier)

    # Reactor count logic: Input is X for 2xX, so actual count is 2*X
    # The original code asked for "Number of Reactors (2 x X)" and multiplied input by 2.
    # We'll keep that logic but make it clearer.
    # We'll accept any positive integer for the 'X' part.
    while True:
        try:
            rows_input = input("Number of Reactors (2 x X), enter X (or 0.5 for a single reactor): ")
            rows = float(rows_input)
            if rows == 0.5:
                reactor_count = 1
                break
            elif rows >= 1 and rows.is_integer():
                reactor_count = int(rows) * 2
                break
            else:
                print("Please enter a number >= 1, or 0.5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    exchanger_tier = get_valid_input("Heat Exchanger Tier (1-4): ", [1, 2, 3, 4])
    turbine_tier = get_valid_input("Steam Turbine Tier (1-3): ", [1, 2, 3])

    results = calculate_nuclear_setup(reactor_tier, reactor_count, exchanger_tier, turbine_tier)

    print("\n--- Results ---")
    print("Total Reactor Output: ", results["total_output"], "MW")
    print(f"Total Tier {exchanger_tier} Exchangers Needed: ", round_up_to_even(results["needed_exchangers"]))
    print(f"Total Tier {turbine_tier} Turbines Needed: ", round_up_to_even(results["needed_turbines"]))
    print("Total Offshore Pumps Needed:", ceil(results["needed_pumps"]))

    # Grouped Layout Suggestions Logic
    def get_grouped_layout_suggestions(total_items, reactor_count, only_2xN=False):
        possible_groups = [1]
        if reactor_count > 1:
            possible_groups.append(reactor_count)
            if reactor_count % 2 == 0 and reactor_count > 2:
                possible_groups.append(int(reactor_count / 2))

        if 2 not in possible_groups and total_items % 2 == 0:
            possible_groups.append(2)

        # Add all other integer factors of total_items
        for i in range(2, int(total_items**0.5) + 1):
            if total_items % i == 0:
                possible_groups.append(i)
                if i != total_items // i:
                    possible_groups.append(total_items // i)

        unique_groups = sorted(list(set(possible_groups)))
        suggestions = []

        for groups in unique_groups:
            # If strict 2xN mode is off, we skip if not divisible
            if not only_2xN and total_items % groups != 0:
                continue

            if only_2xN:
                # Logic for Heat Exchangers: Force 2xN where N is even (items divisible by 4)
                raw_items_per_group = total_items / groups
                target_items_per_group = ceil(ceil(raw_items_per_group) / 4) * 4

                layout_n = int(target_items_per_group / 2)
                layout = f"2x{layout_n}"
                total_required = target_items_per_group * groups
                excess = int(total_required - total_items)

                note = ""
                if excess > 0:
                    note = f" (+{excess} extra for symmetry)"

                if groups == 1:
                    suggestions.append(f"{target_items_per_group} ({layout}){note}")
                else:
                    suggestions.append(f"{groups} groups of {target_items_per_group} ({layout}){note}")

            else:
                items_per_group = int(total_items / groups)
                layouts = get_layout_options(items_per_group)

                if not layouts:
                    continue

                if groups == 1:
                    suggestions.append(f"{items_per_group} ({', '.join(layouts)})")
                else:
                    suggestions.append(f"{groups} groups of {items_per_group} ({', '.join(layouts)})")

        return suggestions

    needed_exchangers = round_up_to_even(results["needed_exchangers"])
    exchanger_suggestions = get_grouped_layout_suggestions(needed_exchangers, reactor_count, only_2xN=True)

    print(f"Potential Layouts for {needed_exchangers} exchangers:")
    if exchanger_suggestions:
        for suggestion in exchanger_suggestions:
            print(suggestion)
    else:
        print("No even rectangular layouts found.")

    needed_turbines = round_up_to_even(results["needed_turbines"])
    turbine_suggestions = get_grouped_layout_suggestions(needed_turbines, reactor_count)

    print(f"Potential Layouts for {needed_turbines} turbines:")
    if turbine_suggestions:
        for suggestion in turbine_suggestions:
            print(suggestion)
    else:
        print("No non-linear layouts found.")



if __name__ == "__main__":
    main()
