import numpy as np
from scipy import stats

# ============================================================
# ============================================================

class StatisticsError(ValueError):
    """Raised when statistical computation cannot proceed."""
    pass

class DataError(ValueError):
    """Raised when dataset is invalid or insufficient."""
    pass

# -------------------------------------------------------
# Input Helpers
# -------------------------------------------------------
def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("  Error: Enter a numeric value.")
            continue
        if value <= 0:
            print("  Error: Value must be greater than zero.")
            continue
        return value

def get_positive_int(prompt, minimum=2):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("  Error: Enter a whole number.")
            continue
        if value < minimum:
            print(f"  Error: Value must be at least {minimum}.")
            continue
        return value

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Error: Enter a numeric value.")

def get_float_in_range(prompt, low, high):
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("  Error: Enter a numeric value.")
            continue
        if not (low <= value <= high):
            print(f"  Error: Value must be between {low} and {high}.")
            continue
        return value

# -------------------------------------------------------
# Dataset Builders
# -------------------------------------------------------
def generate_simulated_data(mean, std_dev, size):
    """Generate normally distributed manufacturing measurements."""
    if std_dev <= 0:
        raise DataError("Standard deviation must be positive.")
    if size < 2:
        raise DataError("Need at least 2 samples.")
    np.random.seed(42)
    return np.random.normal(loc=mean, scale=std_dev, size=size)

def enter_manual_data():
    """Let user enter measurements one by one."""
    n = get_positive_int("  Number of measurements (min 2): ", minimum=2)
    data = []
    print(f"\n  Enter {n} measurements:")
    for i in range(n):
        val = get_float(f"    Measurement {i+1}: ")
        data.append(val)
    return np.array(data)

# -------------------------------------------------------
# Analysis
# -------------------------------------------------------
def compute_statistics(data):
    """Compute descriptive statistics safely."""
    if len(data) < 2:
        raise StatisticsError("Need at least 2 data points.")
    if np.all(data == data[0]):
        raise StatisticsError(
            "All values are identical — standard deviation is zero, "
            "Z-score and T-test cannot be computed."
        )
    mean   = float(np.mean(data))
    std    = float(np.std(data, ddof=1))   # Sample std dev (ddof=1)
    median = float(np.median(data))
    return mean, std, median

def compute_zscore(sample_value, mean, std):
    """Z = (X - mu) / sigma"""
    if std == 0:
        raise StatisticsError("Standard deviation is zero — Z-score undefined.")
    try:
        return (sample_value - mean) / std
    except ZeroDivisionError:
        raise StatisticsError("Division by zero in Z-score calculation.")

def compute_ttest(data, design_value):
    """One-sample T-test against design value."""
    if len(data) < 2:
        raise StatisticsError("T-test requires at least 2 data points.")
    try:
        t_stat, p_value = stats.ttest_1samp(data, design_value)
    except (ValueError, TypeError) as e:
        raise StatisticsError(f"T-test failed: {e}")
    return float(t_stat), float(p_value)

