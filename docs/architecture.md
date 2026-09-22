# Architecture and engineering rationale

## 1. Boundary with the EDA simulator

The simulator is deliberately treated as an execution backend. The project does not reimplement RTL compilation or event scheduling. Its engineering value is the layer above the simulator: stimulus strategy, independent prediction, observation, checking, coverage feedback, mutation campaigns, and regression analytics.

## 2. Verification layers

### Layer A — Functional correctness

The reference model predicts the result from the transaction. The scoreboard compares the prediction with the RTL observation.

### Layer B — Temporal and protocol correctness

Assertions and monitors check rules that can be violated even when a final output happens to be correct. Examples include stability under backpressure, legal transaction acceptance, known-value requirements, and bounded progress.

### Layer C — Coverage

The framework measures operation coverage, operand classes, and operation × operand-class cross coverage. Coverage is not treated as a vanity percentage; uncovered scenarios are fed back to the generator.

### Layer D — Verification effectiveness

Seeded mutations are introduced into the DUT. The same regression is run against each mutant. A mutation score measures how many defects the environment can expose.

## 3. Closed-loop verification

```text
stimulus → simulation → checking → coverage
     ↑                         ↓
     └──── coverage gaps ──────┘

                 + fault campaign
                       ↓
              verification gaps
```

This is the differentiating idea of the project: verification is treated as an iterative optimization problem rather than a one-shot pass/fail simulation.

## 4. Why mutation analysis matters

A passing regression does not prove that the test suite is sensitive to realistic defects. If an intentionally modified DUT also passes, the framework has demonstrated a verification blind spot. Mutation campaigns expose those blind spots and provide a concrete way to improve stimulus or assertions.
