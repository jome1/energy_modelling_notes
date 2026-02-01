# Introduction to Energy System Modelling

*Author: [Jonas](intro.md#jonas)*

Energy system modelling is a critical tool for understanding and planning the transition to sustainable energy systems.

## What is Energy System Modelling?

Energy system models are mathematical representations of energy systems that help us:

- Understand how energy flows through the system
- Analyze the costs and benefits of different technologies
- Plan for future energy infrastructure investments
- Assess the impact of policy decisions

## Why is it Important?

The energy transition requires massive investments in new infrastructure. Models help decision-makers:

1. **Identify optimal pathways** to decarbonization
2. **Assess trade-offs** between different technologies
3. **Quantify uncertainties** in future scenarios
4. **Evaluate policies** before implementation

## Types of Energy System Models

### Optimization Models

These models find the least-cost way to meet energy demand subject to constraints:

$$\min \sum_{t} \sum_{g} c_g \cdot p_{g,t}$$

subject to:

$$\sum_{g} p_{g,t} = d_t \quad \forall t$$

Where:
- $c_g$ is the cost of generator $g$
- $p_{g,t}$ is the power output of generator $g$ at time $t$
- $d_t$ is the demand at time $t$

### Simulation Models

Simulation models track energy flows through a system over time, following predefined rules.

### Agent-Based Models

These models represent individual actors (consumers, producers) and their interactions.

## Key Components

Energy system models typically include:

| Component | Description |
|-----------|-------------|
| Generators | Power plants, renewable sources |
| Storage | Batteries, pumped hydro, hydrogen |
| Transmission | Power lines, pipelines |
| Demand | Electricity, heat, transport |

## Getting Started

In the following chapters, we'll explore:

1. Setting up your modelling environment
2. Understanding energy fundamentals
3. Building simple optimization models
4. Analyzing results and making decisions

:::{note}
These notes assume familiarity with Python. If you're new to Python, consider reviewing basic Python tutorials first.
:::
