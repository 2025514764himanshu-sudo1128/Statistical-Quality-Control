# Experiment 05: Statistical Analysis for Quality Control

---

## Aim
To perform statistical analysis, hypothesis testing, and reliability assessment on manufactured component dimensions using Python.

---

## Concepts Covered
- Mean and Standard Deviation (descriptive statistics)
- Z-Score for outlier detection
- T-Test for hypothesis testing
- p-value interpretation
- Process capability analysis

---

## Formulas Used

| Formula | Description |
|---|---|
| μ = Σx / n | Mean |
| σ = √(Σ(x-μ)²/n) | Standard Deviation |
| Z = (X - μ) / σ | Z-Score |
| H₀: μ = design value | Null Hypothesis |
| p < 0.05 → Reject H₀ | Process out of control |

---

## Software Required

| Software | Purpose | Download Link |
|---|---|---|
| Python 3.x | Programming language | https://www.python.org/downloads/ |
| VS Code | Code editor | https://code.visualstudio.com/ |
| Git | Version control | https://git-scm.com/ |

---

## Installation Steps

### Step 1: Install Python
```
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or above
3. CHECK "Add Python to PATH"
4. Verify: python --version
```

### Step 2: Install Required Libraries
```bash
pip install numpy scipy
```

### Step 3: Verify Installation
```bash
python -c "import numpy; print('NumPy:', numpy.__version__)"
python -c "import scipy; print('SciPy:', scipy.__version__)"
```

---

## How to Run

```bash
git clone https://github.com/2025514764himanshu-sudo1128/Statistical-Quality-Control.git
cd Statistical-Quality-Control
python quality_control_statistics.py
```

---

## Expected Output
```
Mean Diameter: 80.0209 mm
Standard Deviation: 0.0500 mm

Z-Score for X=80.1mm: 1.58
This value is within normal range

T-Statistic: 9.3564
P-Value: 0.000000

Result: Process is NOT under control (reject H0)
Action: Machine calibration required!

Parts within tolerance (±0.1mm): 97.4%
```

---

## Author
**Himanshu Kumar** (2025514764)
Department of Electrical, Electronics and Communication Engineering
Sharda University, Greater Noida
