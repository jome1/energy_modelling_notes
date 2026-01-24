# Electricity Markets

This chapter introduces electricity market concepts and how they inform energy system models.

## Market Structure

Electricity markets typically have several components:

1. **Day-ahead market**: Trading for next-day delivery
2. **Intraday market**: Adjustments closer to real-time
3. **Balancing market**: Real-time adjustments
4. **Capacity market**: Payment for available capacity

## Price Formation

In a competitive market, price is set by the marginal generator:

$$\pi_t = c_{marginal,t}$$

where $\pi_t$ is the electricity price at time $t$ and $c_{marginal,t}$ is the cost of the most expensive operating generator.

### Merit Order Dispatch

```python
import pandas as pd
import matplotlib.pyplot as plt

# Example generators
generators = pd.DataFrame({
    'name': ['Solar', 'Wind', 'Nuclear', 'Gas CCGT', 'Gas OCGT'],
    'capacity': [20, 30, 15, 25, 10],  # GW
    'marginal_cost': [0, 0, 10, 50, 80]  # €/MWh
})

# Sort by marginal cost (merit order)
generators = generators.sort_values('marginal_cost')

# Plot supply curve
plt.figure(figsize=(10, 5))
cumulative = 0
for _, gen in generators.iterrows():
    plt.barh(gen['name'], gen['capacity'], left=cumulative, 
             label=f"{gen['name']}: {gen['marginal_cost']} €/MWh")
    cumulative += gen['capacity']

plt.xlabel('Cumulative Capacity (GW)')
plt.title('Merit Order Supply Curve')
plt.legend(loc='lower right')
plt.tight_layout()
plt.show()
```

## Market Clearing

The market clears where supply meets demand:

$$\sum_{g} p_{g,t} = d_t$$

This is solved as an optimization problem:

$$\min \sum_{t} \sum_{g} c_g \cdot p_{g,t}$$

subject to:
- Supply equals demand
- Generator limits: $0 \leq p_{g,t} \leq P_g^{max}$

## Locational Marginal Pricing (LMP)

When transmission constraints exist, prices can vary by location:

$$\pi_n = \frac{\partial \text{Cost}}{\partial d_n}$$

where $\pi_n$ is the price at node $n$.

## Renewable Integration Effects

### The Duck Curve

High solar penetration creates the "duck curve":

- Morning: Ramp up as solar comes online
- Midday: Low net demand (demand minus VRE)
- Evening: Steep ramp as solar drops and demand peaks

### Price Cannibalization

Renewables reduce prices during high production:

| Scenario | Avg. Price | Solar Revenue Factor |
|----------|------------|---------------------|
| Low Solar | 60 €/MWh | 1.1 |
| Medium Solar | 50 €/MWh | 0.9 |
| High Solar | 40 €/MWh | 0.7 |

## Market Modeling

A simple market clearing model:

```python
import pypsa

# Create network
n = pypsa.Network()
n.set_snapshots(range(24))

# Add bus
n.add("Bus", "electricity")

# Add generators
n.add("Generator", "solar", bus="electricity", 
      p_nom=50, marginal_cost=0, 
      p_max_pu=[0,0,0,0,0,0.2,0.5,0.8,0.9,1,1,1,0.9,0.8,0.5,0.2,0,0,0,0,0,0,0,0])

n.add("Generator", "gas", bus="electricity",
      p_nom=100, marginal_cost=50)

# Add load
n.add("Load", "demand", bus="electricity",
      p_set=[40]*24)

# Solve
n.optimize()

# Results
print(n.generators_t.p)
```

## Key Takeaways

- Electricity markets use merit order dispatch
- Price is set by the marginal generator
- Transmission constraints create locational pricing
- Renewables affect price dynamics significantly

:::{note}
Real electricity markets are more complex, with reserve requirements, ramping constraints, and start-up costs.
:::
