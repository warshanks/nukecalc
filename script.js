// Configuration Data (from nukecalc.py)
const REACTOR_OUTPUTS = {
    "1": 54,
    "2": 72,
    "3": 90,
    "MOX": 20,
    "Breeder": 20
};

const EXCHANGER_CONSUMPTION = {
    "1": 7.2,
    "2": 10.8,
    "3": 14.4,
    "4": 18.0
};

const TURBINE_OUTPUT = {
    "1": 5.4,
    "2": 7.2,
    "3": 9.0
};

// Utility function: Rounds a number up to the nearest even integer
function roundUpToEven(f) {
    return Math.ceil(f / 2) * 2;
}

// Utility function: Formats power output with appropriate units (MW, GW, TW, PW, EW)
function formatPower(megawatts) {
    if (megawatts >= 1e12) {
        return `${(megawatts / 1e12).toLocaleString(undefined, { maximumFractionDigits: 2 })} EW`;
    } else if (megawatts >= 1e9) {
        return `${(megawatts / 1e9).toLocaleString(undefined, { maximumFractionDigits: 2 })} PW`;
    } else if (megawatts >= 1e6) {
        return `${(megawatts / 1e6).toLocaleString(undefined, { maximumFractionDigits: 2 })} TW`;
    } else if (megawatts >= 1000) {
        return `${(megawatts / 1000).toLocaleString(undefined, { maximumFractionDigits: 2 })} GW`;
    } else {
        return `${megawatts.toLocaleString()} MW`;
    }
}

function getRectangularLayouts(count) {
    const layouts = [];
    for (let r = 2; r <= Math.sqrt(count); r++) { // Start from 2 to exclude 1xN
        if (count % r === 0) {
            const c = count / r;
            layouts.push(`${r}×${c}`);
            if (r !== c) {
                layouts.push(`${c}×${r}`);
            }
        }
    }
    // Sort by rows numerical order
    layouts.sort((a, b) => {
        const rowA = parseInt(a.split('×')[0]);
        const rowB = parseInt(b.split('×')[0]);
        return rowA - rowB;
    });
    return layouts;
}

function getGroupedLayoutSuggestions(totalItems, reactorCount, only2xN = false) {
    // Potential group sizes: 1 (total), 2 (half), and by reactor count
    // We filter out 0 or invalid counts
    const possibleGroups = [1];
    if (reactorCount > 1) {
        possibleGroups.push(reactorCount);
        if (reactorCount % 2 === 0 && reactorCount > 2) {
            possibleGroups.push(reactorCount / 2); // e.g. for 4 reactors, groups of 2
        }
    }
    // Add 2 as a standard option if not already present and if it makes sense
    if (!possibleGroups.includes(2) && totalItems % 2 === 0) {
        possibleGroups.push(2);
    }

    // Add all other integer factors of totalItems
    for (let i = 2; i <= Math.sqrt(totalItems); i++) {
        if (totalItems % i === 0) {
            possibleGroups.push(i);
            if (i !== totalItems / i) {
                possibleGroups.push(totalItems / i);
            }
        }
    }

    // sort unique
    const uniqueGroups = [...new Set(possibleGroups)].sort((a, b) => a - b);

    const suggestions = [];

    for (const groups of uniqueGroups) {
        // If strict 2xN mode is off (Turbines), we skip if not divisible
        if (!only2xN && totalItems % groups !== 0) continue;

        // Limit max groups for practicality
        if (groups > 12) continue;


        if (only2xN) {
            // Logic for Heat Exchangers: Force 2xN where N is even (so items divisible by 4)
            // We allow "filling up" to the nearest symmetrical numeric, so we don't strictly require divisibility by groups initially.

            const rawItemsPerGroup = totalItems / groups;
            // We want itemsPerGroup to be a multiple of 4 (2 rows * even columns)
            // e.g. 15 -> 16 (2x8). 30 -> 32 (2x16).
            const targetItemsPerGroup = Math.ceil(Math.ceil(rawItemsPerGroup) / 4) * 4;

            const layout = `2×${targetItemsPerGroup / 2}`;
            const totalRequired = targetItemsPerGroup * groups;
            const excess = totalRequired - totalItems;

            let note = "";
            if (excess > 0) {
                // If the symmetry cost is too high (arbitrarily > 4 exchangers total), don't recommend this layout
                if (excess > 4) continue;
                note = ` <span class="note">(+${excess} extra for symmetry)</span>`;
            }

            if (groups === 1) {
                suggestions.push(`${targetItemsPerGroup} (${layout})${note}`);
            } else {
                suggestions.push(`${groups} groups of ${targetItemsPerGroup} (${layout})${note}`);
            }

        } else {
            // Standard logic (Steam Turbines)
            const itemsPerGroup = totalItems / groups;
            const layouts = getRectangularLayouts(itemsPerGroup);

            if (layouts.length === 0) continue;

            if (groups === 1) {
                suggestions.push(`${itemsPerGroup} (${layouts.join(", ")})`);
            } else {
                suggestions.push(`${groups} groups of ${itemsPerGroup} (${layouts.join(", ")})`);
            }
        }
    }

    return suggestions;
}

