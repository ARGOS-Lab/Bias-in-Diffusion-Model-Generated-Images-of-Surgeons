import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare
from itertools import combinations
import warnings

# Load the CSV data
data = pd.read_csv('data_final.csv')

# Clean the data
data['gender'] = data['gender'].str.strip().replace('', None)
data['race'] = data['race'].str.strip().replace('', None)

# Normalize race categories
def normalize_race(race):
    if pd.isna(race):
        return None
    race = race.lower()
    if 'caucasian' in race:
        return 'Caucasian'
    if 'south asian' in race or 'asian' in race or 'east asian' in race or 'northeast asian' in race:
        return 'Asian'
    if 'hispanic' in race:
        return 'Hispanic'
    if 'middle-eastern' in race or 'middle eastern' in race:
        return 'Middle Eastern'
    if 'black' in race:
        return 'Black'
    return race.capitalize()

# Convert p-value to asterisks
def convert_pvalue_to_asterisks(pvalue):
    if pvalue <= 0.0001:
        return "****"
    elif pvalue <= 0.001:
        return "***"
    elif pvalue <= 0.01:
        return "**"
    elif pvalue <= 0.05:
        return "*"
    return "ns"

# Process race and gender data
race_counts_prompt = {}
intersectionality = {}
total_race_instances = 0  # Count total race mentions (not normalized)
total_prompts = len(data)
maf_prompts = []  # Track "Male and Female" prompts
female_prompt_counts = []  # Track Female contributions

for index, row in data.iterrows():
    gender = row['gender']
    race_field = str(row['race']).strip()
    prompt_races = []
    female_increment = 0
    male_increment = 0
    race_contributions = {}
    seen_races = set()
    races_in_prompt = []

    if gender == 'Male and Female' and ':' in race_field:
        race_gender_pairs = [pair.strip() for pair in race_field.replace(' and ', ',').split(',') if pair.strip()]
        for pair in race_gender_pairs:
            if ':' in pair:
                try:
                    race, specific_gender = pair.split(':', 1)
                    race = race.strip()
                    specific_gender = specific_gender.strip()
                    normalized_race = normalize_race(race)
                    if specific_gender not in ['Male', 'Female']:
                        warnings.warn(f"Invalid gender '{specific_gender}' in race field '{pair}' at row {index}. Original race field: '{row['race']}'. Skipping.")
                        continue
                    if normalized_race and normalized_race not in seen_races:
                        race_contributions.setdefault(normalized_race, {'Male': 0, 'Female': 0, 'Gender-Neutral': 0})
                        race_contributions[normalized_race][specific_gender] += 1  # Full count
                        races_in_prompt.append(normalized_race)
                        prompt_races.append((normalized_race, specific_gender))
                        seen_races.add(normalized_race)
                    else:
                        warnings.warn(f"Invalid or duplicate race '{race}' in race field '{pair}' at row {index}. Original race field: '{row['race']}'. Skipping.")
                except Exception as e:
                    warnings.warn(f"Error parsing race:gender pair '{pair}' at row {index}: {e}. Original race field: '{row['race']}'. Skipping.")
            else:
                normalized_race = normalize_race(pair)
                if normalized_race and normalized_race not in seen_races:
                    race_contributions.setdefault(normalized_race, {'Male': 0, 'Female': 0, 'Gender-Neutral': 0})
                    race_contributions[normalized_race]['Male'] += 1  # Full count
                    race_contributions[normalized_race]['Female'] += 1  # Full count
                    races_in_prompt.append(normalized_race)
                    prompt_races.append((normalized_race, 'Both'))
                    seen_races.add(normalized_race)
                else:
                    warnings.warn(f"Invalid or duplicate race '{pair}' at row {index}. Original race field: '{row['race']}'. Skipping.")
    else:
        races = race_field.split(' and ') if ' and ' in race_field else [race_field]
        normalized_races = [normalize_race(race) for race in races if race and normalize_race(race)]
        for race in normalized_races:
            if race not in seen_races:
                race_contributions.setdefault(race, {'Male': 0, 'Female': 0, 'Gender-Neutral': 0})
                genders_to_add = ['Male', 'Female'] if gender == 'Male and Female' else [gender]
                for g in genders_to_add:
                    race_contributions[race][g] += 1  # Full count
                races_in_prompt.append(race)
                prompt_races.append((race, gender))
                seen_races.add(race)

    # Count race mentions without normalization
    for race in races_in_prompt:
        race_counts_prompt[race] = race_counts_prompt.get(race, 0) + 1  # Full count per race mention
        total_race_instances += 1  # Increment total race mentions
        for g in ['Male', 'Female', 'Gender-Neutral']:
            count = race_contributions.get(race, {}).get(g, 0)
            if count > 0:
                intersectionality[(g, race)] = intersectionality.get((g, race), 0) + count
                if g == 'Female':
                    female_increment += count
                if g == 'Male':
                    male_increment += count
    if gender == 'Male and Female':
        maf_prompts.append((index, race_field, prompt_races, female_increment, male_increment, len(races_in_prompt)))
    elif gender == 'Female':
        female_prompt_counts.append((index, race_field, female_increment, len(races_in_prompt)))

