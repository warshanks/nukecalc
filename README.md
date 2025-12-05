# ☢️ NukeCalc

[![Python 3](https://img.shields.io/badge/Python-3-blue.svg)](https://www.python.org/)
[![Factorio](https://img.shields.io/badge/Factorio-Bob's_Mods-orange.svg)](https://mods.factorio.com/mod/bobpower)

**NukeCalc** is a powerful tool designed to help Factorio engineers calculate the perfect ratios for their nuclear power plants. Specifically tailored for **Bob's Power Mod**, it handles the complex math behind reactor tiers, neighbor bonuses, and heat exchanger/turbine ratios.

Available as both a **modern Web App** and a classic **Command-Line Interface (CLI)**.

## ✨ Features

*   **Multi-Tier Support**: Full support for Bob's Mods tiers:
    *   Reactors (Tier 1-3 + MOX)
    *   Heat Exchangers (Tier 1-4)
    *   Steam Turbines (Tier 1-3)
*   **Smart Calculations**: Automatically calculates total power output based on reactor count and neighbor bonuses.
*   **2xN Layout Optimization**: Optimized for the standard, efficient 2xN reactor layouts.
*   **Resource Management**: Tells you exactly how many:
    *   Heat Exchangers
    *   Steam Turbines
    *   Offshore Pumps
    *   ...you need to build to fully utilize your reactors.

## 🚀 Getting Started

### Prerequisites

You need **Python 3** installed on your machine.
*   [Download Python 3](https://www.python.org/downloads/)

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/warshanks/nukecalc.git
    cd nukecalc
    ```

## 🎮 Usage

### 🌐 Web App (New!)

The easiest way to use NukeCalc is through the new modern web interface.

1.  Simply open `index.html` in your favorite web browser.
    *   *Mac/Linux*: `open index.html`
    *   *Windows*: Double-click `index.html`
2.  Enjoy the premium dark-mode interface with real-time calculations.

### 💻 Command Line

Run the classic calculator using Python:

```bash
python3 nukecalc.py
```

Follow the interactive prompts to configure your setup:

1.  **Reactor Tier**: Choose between Tier 1-3 or MOX.
2.  **Reactor Count**: Enter `X` for a `2 x X` setup (e.g., entering `2` calculates for a `2x2` setup).
3.  **Component Tiers**: Select your Heat Exchanger and Steam Turbine tiers.

### Example Output

```text
--- Bob's Mods Nuclear Power Calculator ---
Reactor Tier (1-3, or 'MOX'): 2
Number of Reactors (2 x X), enter X: 2
Heat Exchanger Tier (1-4): 2
Steam Turbine Tier (1-3): 2

--- Results ---
Total Reactor Output:  288
Total Tier 2 Exchangers Needed:  28
Total Tier 2 Turbines Needed:  40
Total Offshore Pumps Needed: 2
You will need 2 groups of 20 heat exchangers (2x10)
```

---
*Happy Factorio-ing! The factory must grow.* 🏭