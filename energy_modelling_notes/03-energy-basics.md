# Energy System Fundamentals

This chapter covers the fundamental concepts of energy systems.

## Energy vs Power

Understanding the distinction between energy and power is essential:

- **Power** ($P$): Rate of energy transfer, measured in Watts (W)
- **Energy** ($E$): Total amount transferred over time, measured in Watt-hours (Wh)

$$E = P \times t$$

| Unit | Equivalent |
|------|------------|
| 1 kWh | 1,000 Wh |
| 1 MWh | 1,000 kWh |
| 1 GWh | 1,000 MWh |
| 1 TWh | 1,000 GWh |

## The Electricity Grid

The electricity grid connects generators to consumers:

```
Generation → Transmission → Distribution → Consumption
```

### Key Characteristics

1. **Supply must equal demand** at all times
2. **Frequency must be maintained** (50 Hz in Europe, 60 Hz in North America)
3. **Voltage levels vary** from high voltage transmission to low voltage distribution

## Generation Technologies

### Dispatchable Generation

Plants that can adjust output on demand:

- **Natural gas**: Fast ramping, moderate emissions
- **Coal**: Slower ramping, high emissions
- **Nuclear**: Baseload, near-zero emissions
- **Hydropower**: Fast ramping, zero emissions

### Variable Renewable Energy (VRE)

Output depends on weather conditions:

- **Solar PV**: Varies with sunlight
- **Wind**: Varies with wind speed
- **Run-of-river hydro**: Varies with water flow

## Capacity Factor

The capacity factor measures how much energy a plant produces relative to its maximum:

$$CF = \frac{E_{actual}}{P_{max} \times t}$$

Typical capacity factors:

| Technology | Capacity Factor |
|------------|-----------------|
| Nuclear | 85-95% |
| Coal | 50-70% |
| Gas CCGT | 40-60% |
| Onshore Wind | 25-35% |
| Solar PV | 10-25% |

## Load Duration Curve

A load duration curve shows demand sorted from highest to lowest:

```python
import numpy as np
import matplotlib.pyplot as plt

# Example demand data
hours = 8760
demand = np.random.normal(50, 10, hours)
sorted_demand = np.sort(demand)[::-1]

plt.figure(figsize=(10, 5))
plt.plot(sorted_demand)
plt.xlabel('Hours')
plt.ylabel('Demand (GW)')
plt.title('Load Duration Curve')
plt.grid(True)
plt.show()
```

## Merit Order

The merit order ranks generators by marginal cost:

1. Renewables (near-zero marginal cost)
2. Nuclear
3. Coal/Lignite
4. Natural Gas
5. Oil
6. Peakers

:::{note}
The merit order determines which plants operate at any given time, with cheapest sources dispatched first.
:::

## Summary

Key takeaways:

- Energy and power are related but distinct concepts
- The grid requires constant balance between supply and demand
- Different technologies have different characteristics
- The merit order determines dispatch decisions
