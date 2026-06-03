# Experiment 05 — Code Explanation
# Statistical Quality Control

---

## What is this program doing?

A factory produces 500 piston components per batch.
Every piston should have a diameter of exactly 80.00 mm.
But no manufacturing process is perfect — there's always
slight variation. This program:

1. Simulates 500 piston diameter measurements
2. Calculates how much variation exists (mean, std dev)
3. Detects outlier measurements (Z-score)
4. Tests if the machine is correctly calibrated (T-test)
5. Measures what percentage of parts are within tolerance

---

## Line by Line Explanation

---

### Lines 1-2 (Imports)
```python
import numpy as np
from scipy import stats
```
**NumPy:** For generating random data and statistics.

**SciPy:** Scientific Python — has advanced statistics functions.
`from scipy import stats` imports just the statistics module.
`stats.ttest_1samp()` performs the T-test.

---

### Lines 5-7 (Simulating Data)
```python
np.random.seed(0)
data = np.random.normal(loc=80.02, scale=0.05, size=500)
```
**What is np.random.seed(0)?**
Sets a fixed starting point for random number generation.
This ensures you get the SAME random numbers every time you run.
Without seed, results would be different each run.

**What is np.random.normal()?**
Generates numbers following a Normal (Bell curve) distribution.

Parameters:
- `loc=80.02` = mean of distribution (our machine is slightly off at 80.02mm, not 80.00mm)
- `scale=0.05` = standard deviation (variation of 0.05mm)
- `size=500` = generate 500 values

**Why normal distribution?**
Manufacturing variations almost always follow a normal distribution
due to many small random factors combining together (Central Limit Theorem).

---

### Lines 10-13 (Descriptive Statistics)
```python
mean = np.mean(data)
std_dev = np.std(data)
print(f"Mean Diameter: {mean:.4f} mm")
print(f"Standard Deviation: {std_dev:.4f} mm")
```
**np.mean():** Calculates average of all 500 values.
Formula: μ = (x1 + x2 + ... + xn) / n

**np.std():** Calculates standard deviation.
Formula: σ = √(Σ(xi - μ)² / n)

**What does standard deviation tell us?**
- Small σ → measurements are tightly clustered (consistent machine)
- Large σ → measurements are spread out (inconsistent machine)

**Expected result:** mean ≈ 80.02, std ≈ 0.05

---

### Lines 16-22 (Z-Score)
```python
X = 80.10
z_score = (X - mean) / std_dev
```
**What is Z-Score?**
Z-score measures how many standard deviations a value
is away from the mean.

**Formula:** Z = (X - μ) / σ

**Interpretation:**
- Z = 0 → exactly at the mean
- Z = 1 → 1 standard deviation above mean
- Z = -1 → 1 standard deviation below mean
- |Z| > 3 → outlier (less than 0.3% probability normally)

**Example calculation:**
Z = (80.10 - 80.02) / 0.05 = 0.08/0.05 = 1.6

This means 80.10mm is 1.6 standard deviations from mean.
Not an outlier (|Z| < 3).

**Why is this useful?**
Quickly identifies measurements that are suspiciously far
from normal — possible measurement errors or defective parts.

---

### Lines 25-27 (Hypothesis Testing)
```python
t_stat, p_value = stats.ttest_1samp(data, design_value)
```
**What is Hypothesis Testing?**
A statistical method to decide if an observation is real
or just due to random chance.

**What is the T-Test?**
Tests if the mean of our 500 measurements equals a target value.

**Null Hypothesis (H₀):** Machine mean = 80.00mm (machine is correctly calibrated)
**Alternative Hypothesis (H₁):** Machine mean ≠ 80.00mm (machine is off)

**What is `stats.ttest_1samp(data, design_value)`?**
- `data` = our 500 measurements
- `design_value` = 80.00 (what we want)
- Returns two values: t_stat and p_value

**What is t_stat?**
The T-statistic — measures how far the sample mean is
from the target in units of standard error.
Large |t| = bigger difference from target.

**What is p_value?**
The probability of getting this result IF the machine
were perfectly calibrated (H₀ were true).

---

### Lines 30-35 (Decision)
```python
if p_value < 0.05:
    print("Result: Process is NOT under control (reject H0)")
else:
    print("Result: Process IS under control (accept H0)")
```
**The 0.05 threshold:**
- p < 0.05 → Less than 5% chance this is random
  → The difference is REAL → Machine is off → Reject H₀
- p ≥ 0.05 → More than 5% chance this is random
  → Difference could be by chance → Machine is fine → Accept H₀

**In our simulation:**
Mean is 80.02 (not 80.00) → T-test will find this significant
→ p < 0.05 → "Process NOT under control"
This is correct — the machine IS slightly off!

---

### Lines 38-41 (Process Capability)
```python
tolerance = 0.1
upper_limit = design_value + tolerance
lower_limit = design_value - tolerance
within_tolerance = np.sum((data >= lower_limit) & (data <= upper_limit))
percentage = (within_tolerance / len(data)) * 100
```
**What is tolerance?**
The allowed range: 80.00 ± 0.10mm means parts between 79.90 and 80.10mm are acceptable.

**What is `(data >= lower_limit) & (data <= upper_limit)`?**
- `data >= lower_limit` → True/False array (is each value above lower limit?)
- `data <= upper_limit` → True/False array (is each value below upper limit?)
- `&` → AND operator: True only when BOTH conditions are True

**np.sum() on Boolean array:**
Counts how many True values (True=1, False=0).
Gives total parts within tolerance.

---

## Statistical Concepts Summary

| Concept | Formula | Meaning |
|---|---|---|
| Mean | μ = Σx/n | Average value |
| Std Dev | σ = √(Σ(x-μ)²/n) | Spread of data |
| Z-Score | Z = (X-μ)/σ | Distance from mean in σ units |
| T-Statistic | t = (x̄-μ₀)/(s/√n) | Distance from target in std error units |
| p-value | Probability | Chance of result if H₀ is true |

## Real World Application

This exact process is used in:
- **Six Sigma** quality control in manufacturing
- **Pharmaceutical** drug potency testing
- **Automotive** engine component inspection
- **Aerospace** critical dimension verification
