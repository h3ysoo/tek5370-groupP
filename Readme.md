# TEK5370 Group P: Effects of Balcony Solar Power Plants on Distribution Grids

Group project in **TEK5370 Grid, Smart Grid and IoT** at the University of Oslo (Autumn 2026).

## Research question

How, and how strongly, do balcony solar power plants (1.8 kWp each) influence the distribution grid and a specific distribution line, if at all?

## Approach

1. Build a distribution grid model in [pandapower](https://www.pandapower.org/) with the same characteristics as the 11 kV radial network described in T. Oldernes' master's thesis (NTNU, 2026).
2. Add low-voltage feeders where the balcony PV units are connected.
3. Run power flow simulations for a matrix of scenarios:
   - **Grid load level:** low (summer minimum), medium (summer median), high (winter peak)
   - **PV output:** none, partial, full power (e.g. clear summer noon, cold clear winter day at -20 °C)
   - **Penetration:** share of households with a balcony PV unit
4. Evaluate voltage levels, line and transformer loading, losses and reverse power flow.

## Setup

Requires Python 3.12 (newer versions may not yet be supported by all dependencies).

**macOS / Linux**

```bash
git clone https://github.com/h3ysoo/tek5370-groupP.git
cd tek5370-groupP
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows**

```bash
git clone https://github.com/h3ysoo/tek5370-groupP.git
cd tek5370-groupP
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Jupyter kernel (for notebooks in VS Code)**

Register the virtual environment as a named kernel, then select **TEK5370 (.venv)** as the kernel in VS Code (Select Kernel > Jupyter Kernel):

```bash
python -m ipykernel install --user --name tek5370 --display-name "TEK5370 (.venv)"
```

## Files

| File | Description |
|---|---|
| `balcony_demo.py` | Minimal demo: 11/0.4 kV transformer feeding a 400 V street with 10 houses, each with a 1.8 kW balcony PV unit. Compares voltage, transformer loading and grid exchange in four scenarios, with and without PV. |
| `minimal_example.ipynb` | pandapower minimal example, adapted from the official pandapower tutorials. |
| `requirements.txt` | Python dependencies. |

Run the demo:

```bash
python balcony_demo.py
```

## Notes

- The original network data (Elvia) used in the thesis is not public. Our grid is a synthetic equivalent that reproduces the key characteristics reported in the thesis.
- Do not commit the thesis, course material or other third-party documents to this repository.

## References

- L. Thurner et al., "pandapower: An Open-Source Python Tool for Convenient Modeling, Analysis, and Optimization of Electric Power Systems," *IEEE Transactions on Power Systems*, vol. 33, no. 6, pp. 6510-6521, 2018. doi: 10.1109/TPWRS.2018.2829021
- T. Oldernes, *Master's thesis on medium voltage regulators in Norwegian distribution grids*, NTNU, 2026.
- pandapower documentation: https://pandapower.readthedocs.io
- pandapower tutorials: https://github.com/e2nIEE/pandapower/tree/develop/tutorials
