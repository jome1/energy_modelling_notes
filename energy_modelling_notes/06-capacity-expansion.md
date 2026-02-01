# Capacity Expansion Planning

*Author: [Jonas](intro.md#jonas)*

This chapter covers capacity expansion planning - determining optimal investments in energy infrastructure.

## The Capacity Expansion Problem

Unlike dispatch (short-term), capacity expansion determines **what to build**:

$$\min \sum_{g} (c_g^{cap} \cdot G_g + \sum_t c_g^{op} \cdot p_{g,t})$$

where:
- $G_g$ is the capacity to build for technology $g$
- $c_g^{cap}$ is the annualized capital cost
- $c_g^{op}$ is the operational (marginal) cost

## Annualized Costs

Capital costs are annualized using the capital recovery factor:

$$CRF = \frac{r(1+r)^n}{(1+r)^n - 1}$$

where:
- $r$ is the discount rate
- $n$ is the lifetime in years

```python
def annuity(r, n):
    """Calculate the annuity factor."""
    return r / (1 - (1 + r) ** (-n))

# Example: 7% discount rate, 25 year lifetime
crf = annuity(0.07, 25)
print(f"Capital Recovery Factor: {crf:.4f}")

# Overnight cost of 1000 €/kW becomes:
overnight_cost = 1000  # €/kW
annual_cost = overnight_cost * crf
print(f"Annualized cost: {annual_cost:.2f} €/kW/year")
```

## Technology Data

Typical technology assumptions for 2030:

| Technology | Capital Cost (€/kW) | Lifetime (years) | Marginal Cost (€/MWh) |
|------------|---------------------|------------------|----------------------|
| Onshore Wind | 1,200 | 25 | 0 |
| Solar PV | 400 | 25 | 0 |
| Gas CCGT | 800 | 30 | 50 |
| Battery (4h) | 300 | 15 | 0 |

## Basic Model with PyPSA

```python
import pypsa
import pandas as pd
import numpy as np

# Create network
n = pypsa.Network()

# Time resolution
hours = pd.date_range('2030-01-01', periods=8760, freq='h')
n.set_snapshots(hours)

# Add bus
n.add("Bus", "electricity")

# Load profile (normalized)
load_profile = 1 + 0.3 * np.sin(2 * np.pi * np.arange(8760) / 8760)
n.add("Load", "demand", 
      bus="electricity",
      p_set=50 * load_profile)  # 50 GW average

# Wind capacity factors
wind_cf = 0.3 + 0.2 * np.random.random(8760)

# Solar capacity factors  
hour_of_day = np.tile(np.arange(24), 365)
solar_cf = np.maximum(0, np.sin(np.pi * (hour_of_day - 6) / 12)) * (0.8 + 0.2 * np.random.random(8760))

# Add generators with expansion
n.add("Generator", "wind",
      bus="electricity",
      p_nom_extendable=True,
      capital_cost=1200 * annuity(0.07, 25) * 1000,  # €/MW/year
      marginal_cost=0,
      p_max_pu=wind_cf)

n.add("Generator", "solar",
      bus="electricity", 
      p_nom_extendable=True,
      capital_cost=400 * annuity(0.07, 25) * 1000,
      marginal_cost=0,
      p_max_pu=solar_cf)

n.add("Generator", "gas",
      bus="electricity",
      p_nom_extendable=True,
      capital_cost=800 * annuity(0.07, 30) * 1000,
      marginal_cost=50)

# Optimize
n.optimize()

# Results
print("\nOptimal Capacities (GW):")
print(n.generators.p_nom_opt / 1000)
print(f"\nTotal System Cost: {n.objective / 1e9:.2f} B€/year")
```

## Adding Storage

Storage is crucial for high renewable scenarios:

```python
n.add("StorageUnit", "battery",
      bus="electricity",
      p_nom_extendable=True,
      capital_cost=300 * annuity(0.07, 15) * 1000,
      marginal_cost=0,
      efficiency_store=0.95,
      efficiency_dispatch=0.95,
      max_hours=4)  # 4-hour battery
```

## Adding Constraints

### CO2 Limit

```python
# Add CO2 emissions
n.generators.loc['gas', 'carrier'] = 'gas'
n.add("Carrier", "gas", co2_emissions=0.2)  # t/MWh

# Add global constraint
n.add("GlobalConstraint", "co2_limit",
      type="primary_energy",
      carrier_attribute="co2_emissions",
      sense="<=",
      constant=10e6)  # 10 Mt CO2
```

### Renewable Targets

```python
# Minimum renewable share
n.add("GlobalConstraint", "renewable_target",
      type="tech_capacity_expansion",
      carrier_attribute="renewable",
      sense=">=",
      constant=0.8 * n.loads.p_set.sum())  # 80% renewable
```

## Analyzing Results

```python
import matplotlib.pyplot as plt

# Capacity mix
fig, ax = plt.subplots(figsize=(10, 5))
n.generators.p_nom_opt.plot.bar(ax=ax)
ax.set_ylabel('Optimal Capacity (MW)')
ax.set_title('Optimal Generation Mix')
plt.tight_layout()
plt.show()

# Generation time series
fig, ax = plt.subplots(figsize=(12, 5))
n.generators_t.p.plot.area(ax=ax)
ax.set_ylabel('Generation (MW)')
ax.set_title('Generation Dispatch')
plt.tight_layout()
plt.show()
```

## Sensitivity Analysis

Explore how results change with assumptions:

```python
results = []
for co2_price in [0, 50, 100, 150, 200]:
    n.generators.loc['gas', 'marginal_cost'] = 30 + co2_price * 0.2
    n.optimize()
    results.append({
        'co2_price': co2_price,
        'wind_cap': n.generators.loc['wind', 'p_nom_opt'],
        'solar_cap': n.generators.loc['solar', 'p_nom_opt'],
        'gas_cap': n.generators.loc['gas', 'p_nom_opt']
    })

sensitivity = pd.DataFrame(results)
sensitivity.plot(x='co2_price', figsize=(10, 5))
plt.xlabel('CO2 Price (€/t)')
plt.ylabel('Optimal Capacity (MW)')
plt.title('Capacity Sensitivity to CO2 Price')
plt.show()
```

## Key Takeaways

- Capacity expansion optimizes investment decisions
- Capital costs must be annualized for comparison
- Constraints (CO2, renewables) shape the optimal mix
- Storage enables higher renewable penetration
- Sensitivity analysis reveals key drivers

:::{note}
Real capacity expansion models include transmission, sector coupling, and detailed temporal/spatial resolution.
:::