# Ensure all races and gender-race combinations are represented
all_races = set(race_counts_prompt.keys())
for race in all_races:
    for g in ['Female', 'Male', 'Gender-Neutral']:
        intersectionality.setdefault((g, race), 0)

# Gender and race counts
genders = ['Female', 'Male', 'Gender-Neutral']
counts_gender = [
    sum(intersectionality[('Female', race)] for race in all_races),
    sum(intersectionality[('Male', race)] for race in all_races),
    sum(intersectionality[('Gender-Neutral', race)] for race in all_races)
]
races = sorted(race_counts_prompt.keys())
counts_race = [race_counts_prompt[race] for race in races]

# Create intersectionality matrix
genders_heat = sorted(['Female', 'Male', 'Gender-Neutral'])
races_heat = sorted(races)
intersection_matrix = np.zeros((len(genders_heat), len(races_heat)))
for (g, r), count in intersectionality.items():
    if g in genders_heat:
        i, j = genders_heat.index(g), races_heat.index(r)
        intersection_matrix[i, j] = count

# Calculate heatmap percentages and adjust to sum to 100.0
percentage_matrix = (intersection_matrix / total_race_instances) * 100
sum_percentages_matrix = sum(percentage_matrix.flatten())
if sum_percentages_matrix != 100.0:
    max_idx = np.argmax(percentage_matrix)
    percentage_matrix.flat[max_idx] += 100.0 - sum_percentages_matrix
percentage_matrix = np.round(percentage_matrix, 1)

# Derive bar chart percentages from heatmap
percentages_gender = [sum(percentage_matrix[genders_heat.index(g), :]) for g in genders]
percentages_race = [sum(percentage_matrix[:, races_heat.index(r)]) for r in races]
# Adjust to ensure sums are exactly 100.0
sum_percentages_gender = sum(percentages_gender)
if sum_percentages_gender != 100.0:
    max_index = np.argmax(percentages_gender)
    percentages_gender[max_index] += 100.0 - sum_percentages_gender
percentages_gender = [round(p, 1) for p in percentages_gender]
sum_percentages_race = sum(percentages_race)
if sum_percentages_race != 100.0:
    max_index = np.argmax(percentages_race)
    percentages_race[max_index] += 100.0 - sum_percentages_race
percentages_race = [round(p, 1) for p in percentages_race]

# Calculate standard errors
se_gender = [round(np.sqrt((p/100) * (1 - p/100) / total_race_instances) * 100, 1) if count > 0 else 0 
             for p, count in zip(percentages_gender, counts_gender)]
se_race = [round(np.sqrt((p/100) * (1 - p/100) / total_race_instances) * 100, 1) if count > 0 else 0 
           for p, count in zip(percentages_race, counts_race)]

