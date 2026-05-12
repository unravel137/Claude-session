import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(11, 8))

# X: PM-centric (0) → Agentic (1)
# Y: Bundled/included (0) → Premium/add-on (1)

companies = {
    "Asana":           {"x": 0.62, "y": 0.18, "color": "#E8624A"},
    "Monday.com":      {"x": 0.42, "y": 0.08, "color": "#F04E8C"},
    "Atlassian":       {"x": 0.88, "y": 0.78, "color": "#0052CC"},
    "Smartsheet":      {"x": 0.18, "y": 0.52, "color": "#00A1E0"},
    "Meridian\n(Option A)": {"x": 0.28, "y": 0.68, "color": "#2D9B6F", "marker": "D", "size": 180},
    "Meridian\n(Option B)": {"x": 0.78, "y": 0.82, "color": "#1A5C3A", "marker": "D", "size": 180},
}

offsets = {
    "Asana":           ( 0.03, -0.07),
    "Monday.com":      (-0.04, -0.07),
    "Atlassian":       ( 0.03,  0.04),
    "Smartsheet":      (-0.22,  0.04),
    "Meridian\n(Option A)": (-0.24,  0.03),
    "Meridian\n(Option B)": ( 0.03,  0.03),
}

for name, props in companies.items():
    marker = props.get("marker", "o")
    size   = props.get("size", 160)
    ax.scatter(props["x"], props["y"], s=size, color=props["color"],
               marker=marker, zorder=5, edgecolors="white", linewidths=1.5)
    dx, dy = offsets[name]
    ax.text(props["x"] + dx, props["y"] + dy, name,
            fontsize=9.5, color=props["color"], fontweight="bold",
            ha="left", va="center", linespacing=1.4)

# Arrow connecting Meridian A → B
ax.annotate("", xy=(0.78, 0.82), xytext=(0.28, 0.68),
            arrowprops=dict(arrowstyle="->", color="#1A5C3A",
                            lw=1.6, linestyle="dashed"))

# Quadrant shading
ax.axvline(0.5, color="gray", linewidth=0.8, linestyle="--", alpha=0.5)
ax.axhline(0.5, color="gray", linewidth=0.8, linestyle="--", alpha=0.5)

quad_labels = [
    (0.25, 0.75, "Cautious\nPM incumbents"),
    (0.75, 0.75, "Agentic\npremium platforms"),
    (0.25, 0.25, "Bundled\nPM tools"),
    (0.75, 0.25, "Agentic\nbundlers"),
]
for qx, qy, ql in quad_labels:
    ax.text(qx, qy, ql, fontsize=8, color="gray", alpha=0.55,
            ha="center", va="center", style="italic")

# White space call-out
ws_x, ws_y = 0.78, 0.58
ax.annotate("White space:\nenterprise-grade\nagentic governance",
            xy=(ws_x, ws_y),
            xytext=(0.58, 0.38),
            fontsize=8, color="#1A5C3A", alpha=0.85,
            arrowprops=dict(arrowstyle="->", color="#1A5C3A", alpha=0.6, lw=1.2),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#1A5C3A", alpha=0.7))

# Axes labels and title
ax.set_xlabel("← PM-centric · · · · · · · · · · · · · · · · · · Agentic →",
              fontsize=10, labelpad=10, color="#333333")
ax.set_ylabel("← Bundled / included · · · · · · · · · Premium / add-on →",
              fontsize=10, labelpad=10, color="#333333")
ax.set_title("Competitive Positioning Matrix\nAI Strategy × Pricing Posture  |  Feb 2026",
             fontsize=13, fontweight="bold", pad=14)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_edgecolor("#cccccc")

legend_elements = [
    mpatches.Patch(color="#E8624A", label="Asana"),
    mpatches.Patch(color="#F04E8C", label="Monday.com"),
    mpatches.Patch(color="#0052CC", label="Atlassian"),
    mpatches.Patch(color="#00A1E0", label="Smartsheet"),
    plt.scatter([], [], marker="D", color="#2D9B6F", s=80, label="Meridian Option A"),
    plt.scatter([], [], marker="D", color="#1A5C3A", s=80, label="Meridian Option B"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=8.5,
          framealpha=0.9, edgecolor="#cccccc")

plt.tight_layout()
plt.savefig("positioning_matrix.png", dpi=150, bbox_inches="tight")
print("Saved positioning_matrix.png")
