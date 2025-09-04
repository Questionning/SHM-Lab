import matplotlib.pyplot as plt

# Values and their errors
values = [31.52, 30.7]
errors = [0.22, 0.709]
labels = ['Static method', 'Dynamic method']

# X positions for the points
x_pos = [1, 2]

lower_bounds = [v - e for v, e in zip(values, errors)]
upper_bounds = [v + e for v, e in zip(values, errors)]

overlap_lower = max(lower_bounds)
overlap_upper = min(upper_bounds)
overlap_size = max(0, overlap_upper - overlap_lower)

# Create figure
plt.figure(figsize=(6, 4))
plt.errorbar(x_pos, values, yerr=errors, fmt='o', capsize=5, markersize=8, color='blue', label='Value of k')

for x, val, err in zip(x_pos, values, errors):
    plt.fill_between([x-0.1, x+0.1], val-err, val+err, alpha=0.2, color='blue')

if overlap_size > 0:
    plt.fill_between([x_pos[0]-0.2, x_pos[1]+0.2], overlap_lower, overlap_upper, color='red', alpha=0.3, label='Overlap')
    plt.text(x=1.5, y=overlap_upper + 0.05, s=f'Overlap: {overlap_size:.3f}', color='red', ha='center')

plt.xticks(x_pos, labels)
plt.ylabel('Value of k (N/m)')
plt.title('Error Bar Comparison with Overlap Zone')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(min(lower_bounds) - 0.5, max(upper_bounds) + 0.5)
plt.legend()

plt.show()