def perform_analysis(data, design_value, tolerance, sample_value):
    """Run full quality control analysis."""
    print(f"\n{'='*58}")
    print("  STATISTICAL QUALITY CONTROL RESULTS")
    print(f"{'='*58}")

    # --- Descriptive Statistics ---
    try:
        mean, std, median = compute_statistics(data)
    except StatisticsError as e:
        print(f"  Statistics Error: {e}")
        return

    print(f"\n  --- Descriptive Statistics ---")
    print(f"  Sample Size    : {len(data)}")
    print(f"  Mean           : {mean:.4f} mm")
    print(f"  Median         : {median:.4f} mm")
    print(f"  Std Deviation  : {std:.4f} mm")
    print(f"  Min            : {float(np.min(data)):.4f} mm")
    print(f"  Max            : {float(np.max(data)):.4f} mm")

    # --- Z-Score ---
    print(f"\n  --- Z-Score Analysis ---")
    try:
        z = compute_zscore(sample_value, mean, std)
        print(f"  Sample Value   : {sample_value:.4f} mm")
        print(f"  Z-Score        : {z:.2f}")
        if abs(z) > 3:
            print(f"  Classification : OUTLIER ⚠ (|Z| > 3)")
        elif abs(z) > 2:
            print(f"  Classification : WARNING (2 < |Z| ≤ 3)")
        else:
            print(f"  Classification : Normal range (|Z| ≤ 2)")
    except StatisticsError as e:
        print(f"  Z-Score Error  : {e}")

    # --- T-Test ---
    print(f"\n  --- Hypothesis Testing (T-Test) ---")
    print(f"  H0: Process mean = {design_value:.4f} mm")
    print(f"  H1: Process mean ≠ {design_value:.4f} mm")
    try:
        t_stat, p_value = compute_ttest(data, design_value)
        print(f"  T-Statistic    : {t_stat:.4f}")
        print(f"  P-Value        : {p_value:.6f}")
        if p_value < 0.05:
            print(f"  Decision       : REJECT H0 — Process NOT under control ✗")
            print(f"  Action         : Machine calibration required!")
        else:
            print(f"  Decision       : ACCEPT H0 — Process IS under control ✓")
            print(f"  Action         : Continue production.")
    except StatisticsError as e:
        print(f"  T-Test Error   : {e}")

    # --- Process Capability ---
    print(f"\n  --- Process Capability ---")
    if tolerance <= 0:
        print(f"  Error: Tolerance must be positive.")
    else:
        upper = design_value + tolerance
        lower = design_value - tolerance
        within = int(np.sum((data >= lower) & (data <= upper)))
        pct    = (within / len(data)) * 100
        print(f"  Tolerance      : ±{tolerance} mm")
        print(f"  Upper Limit    : {upper:.4f} mm")
        print(f"  Lower Limit    : {lower:.4f} mm")
        print(f"  Within Range   : {within}/{len(data)} ({pct:.1f}%)")
        if pct >= 99.73:
            grade = "Six Sigma ✓✓"
        elif pct >= 99.0:
            grade = "Excellent ✓"
        elif pct >= 95.0:
            grade = "Acceptable"
        else:
            grade = "Poor — needs improvement ✗"
        print(f"  Quality Grade  : {grade}")

    print(f"{'='*58}")

# -------------------------------------------------------
# Main Program
# -------------------------------------------------------
def main():
    print("=" * 58)
    print("   EXPERIMENT 05: Statistical Quality Control")
    print("   AI in Mechanical Engineering — ONT406")
    print("   Sharda University")
    print("=" * 58)

    while True:
        print("\n--- MENU ---")
        print("1. Generate Simulated Dataset")
        print("2. Enter Measurements Manually")
        print("3. Exit")

        choice = input("\nEnter your choice (1/2/3): ").strip()

        if choice == '1':
            print("\n--- Simulation Parameters ---")
            try:
                true_mean   = get_float(
                    "  True process mean (mm)           : ")
                std_dev     = get_positive_float(
                    "  Standard deviation (mm)          : ")
                size        = get_positive_int(
                    "  Number of samples (min 2)        : ", minimum=2)
                data        = generate_simulated_data(true_mean, std_dev, size)
                print(f"  ✓ {size} samples generated successfully.")

                design_val  = get_float(
                    "\n  Design/target value (mm)         : ")
                tolerance   = get_positive_float(
                    "  Tolerance ± (mm)                 : ")
                sample_val  = get_float(
                    "  Sample value to check (Z-score)  : ")
                perform_analysis(data, design_val, tolerance, sample_val)

            except DataError as e:
                print(f"  Data Error: {e}")

        elif choice == '2':
            try:
                data = enter_manual_data()
                if len(data) < 2:
                    raise DataError("Need at least 2 measurements.")

                design_val  = get_float(
                    "\n  Design/target value (mm)         : ")
                tolerance   = get_positive_float(
                    "  Tolerance ± (mm)                 : ")
                sample_val  = get_float(
                    "  Sample value to check (Z-score)  : ")
                perform_analysis(data, design_val, tolerance, sample_val)

            except DataError as e:
                print(f"  Data Error: {e}")

        elif choice == '3':
            print("\nExiting. Goodbye!")
            break

        else:
            print("  Error: Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Program interrupted by user. Goodbye!")
