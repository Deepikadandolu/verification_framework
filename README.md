# Project 3 — Coverage- and Mutation-Driven Automated RTL Verification Framework

## What this project is

A reusable verification infrastructure that sits **above** an RTL simulator. The simulator is treated as an execution engine; the framework decides what to test, predicts expected behavior independently, observes protocol/invariant behavior, measures coverage, injects controlled RTL faults, correlates failures, and feeds coverage gaps back into stimulus generation.

The included reference DUT is a 32-bit ALU because it is small enough to run anywhere while still exercising the complete infrastructure. The framework is deliberately written with adapter boundaries so the same flow can be connected to a processor, accelerator, FIFO, AXI-stream block, etc.

## Core loop

```text
Stimulus generation
      ↓
Independent reference model ─────┐
      ↓                          │
RTL simulator → monitor → trace  │
      ↓                          │
Assertions / protocol checks     │
      ↓                          │
Scoreboard ←─────────────────────┘
      ↓
Coverage analysis
      ↓
Coverage-directed stimulus update
      ↓
Regression + failure correlation
      ↓
Fault / mutation campaign
      ↓
Verification effectiveness report
```

## Why this is not an EDA compiler/simulator project

Icarus/Verilator/Questa/etc. compile and execute RTL. This project orchestrates verification around the simulator:

- independent reference modeling
- transaction generation and reproducible seeds
- directed + constrained-random stimulus
- monitors and scoreboarding
- cycle/transaction failure correlation
- assertion/protocol checking
- functional and cross coverage
- timeout/progress monitoring
- adaptive stimulus based on coverage gaps
- seeded RTL mutation/fault campaigns
- mutation score / fault-detection effectiveness
- machine-readable + human-readable regression reports

The framework intentionally **uses** the simulator rather than attempting to replace it.

## Repository

```text
project3_verification_framework/
├── rtl/
│   ├── alu.s                         # golden DUT
│   ├── alu_fault_stuck0.s            # seeded output fault
│   ├── alu_fault_stuck1.s            # seeded output fault
│   └── alu_fault_wrong_add.s         # seeded functional mutation
├── tb/
│   └── alu_tb.sv                     # monitor + protocol assertions + trace
├── src/
│   ├── config.py                     # configuration / schemas
│   ├── transaction.py                # transaction abstraction
│   ├── ref_model.py                  # independent behavioral model
│   ├── generator.py                   # directed + constrained-random generation
│   ├── coverage.py                    # functional + cross coverage
│   ├── analyzer.py                    # mismatch + first-divergence analysis
│   ├── regression.py                  # simulation orchestration
│   ├── mutation.py                    # fault campaign manager
│   ├── report.py                      # JSON + Markdown/terminal reports
│   └── runner.py                      # one-command end-to-end flow
├── tests/
│   └── test_python_layers.py          # framework self-tests
├── reports/                            # generated reports
├── Makefile
└── requirements.txt
```

## Requirements

- Python 3.9+
- Icarus Verilog (`iverilog`, `vvp`) OR another simulator can be substituted in `src/regression.py`

### Install Icarus

Ubuntu/Debian:
```bash
sudo apt-get install iverilog
```

macOS:
```bash
brew install icarus-verilog
```

## One-command execution

```bash
python3 -m src.runner --tests 500 --seed 18473
```

Run a single fault campaign:
```bash
python3 -m src.runner --tests 500 --fault-campaign
```

Use adaptive coverage-directed generation:
```bash
python3 -m src.runner --tests 1000 --adaptive
```

The generated artifacts include:

```text
reports/
├── regression_<id>.json
├── regression_<id>.md
├── coverage_<id>.json
├── failures_<id>.json
└── traces/
```

## What the framework actually checks

### Functional

Expected transaction results are computed by the Python reference model and compared with RTL observations.

### Temporal / protocol

The SystemVerilog monitor checks transaction stability while stalled, reset/valid behavior, and a bounded progress property. These are independent of the final numerical result.

### Coverage

The framework records operation coverage, operand classes, boundary classes, and selected cross coverage such as `operation × operand_class`.

### Failure analysis

The trace is searched for the **earliest divergence**, not merely the first test that failed. Failure records include seed, transaction ID, cycle, expected/actual values, and surrounding trace context.

### Fault effectiveness

The campaign runs the same regression against deliberately faulty RTL. It records which seeded faults are detected, by which mechanism, and calculates a mutation/fault-detection score.

### Coverage-directed loop

After an initial batch, uncovered operation/operand scenarios are converted into higher generator weights. A second batch is generated using those weights. This turns coverage from a passive report into feedback for stimulus generation.

## Interview-safe description

> Built a reusable coverage- and mutation-driven RTL verification framework that orchestrates directed/constrained-random stimulus, independent reference modeling, RTL simulation, protocol/assertion checks, differential scoreboarding, functional/cross coverage, failure correlation, adaptive stimulus generation, and seeded fault campaigns. The framework measures verification effectiveness through coverage closure and fault-detection/mutation scores rather than relying only on final output comparison.

## Important limitation

This is a student-scale verification infrastructure, not a replacement for UVM, Questa, VCS, Verilator, formal tools, or commercial coverage engines. Its engineering contribution is the **verification orchestration and feedback loop** around those execution tools.
