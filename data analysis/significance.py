import numpy as np
from scipy.stats import chi2_contingency, chisquare

# Placeholder counts (replace with your actual numbers)
# Gender counts: Female, Male, Gender-Neutral
counts_gender = [204, 64, 1]  # Total = 269

# Race counts: Asian, Black, Caucasian, Hispanic, Middle Eastern
counts_race = [118, 26, 33, 33, 59]  # Total = 269

# Intersectionality matrix: rows = [Female, Male, Gender-Neutral], columns = [Asian, Black, Caucasian, Hispanic, Middle Eastern]
intersection_matrix = np.array([
    [92, 20, 22, 28, 42],  # Female
    [25, 6, 11, 5, 17],     # Male
    [1, 0, 0, 0, 0]        # Gender-Neutral
])

# Chi-square tests
# Gender: Goodness-of-fit test against uniform distribution
gender_pvalue = 1.0
if sum(counts_gender) > 0:
    expected_gender = [sum(counts_gender) / 3] * 3
    _, gender_pvalue = chisquare(f_obs=counts_gender, f_exp=expected_gender)

# Race: Goodness-of-fit test against uniform distribution
race_pvalue = 1.0
if sum(counts_race) > 0:
    expected_race = [sum(counts_race) / 5] * 5
    _, race_pvalue = chisquare(f_obs=counts_race, f_exp=expected_race)

# Intersectionality: Chi-square test for independence
intersection_pvalue = 1.0
if intersection_matrix.sum() > 0:
    _, intersection_pvalue, _, _ = chi2_contingency(intersection_matrix)

# Output raw p-values
print("Gender Breakdown p-value:", gender_pvalue)
print("Race/Ethnicity Breakdown p-value:", race_pvalue)
print("Intersectionality p-value:", intersection_pvalue)