// Main Calculation Function
function calculateNuclearSetup(reactorTier, reactorCount, exchangerTier, turbineTier) {
    const reactorOutputPerUnit = REACTOR_OUTPUTS[reactorTier];
    const exchangerConsumption = EXCHANGER_CONSUMPTION[exchangerTier];
    const turbineOutputPerUnit = TURBINE_OUTPUT[turbineTier];

    let totalOutput = 0;

    // Calculate Neighbor Bonus (from nukecalc.py)
    let neighborBonus = 1.0;
    if (reactorTier === "MOX") {
        neighborBonus = 1.5;
    } else if (reactorTier === "Breeder") {
        neighborBonus = 0.5;
    }

    if (reactorCount === 1) {
        totalOutput = reactorOutputPerUnit;
    } else if (reactorCount === 2) {
        // Each reactor has 1 neighbor -> (1 + 1 * bonus)
        const multiplier = 1 + neighborBonus;
        totalOutput = reactorCount * reactorOutputPerUnit * multiplier;
    } else {
        // Logic for 2xN layout where N >= 2 (so count >= 4)
        // 4 corners get (1 + 2 * bonus) multiplier
        // The rest (reactorCount - 4) get (1 + 3 * bonus) multiplier
        const cornerMultiplier = 1 + (2 * neighborBonus);
        const middleMultiplier = 1 + (3 * neighborBonus);

        totalOutput = (4 * reactorOutputPerUnit * cornerMultiplier) +
            ((reactorCount - 4) * reactorOutputPerUnit * middleMultiplier);
    }

    const neededExchangers = totalOutput / exchangerConsumption;
    const neededTurbines = totalOutput / turbineOutputPerUnit;
    const neededPumps = (neededExchangers * 12) / 1200;
    const exchangerModules = neededExchangers / 20;

    return {
        totalOutput: totalOutput,
        neededExchangers: neededExchangers,
        neededTurbines: neededTurbines,
        neededPumps: neededPumps,
        exchangerModules: exchangerModules
    };
}

// UI Setup and Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    const reactorTierInput = document.getElementById('reactor-tier');
    const reactorRowsInput = document.getElementById('reactor-count'); // This is 'X' in '2xX'
    const exchangerTierInput = document.getElementById('exchanger-tier');
    const turbineTierInput = document.getElementById('turbine-tier');

    // Output Elements
    const outputTotal = document.getElementById('total-output');
    const outputExchangers = document.getElementById('needed-exchangers');
    const outputModules = document.getElementById('exchanger-modules');
    const outputTurbines = document.getElementById('needed-turbines');
    const outputTurbineLayouts = document.getElementById('turbine-layouts');
    const outputPumps = document.getElementById('needed-pumps');

    function updateCalculations() {
        const rTier = reactorTierInput.value;
        const rows = parseFloat(reactorRowsInput.value) || 1; // Default to 1 if empty/invalid
        let reactorCount;

        if (rows === 0.5) {
            reactorCount = 1;
        } else {
            // Logic: Input is X for 2xX
            reactorCount = Math.floor(Math.max(1, rows)) * 2;
        }

        const eTier = exchangerTierInput.value;
        const tTier = turbineTierInput.value;

        // Ensure we have valid inputs for calculation
        const validReactorCount = Math.max(1, reactorCount);

        const results = calculateNuclearSetup(rTier, validReactorCount, eTier, tTier);

        // Update UI
        // Animate numbers? For now, just set them.
        outputTotal.textContent = formatPower(results.totalOutput);
        outputExchangers.textContent = roundUpToEven(results.neededExchangers).toLocaleString();

        const totalExchangers = roundUpToEven(results.neededExchangers);
        const exchangerSuggestions = getGroupedLayoutSuggestions(totalExchangers, validReactorCount, true);
        outputModules.innerHTML = exchangerSuggestions.length > 0
            ? `Potential Layouts:<br>${exchangerSuggestions.join("<br>")}`
            : "No even rectangular layouts found.";

        const totalTurbines = roundUpToEven(results.neededTurbines);
        const turbineSuggestions = getGroupedLayoutSuggestions(totalTurbines, validReactorCount);

        outputTurbines.textContent = totalTurbines.toLocaleString();
        outputTurbineLayouts.innerHTML = turbineSuggestions.length > 0
            ? `Potential Layouts:<br>${turbineSuggestions.join("<br>")}`
            : "No non-linear layouts found.";

        outputPumps.textContent = Math.ceil(results.neededPumps).toLocaleString();
    }

    // Attach listeners
    const inputs = [reactorTierInput, reactorRowsInput, exchangerTierInput, turbineTierInput];
    inputs.forEach(input => {
        input.addEventListener('input', updateCalculations);
        input.addEventListener('change', updateCalculations); // For selects
    });

    // Initial run
    updateCalculations();
});
