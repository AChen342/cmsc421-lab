"""Plot the experiment results saved by experiment.py.

Run from the repo root:  python -m p01_agents.plot_results
"""
import csv
import os
import random
from statistics import mean

import matplotlib.pyplot as plt

from .experiment import SEED, WALL_DENSITY, DIRT_DENSITY, MAP_SIZE

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
CSV_PATH = os.path.join(RESULTS_DIR, "experiment.csv")
PLOT_PATH = os.path.join(RESULTS_DIR, "agent_comparison.png")

AGENTS = ["reflex", "model", "goal"]
LABELS = {"reflex": "Reflex", "model": "Model-based", "goal": "Goal-based"}
# fixed color per agent (colorblind-safe blue / orange / aqua)
COLORS = {"reflex": "#2a78d6", "model": "#eb6834", "goal": "#1baf7a"}

SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT_MUTED = "#52514e"
GRID = "#e4e3df"

STEP_LIMIT = 4 * MAP_SIZE * MAP_SIZE
REWARD = 100   # points per dirt cell cleaned (see GridWorld.score)


def load_results(path=CSV_PATH):
    rows = {agent: [] for agent in AGENTS}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            cleaned, total = int(row["cleaned"]), int(row["total_dirt"])
            rows[row["agent"]].append({
                "score": int(row["score"]),
                "steps": int(row["steps"]),
                "cleaned_pct": 100 * cleaned / total,
                "total_dirt": total,
                "finished": row["hit_limit"] == "False",
                "explored": float(row["explored"]),
            })
    return rows


def strip_panel(ax, rows, metric, rng, unit=""):
    """One dot per map, jittered sideways, with a line and label at the mean."""
    for x, agent in enumerate(AGENTS):
        values = [r[metric] for r in rows[agent]]
        xs = [x + rng.uniform(-0.2, 0.2) for _ in values]
        ax.scatter(xs, values, s=20, color=COLORS[agent], alpha=0.5,
                   edgecolors=SURFACE, linewidths=0.6, zorder=3)

        avg = mean(values)
        ax.hlines(avg, x - 0.3, x + 0.3, color=TEXT, linewidth=2, zorder=4)
        ax.annotate(f"{avg:,.0f}{unit}", (x + 0.32, avg), va="center", fontsize=9.5,
                    color=TEXT, fontweight="bold")


def style_panel(ax, title, subtitle, tick_labels):
    # title = what is measured, subtitle (muted) = the takeaway
    ax.set_title(title, loc="left", fontsize=11.5, fontweight="bold", color=TEXT, pad=22)
    ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=9, color=TEXT_MUTED)
    ax.set_xticks(range(len(AGENTS)), tick_labels)
    ax.set_xlim(-0.6, len(AGENTS) - 0.25)
    ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
    ax.tick_params(colors=TEXT_MUTED, length=0, labelsize=9.5)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.set_facecolor(SURFACE)


def reference_line(ax, y, label):
    # solid hairline: a reference value, not a gridline
    ax.axhline(y, color=TEXT_MUTED, linewidth=0.9, zorder=2)
    ax.annotate(label, (-0.58, y), xytext=(0, 3), textcoords="offset points",
                fontsize=8, color=TEXT_MUTED)


def main():
    rows = load_results()
    rng = random.Random(0)  # fixed jitter so the image is the same every run
    n_maps = len(rows[AGENTS[0]])
    total_dirt = rows[AGENTS[0]][0]["total_dirt"]

    # x labels carry the agent name and how many maps it finished
    ticks = []
    for agent in AGENTS:
        done = sum(r["finished"] for r in rows[agent])
        ticks.append(f"{LABELS[agent]}\nfinished {done}/{n_maps}")

    fig, axes = plt.subplots(2, 2, figsize=(12, 9.5), facecolor=SURFACE)
    score_ax, steps_ax, clean_ax, explore_ax = axes.flatten()

    # 1. score
    strip_panel(score_ax, rows, "score", rng)
    best = total_dirt * REWARD
    reference_line(score_ax, best, f"{best:,} = every dirt cell, zero steps")
    score_ax.set_ylim(min(-300, score_ax.get_ylim()[0]), best * 1.08)
    style_panel(score_ax, "Score",
                "Model- and goal-based clean everything; their scores differ only by steps",
                ticks)

    # 2. steps (axis from 0, so "half the steps" looks like half)
    strip_panel(steps_ax, rows, "steps", rng)
    reference_line(steps_ax, STEP_LIMIT, f"step limit ({STEP_LIMIT})")
    steps_ax.set_ylim(0, STEP_LIMIT * 1.1)
    style_panel(steps_ax, "Steps taken",
                "Goal-based needs less than half the steps of model-based",
                ticks)

    # 3. dirt cleaned
    strip_panel(clean_ax, rows, "cleaned_pct", rng, unit="%")
    clean_ax.set_ylim(0, 108)
    clean_ax.set_yticks(range(0, 101, 20))
    style_panel(clean_ax, "Dirt cleaned (%)",
                "Reflex runs out of steps on every map, leaving dirt behind",
                ticks)

    # 4. exploration
    strip_panel(explore_ax, rows, "explored", rng, unit="%")
    explore_ax.set_ylim(0, 108)
    explore_ax.set_yticks(range(0, 101, 20))
    style_panel(explore_ax, "Open cells explored (%)",
                "Knowing the map lets goal-based skip a third of it",
                ticks)

    fig.suptitle(f"Three vacuum agents on {n_maps} random {MAP_SIZE}x{MAP_SIZE} maps",
                 x=0.012, ha="left", fontsize=15, fontweight="bold", color=TEXT)
    fig.text(0.012, 0.948,
             "Each dot is one map; the black line and label show the mean. "
             "Explored = share of the map's open cells the agent stood on at least once.",
             fontsize=9.5, color=TEXT_MUTED, va="top")
    fig.text(0.012, 0.012,
             f"Maps: seeds 0-{n_maps - 1}, {WALL_DENSITY:.0%} walls, {DIRT_DENSITY:.0%} dirt "
             f"({total_dirt} cells). Agent seed {SEED}. Step limit 4n² = {STEP_LIMIT}. "
             f"Score = {REWARD} x dirt cleaned - steps.",
             fontsize=8.5, color=TEXT_MUTED)
    fig.tight_layout(rect=(0, 0.025, 1, 0.93), h_pad=3.5, w_pad=3)

    fig.savefig(PLOT_PATH, dpi=150, facecolor=SURFACE)
    print(f"Saved plot to {PLOT_PATH}")


if __name__ == "__main__":
    main()