# Debugging: Verify counts and alignment
print("Total prompts:", total_prompts)
print("Total race instances:", total_race_instances)
print("Race counts (prompt-based):", {race: count for race, count in race_counts_prompt.items()})
print("Gender counts (bar chart):", {g: c for g, c in zip(genders, counts_gender)})
heatmap_sum = sum(count for (g, r), count in intersectionality.items())
print("Sum of heatmap counts:", heatmap_sum)
for g in ['Female', 'Male', 'Gender-Neutral']:
    gender_sum = sum(intersectionality[(g, r)] for r in all_races)
    print(f"Sum of counts for {g} in heatmap:", gender_sum)
for race in races:
    intersection_sum = sum(intersectionality[(g, race)] for g in ['Female', 'Male', 'Gender-Neutral'])
    print(f"Race {race}: race_counts_prompt = {race_counts_prompt[race]}, intersectionality sum = {intersection_sum}")
print("\n'Male and Female' prompts (index, race_field, races, female_increment, male_increment, num_races):")
for idx, rf, pr, fi, mi, nr in maf_prompts:
    print(f"Row {idx}: {rf} -> {pr}, Female increment = {fi}, Male increment = {mi}, Num races = {nr}")
print("\nFemale prompts (index, race_field, female_increment, num_races):")
for idx, rf, fi, nr in female_prompt_counts:
    print(f"Row {idx}: {rf} -> Female increment = {fi}, Num races = {nr}")
print("\nIntersectionality counts:")
for (g, r), count in intersectionality.items():
    print(f"({g}, {r}): {count}")

# Verify counts
female_counts_by_race = {race: intersectionality.get(('Female', race), 0) for race in races}
print("\nFemale counts by race in heatmap:")
for race, count in female_counts_by_race.items():
    print(f"  {race}: {count}")
female_heatmap_count = sum(female_counts_by_race.values())
female_bar_count = counts_gender[genders.index('Female')]
print(f"\nVerification: Female bar chart count = {female_bar_count}, Actual Female heatmap count = {female_heatmap_count}")

# Calculate significance asterisks for gender pairs
print("\nGender Pairwise Significance (Asterisks):")
n_genders = len(genders)
for i, j in combinations(range(n_genders), 2):
    x1, x2 = genders[i], genders[j]
    obs_pair = [counts_gender[i], counts_gender[j]]
    if min(obs_pair) > 0:
        exp_pair = [sum(obs_pair) / 2] * 2
        _, p_value = chisquare(f_obs=obs_pair, f_exp=exp_pair)
        p_value_adj = p_value * (n_genders * (n_genders-1) / 2)
        sig = convert_pvalue_to_asterisks(p_value_adj)
        print(f"{x1} vs {x2}: {sig}")
    else:
        print(f"{x1} vs {x2}: ns (one count is zero)")

# Calculate significance asterisks for race pairs
print("\nRace Pairwise Significance (Asterisks):")
n_races = len(races)
for i, j in combinations(range(n_races), 2):
    x1, x2 = races[i], races[j]
    obs_pair = [counts_race[i], counts_race[j]]
    if min(obs_pair) > 0:
        exp_pair = [sum(obs_pair) / 2] * 2
        _, p_value = chisquare(f_obs=obs_pair, f_exp=exp_pair)
        p_value_adj = p_value * (n_races * (n_races-1) / 2)
        sig = convert_pvalue_to_asterisks(p_value_adj)
        print(f"{x1} vs {x2}: {sig}")
    else:
        print(f"{x1} vs {x2}: ns (one count is zero)")

# Plot
plt.rcParams.update({'font.size': 14})
fig = plt.figure(figsize=(18, 12))

