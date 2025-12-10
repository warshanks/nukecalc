# ☢️ NukeCalc

[![Python 3](https://img.shields.io/badge/Python-3-blue.svg)](https://www.python.org/)
[![Factorio](https://img.shields.io/badge/Factorio_Mods-Bob's_Power-orange.svg)](https://mods.factorio.com/mod/bobpower)
[![Plutonium Energy](https://img.shields.io/badge/Factorio_Mods-Plutonium_Energy-cyan.svg)](https://mods.factorio.com/mod/PlutoniumEnergy)
[![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-Hosted_on_GitHub_Pages-green.svg)](https://warshanks.github.io/nukecalc/)

**NukeCalc** is a powerful tool designed to help Factorio engineers calculate the perfect ratios for their nuclear power plants. Specifically tailored for **Bob's Power Mod** and **Plutonium Energy**, it handles the complex math behind reactor tiers, neighbor bonuses, and heat exchanger/turbine ratios.

Available as both a **modern Web App** and a classic **Command-Line Interface (CLI)**.

## ✨ Features

*   **Multi-Tier Support**: Full support for Bob's Mods & Plutonium Energy tiers:
    *   Reactors (Tier 1-3 + MOX + Breeder)
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

You need **Python 3** installed on your machine to run the CLI version.
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

1.  Simply go to https://warshanks.github.io/nukecalc/ in your favorite web browser.

### 💻 Command Line

Run the classic calculator using Python:

```bash
python3 nukecalc.py
```

Follow the interactive prompts to configure your setup:

1.  **Reactor Tier**: Choose between Tier 1-3 or MOX.
2.  **Reactor Count**: Enter `X` for a `2 x X` setup (e.g., entering `2` calculates for a `2x2` setup). You can also enter `0.5` for a single reactor.
3.  **Component Tiers**: Select your Heat Exchanger and Steam Turbine tiers.

Example Output

```text
--- Bob's Mods & Plutonium Energy Nuclear Power Calculator ---
Reactor Tier (1-3, 'MOX', or 'Breeder'): 2
Number of Reactors (2 x X), enter X (or 0.5 for a single reactor): 2
Heat Exchanger Tier (1-4): 2
Steam Turbine Tier (1-3): 2

--- Results ---
Total Reactor Output:  288 MW
Total Tier 2 Exchangers Needed:  28
Total Tier 2 Turbines Needed:  40
Total Offshore Pumps Needed: 2
Potential Layouts for 28 exchangers:
2 groups of 14 (2x7)
Potential Layouts for 40 turbines:
2 groups of 20 (2x10, 4x5, 5x4)
4 groups of 10 (2x5)
```

---
*Happy Factorio-ing! The factory must grow.* 🏭