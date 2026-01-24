# Optimization for Energy Systems

This chapter introduces optimization techniques used in energy system modelling.

## Linear Programming

Many energy system problems can be formulated as linear programs (LP):

$$\min_x \quad c^T x$$
$$\text{s.t.} \quad Ax \leq b$$
$$\quad \quad x \geq 0$$

### Example: Economic Dispatch

Find the least-cost way to meet demand:

$$\min \sum_{g} c_g \cdot p_g$$

subject to:

$$\sum_{g} p_g = d \quad \text{(demand balance)}$$
$$0 \leq p_g \leq P_g^{max} \quad \forall g \quad \text{(capacity limits)}$$

## Using Linopy

[Linopy](https://linopy.readthedocs.io/) is a Python package for linear optimization:

```python
import linopy
import pandas as pd

# Create model
m = linopy.Model()

# Data
generators = ['coal', 'gas', 'wind']
costs = {'coal': 30, 'gas': 50, 'wind': 0}  # €/MWh
capacities = {'coal': 40, 'gas': 60, 'wind': 30}  # MW
demand = 80  # MW

# Variables
p = m.add_variables(lower=0, coords=[generators], name='p')

# Constraints
for g in generators:
    m.add_constraints(p.loc[g] <= capacities[g], name=f'cap_{g}')

m.add_constraints(p.sum() == demand, name='demand_balance')

# Objective
cost_expr = sum(costs[g] * p.loc[g] for g in generators)
m.add_objective(cost_expr)

# Solve
m.solve()

# Results
print("Generation (MW):")
print(m.solution['p'])
print(f"\nTotal cost: {m.objective.value:.2f} €")
```

## Mixed-Integer Programming

When discrete decisions are needed (e.g., unit commitment):

$$\min \sum_{g,t} (c_g \cdot p_{g,t} + SC_g \cdot u_{g,t})$$

where:
- $u_{g,t} \in \{0, 1\}$ is the commitment decision
- $SC_g$ is the start-up cost

```python
# Add binary variables
u = m.add_variables(binary=True, coords=[generators, snapshots], name='u')

# Linking constraints
m.add_constraints(p <= capacities * u, name='commitment')
```

## Duality and Prices

The dual variables give marginal prices:

$$\pi = \lambda_{demand}$$

where $\lambda$ is the dual variable of the demand constraint.

```python
# Get dual values (prices)
prices = m.dual['demand_balance']
print(f"Electricity price: {prices:.2f} €/MWh")
```

## Multi-Period Optimization

For time-series optimization:

```python
import numpy as np

# Time periods
T = 24
demand = 80 + 20 * np.sin(np.linspace(0, 2*np.pi, T))

m = linopy.Model()

# Variables indexed by time
p = m.add_variables(lower=0, coords=[generators, range(T)], name='p')

# Constraints for each time step
for t in range(T):
    m.add_constraints(p.loc[:, t].sum() == demand[t], name=f'demand_{t}')
    for g in generators:
        m.add_constraints(p.loc[g, t] <= capacities[g], name=f'cap_{g}_{t}')

# Objective
m.add_objective(sum(costs[g] * p.loc[g, :].sum() for g in generators))

m.solve()
```

## Storage Modeling

Storage adds temporal coupling:

$$E_{t} = E_{t-1} + \eta_c \cdot p_t^{charge} - \frac{p_t^{discharge}}{\eta_d}$$

```python
# Storage variables
charge = m.add_variables(lower=0, coords=[range(T)], name='charge')
discharge = m.add_variables(lower=0, coords=[range(T)], name='discharge')
soc = m.add_variables(lower=0, coords=[range(T)], name='soc')

# Storage capacity
storage_power = 20  # MW
storage_energy = 40  # MWh
efficiency = 0.9

# Constraints
for t in range(T):
    m.add_constraints(charge.loc[t] <= storage_power, name=f'charge_cap_{t}')
    m.add_constraints(discharge.loc[t] <= storage_power, name=f'discharge_cap_{t}')
    m.add_constraints(soc.loc[t] <= storage_energy, name=f'soc_cap_{t}')
    
    if t == 0:
        m.add_constraints(soc.loc[t] == 20, name='soc_initial')  # Initial SOC
    else:
        m.add_constraints(
            soc.loc[t] == soc.loc[t-1] + efficiency * charge.loc[t] - discharge.loc[t] / efficiency,
            name=f'soc_balance_{t}'
        )
```

## Solvers

Common solvers for energy optimization:

| Solver | License | LP | MILP |
|--------|---------|-----|------|
| HiGHS | Open-source | ✓ | ✓ |
| Gurobi | Commercial | ✓ | ✓ |
| CPLEX | Commercial | ✓ | ✓ |
| GLPK | Open-source | ✓ | ✓ |

```python
# Specify solver
m.solve(solver_name='highs')
```

## Key Takeaways

- Linear programming is fundamental to energy optimization
- Linopy provides a clean interface for building models
- Storage and unit commitment add complexity
- Dual variables give economic signals (prices)

:::{note}
For production use, consider using [PyPSA](https://pypsa.org/) which handles many modeling details automatically.
:::
