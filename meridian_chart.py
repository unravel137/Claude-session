import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.patches as mpatches
import numpy as np

df = pd.read_csv("meridian_financials_2022_2025.csv")

# Compute YoY ARR growth rate (vs same quarter prior year)
df["arr_growth_yoy"] = df["arr_usd_m"].pct_change(4) * 100

# Use full labels for annual quarters only (Q4 each year + Q1 2022 anchor)
labels = df["quarter"].tolist()
x = np.arange(len(labels))

fig, ax1 = plt.subplots(figsize=(13, 6))
fig.patch.set_facecolor("#F7F7F5")
ax1.set_facecolor("#F7F7F5")

# --- ARR growth rate bars (left axis) ---
colors = ["#B0C4DE" if g is None or np.isnan(g) else
          ("#2563EB" if g >= 20 else ("#60A5FA" if g >= 13 else "#93C5FD"))
          for g in df["arr_growth_yoy"]]

bars = ax1.bar(x, df["arr_growth_yoy"], color=colors, alpha=0.85, width=0.55, zorder=2)

ax1.set_ylabel("ARR Growth (YoY %)", fontsize=11, color="#1E3A5F", labelpad=10)
ax1.tick_params(axis="y", labelcolor="#1E3A5F")
ax1.set_ylim(0, 35)
ax1.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=45, ha="right", fontsize=8.5)
ax1.grid(axis="y", linestyle="--", alpha=0.4, zorder=1)
ax1.spines[["top", "right", "left", "bottom"]].set_visible(False)

# --- Operating margin line (right axis) ---
ax2 = ax1.twinx()
ax2.set_facecolor("#F7F7F5")
ax2.plot(x, df["operating_margin_pct"], color="#DC2626", linewidth=2.5,
         marker="o", markersize=4, zorder=3, label="Operating Margin")
ax2.set_ylabel("Operating Margin (%)", fontsize=11, color="#DC2626", labelpad=10)
ax2.tick_params(axis="y", labelcolor="#DC2626")
ax2.set_ylim(0, 20)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax2.spines[["top", "left", "bottom"]].set_visible(False)
ax2.spines["right"].set_color("#DC2626")

# --- Annotations: key milestones ---
milestones = {
    "2023Q1": ("AI plan\nwritten", -2),
    "2024Q3": ("FedRAMP\nMod.", -2),
    "2025Q1": ("Catherine\nstarts", -2),
    "2025Q3": ("Copilot\nGA + Helio", -2),
}
for q, (label, yoff) in milestones.items():
    idx = labels.index(q)
    yval = df.loc[df["quarter"] == q, "arr_growth_yoy"].values[0]
    ax1.annotate(
        label,
        xy=(idx, yval),
        xytext=(idx, yval + 4 + yoff),
        fontsize=7.5,
        color="#374151",
        ha="center",
        arrowprops=dict(arrowstyle="-", color="#9CA3AF", lw=0.8),
    )

# --- Title and legend ---
fig.suptitle(
    "Meridian Technologies: Growth Decelerating, Profitability Improving",
    fontsize=14, fontweight="bold", color="#111827", y=1.01
)
ax1.set_title(
    "ARR YoY growth rate (bars, left) vs. operating margin (line, right)  |  Q1 2022–Q4 2025",
    fontsize=9, color="#6B7280", pad=6
)

bar_patch = mpatches.Patch(color="#2563EB", alpha=0.85, label="ARR Growth ≥20%")
bar_patch2 = mpatches.Patch(color="#93C5FD", alpha=0.85, label="ARR Growth <13%")
line_patch = mpatches.Patch(color="#DC2626", label="Operating Margin")
ax1.legend(handles=[bar_patch, bar_patch2, line_patch],
           loc="upper right", fontsize=8.5, framealpha=0.0)

plt.tight_layout()
plt.savefig("meridian_growth_vs_margin.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("saved")
