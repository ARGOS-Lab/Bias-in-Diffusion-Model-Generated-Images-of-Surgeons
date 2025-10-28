import csv
try:
    from rpy2.robjects import r, IntVector, FloatVector
    from rpy2.robjects.packages import importr
    rpy2_available = True
except ImportError:
    rpy2_available = False
    print("WARNING: rpy2 not installed. Install with: pip install rpy2")
    print("Also ensure R is installed on your system.\n")

# Data directly from the table - MANUALLY CALCULATED COUNTS
# Format: (category_name, count_2023, total_2023, count_2024, total_2024, count_2025, total_2025)

# Birth Sex totals: 469 + 591 + 39 = 1099 (2023), 503 + 653 = 1156 (2024), 491 + 652 = 1143 (2025)
# Race totals: 200 + 61 + 738 + 28 + 39 = 1066 (2023), 242 + 77 + 763 + 41 + 39 = 1162 (2024), 
#              246 + 72 + 748 + 49 + 31 = 1146 (2025)
# Ethnicity totals: 101 + 950 + 39 = 1090 (2023), 103 + 1040 + 25 = 1168 (2024), 108 + 1025 = 1133 (2025)

data = [
    # Birth Sex
    ("Birth Sex - Male", 469, 1060, 503, 1156, 491, 1143),
    ("Birth Sex - Female", 591, 1060, 653, 1156, 652, 1143),
    
    # Race
    ("Race - Asian", 200, 1066, 242, 1162, 246, 1146),
    ("Race - Black/African American", 61, 1066, 77, 1162, 72, 1146),
    ("Race - White", 738, 1066, 763, 1162, 748, 1146),
    ("Race - Other", 28, 1066, 41, 1162, 49, 1146),
    ("Race - Don't Know/Prefer not to Answer", 39, 1066, 39, 1162, 31, 1146),
    ("Non-white Race", 289, 1066, 360, 1162, 367, 1146),
    
    # Ethnicity
    ("Ethnicity - Hispanic/Latino Yes", 101, 1051, 103, 1168, 108, 1133),
    ("Ethnicity - Hispanic/Latino No", 950, 1051, 1040, 1168, 1025, 1133),
]

print("Chi-Square Test for Trends using R's prop.trend.test")
print("=" * 90)

results = [["Category", "2023_Count", "2023_Total", "2023_Prop", 
            "2024_Count", "2024_Total", "2024_Prop",
            "2025_Count", "2025_Total", "2025_Prop",
            "Chi_Square", "P_Value", "Significant"]]

if rpy2_available:
    for category, c23, t23, c24, t24, c25, t25 in data:
        # Calculate proportions
        p23 = c23 / t23 * 100
        p24 = c24 / t24 * 100
        p25 = c25 / t25 * 100
        
        # R's prop.trend.test requires:
        # - x: vector of counts of successes
        # - n: vector of total counts
        x = IntVector([c23, c24, c25])
        n = IntVector([t23, t24, t25])
        
        # Call R's prop.trend.test
        try:
            result = r['prop.trend.test'](x, n)
            
            # Extract results
            chi_square = result[0][0]  # Chi-square statistic
            p_value = result[2][0]     # p-value
            
            # Determine significance
            significant = "Yes" if p_value < 0.05 else "No"
            
            # Print results
            print(f"\n{category}:")
            print(f"  2023: {c23}/{t23} = {p23:.1f}%")
            print(f"  2024: {c24}/{t24} = {p24:.1f}%")
            print(f"  2025: {c25}/{t25} = {p25:.1f}%")
            print(f"  Chi-square = {chi_square:.4f}, p-value = {p_value:.4f} [{significant}]")
            
            # Add to results
            results.append([
                category,
                c23, t23, f"{p23:.1f}%",
                c24, t24, f"{p24:.1f}%",
                c25, t25, f"{p25:.1f}%",
                round(chi_square, 4),
                round(p_value, 4),
                significant
            ])
        except Exception as e:
            print(f"\n{category}: ERROR - {str(e)}")
            results.append([category, c23, t23, f"{p23:.1f}%", c24, t24, f"{p24:.1f}%",
                          c25, t25, f"{p25:.1f}%", "ERROR", "ERROR", "ERROR"])
else:
    print("\nCannot run tests - rpy2 not available")
    print("\nTo install rpy2:")
    print("1. Install R from https://www.r-project.org/")
    print("2. Run: pip install rpy2")

print("\n" + "=" * 90)
print("Note: p < 0.05 indicates a statistically significant trend")

# Save to CSV
csv_filename = "chi_square_trends_results_r.csv"
with open(csv_filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(results)

print(f"\nResults saved to {csv_filename}")