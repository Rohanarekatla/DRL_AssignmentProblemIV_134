"""
chart_counts.py  -  DRL Assignment I, Problem IV, Group 134

Reproduces the summary analysis of Bouneffouf & Rish (2019),
"A Survey on Practical Applications of Multi-Armed and Contextual Bandits"
(arXiv:1904.10040). Table 1 (p.4) and Table 2 (p.6) are encoded cell-for-cell
from the paper, then we count how often each bandit setting is used and find
the empty cells the authors point to as open research directions.

Run:  python chart_counts.py      (needs matplotlib)
"""
import matplotlib.pyplot as plt

SETTINGS = ["MAB", "Non-stat. MAB", "CMAB", "Non-stat. CMAB"]

# 1 = setting used in that domain (a check mark in the paper's table)
TABLE_1 = {  # Bandits in real-life applications (paper p.4)
    "Healthcare":             [1, 0, 1, 0],
    "Finance":                [1, 0, 0, 0],
    "Dynamic pricing":        [0, 1, 0, 0],
    "Recommender system":     [1, 1, 1, 1],
    "Influence maximization": [1, 0, 0, 0],
    "Dialogue system":        [0, 0, 1, 0],
    "Telecommunication":      [1, 0, 0, 0],
    "Anomaly detection":      [1, 0, 0, 0],
}
TABLE_2 = {  # Bandits in machine learning (paper p.6)
    "Algorithm selection":    [0, 1, 0, 0],
    "Parameter optimization": [1, 0, 0, 0],
    "Feature selection":      [1, 1, 0, 0],
    "Active learning":        [1, 0, 1, 0],
    "Clustering":             [1, 0, 0, 0],
    "Reinforcement learning": [1, 1, 1, 0],
}


def column_counts(table):
    return [sum(row[i] for row in table.values()) for i in range(len(SETTINGS))]


def empty_cells(table):
    return {d: [SETTINGS[i] for i, v in enumerate(row) if v == 0]
            for d, row in table.items()}


t1, t2 = column_counts(TABLE_1), column_counts(TABLE_2)
total = [a + b for a, b in zip(t1, t2)]
n_cells = len(SETTINGS) * (len(TABLE_1) + len(TABLE_2))

print(f"{'Setting':<16}{'Table 1':>8}{'Table 2':>8}{'Total':>7}")
for s, a, b, c in zip(SETTINGS, t1, t2, total):
    print(f"{s:<16}{a:>8}{b:>8}{c:>7}")
print(f"\nCells filled: {sum(total)} of {n_cells} "
      f"({100 * sum(total) / n_cells:.0f}%)")
print("Domains using all four settings:",
      [d for d, r in {**TABLE_1, **TABLE_2}.items() if all(r)])
print("ML tasks with no contextual bandit:",
      [d for d, r in TABLE_2.items() if r[2] == 0 and r[3] == 0])

# ---- chart -----------------------------------------------------------------
NAVY, ORANGE = "#1B1F3B", "#FC8337"
fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=200)
y = range(len(SETTINGS))[::-1]
ax.barh(list(y), t1, color=NAVY, label="Table 1 - real-life applications")
ax.barh(list(y), t2, left=t1, color=ORANGE, label="Table 2 - machine learning")
for yi, tot in zip(y, total):
    ax.text(tot + 0.15, yi, str(tot), va="center", fontsize=11, color=NAVY,
            fontweight="bold")
ax.set_yticks(list(y))
ax.set_yticklabels(SETTINGS, fontsize=11, color=NAVY)
ax.set_xlabel("Number of domains / ML tasks using the setting", color=NAVY)
ax.set_xlim(0, max(total) + 1.5)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, fontsize=9, loc="lower right")
ax.set_title("Bandit settings used across the 14 surveyed areas",
             fontsize=12, color=NAVY, loc="left")
fig.tight_layout()
fig.savefig("bandit_setting_counts.png", transparent=True)
print("\nSaved bandit_setting_counts.png")
