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

// Main Calculation Function
function calculateNuclearSetup(reactorTier, reactorCount, exchangerTier, turbineTier) {
    const reactorOutputPerUnit = REACTOR_OUTPUTS[reactorTier];
    const exchangerConsumption = EXCHANGER_CONSUMPTION[exchangerTier];
    const turbineOutputPerUnit = TURBINE_OUTPUT[turbineTier];

    let totalOutput = 0;

    // Calculate Neighbor Bonus (from nukecalc.py)
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
        outputTotal.textContent = `${results.totalOutput.toLocaleString()} MW`;
        outputExchangers.textContent = roundUpToEven(results.neededExchangers);
        outputModules.textContent = `${Math.ceil(results.exchangerModules)} groups of 20 heat exchangers (2x10)`;
        outputTurbines.textContent = roundUpToEven(results.neededTurbines);
        outputPumps.textContent = roundUpToEven(results.neededPumps);
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