# a) Gender bar chart
ax1 = fig.add_subplot(2, 2, 1)
x_gender = np.arange(len(genders)) * 0.5
bars1 = ax1.bar(x_gender, counts_gender, color=['#1f77b4', '#ff7f0e', '#d62728'], width=0.15, label=genders)
ax1.set_title('a)')
ax1.set_ylabel('Count (n)')
ax1.set_ylim(0, max(counts_gender) * 1.3 + max(se_gender, default=0))
ax1.set_xticks(x_gender)
ax1.set_xticklabels(genders)
for i, bar in enumerate(bars1):
    height = bar.get_height()
    se = se_gender[i]
    if se > 0:
        ax1.errorbar(bar.get_x() + bar.get_width()/2., height, yerr=se, fmt='none', capsize=3, capthick=1, color='black', alpha=0.7)
    ax1.text(bar.get_x() + bar.get_width()/2., height + se, f'{counts_gender[i]:.0f} ({percentages_gender[i]:.1f}%)', 
             ha='center', va='bottom', fontsize=15)

# b) Race bar chart
ax2 = fig.add_subplot(2, 2, 2)
x_race = np.arange(len(races)) * 0.5
bars2 = ax2.bar(x_race, counts_race, color='skyblue', width=0.12, label=races)
ax2.set_title('b)')
ax2.set_ylabel('Count (n)')
ax2.set_ylim(0, max(counts_race) * 1.3 + max(se_race, default=0))
ax2.set_xticks(x_race)
ax2.set_xticklabels(races, rotation=45, ha='right')
for i, bar in enumerate(bars2):
    height = bar.get_height()
    se = se_race[i]
    if se > 0:
        ax2.errorbar(bar.get_x() + bar.get_width()/2., height, yerr=se, fmt='none', capsize=3, capthick=1, color='black', alpha=0.7)
    ax2.text(bar.get_x() + bar.get_width()/2., height + se, f'{counts_race[i]:.0f} ({percentages_race[i]:.1f}%)', 
             ha='center', va='bottom', fontsize=15)

# c) Heatmap
ax3 = fig.add_subplot(2, 1, 2)
im = ax3.imshow(intersection_matrix, cmap='YlOrRd', interpolation='nearest', vmin=0)
ax3.set_title('c)')
ax3.set_xticks(np.arange(len(races_heat)))
ax3.set_yticks(np.arange(len(genders_heat)))
ax3.set_xticklabels(races_heat, rotation=45, ha='right')
ax3.set_yticklabels(genders_heat)
plt.colorbar(im, ax=ax3, label='Count (n)')
for i in range(len(genders_heat)):
    for j in range(len(races_heat)):
        val = intersection_matrix[i, j]
        if val > 0:
            perc = percentage_matrix[i, j]
            text = f'{val:.0f} ({perc:.1f}%)'
            ax3.text(j, i, text, ha='center', va='center', fontsize=15, color='white',
                     bbox=dict(facecolor='black', edgecolor='none', boxstyle='round,pad=0.3'))

ax3.grid(False)
ax3.set_aspect('auto')

# Debugging: Compare heatmap sums with bar charts
print("\nHeatmap vs Bar Chart Comparison:")
for race in races_heat:
    heatmap_race_sum = sum(intersection_matrix[:, races_heat.index(race)])
    heatmap_race_pct = sum(percentage_matrix[:, races_heat.index(race)])
    bar_chart_pct = percentages_race[races.index(race)]
    print(f"Race {race}: Heatmap count = {heatmap_race_sum:.0f}, Heatmap % = {heatmap_race_pct:.1f}%, Bar chart % = {bar_chart_pct:.1f}%")
for g in genders_heat:
    heatmap_gender_sum = sum(intersection_matrix[genders_heat.index(g), :])
    heatmap_gender_pct = sum(percentage_matrix[genders_heat.index(g), :])
    bar_chart_count = counts_gender[genders.index(g)]
    bar_chart_pct = percentages_gender[genders.index(g)]
    print(f"Gender {g}: Heatmap count = {heatmap_gender_sum:.0f}, Heatmap % = {heatmap_gender_pct:.1f}%, Bar chart count = {bar_chart_count:.0f}, Bar chart % = {bar_chart_pct:.1f}%")
print("Sum of heatmap percentages:", round(sum(percentage_matrix.flatten()), 1))

plt.tight_layout()
plt.savefig('figure2.png')
plt.close()

print("Figure saved as: 'figure2.png'")