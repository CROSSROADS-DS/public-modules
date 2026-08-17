"""
tool_library.py
Helper functions for the FIFA player investigation module.

Students are not expected to read or modify this file. Each function is
designed to be called with a small number of readable settings so that
changing one setting produces a directly comparable result.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 50)


# ---------------------------------------------------------------------------
# Shared settings
# ---------------------------------------------------------------------------

AGE_GROUPS = ["23 and under", "24 to 28", "29 and over"]
AGE_BINS = [0, 23, 28, 200]

RATING_GROUPS = ["64 and under", "65 to 69", "70 to 74", "75 and over"]
RATING_BINS = [0, 64, 69, 74, 200]

# The 29 skill attributes recorded for every field player.
ATTRIBUTES = [
    "crossing", "finishing", "heading_accuracy", "short_passing", "volleys",
    "dribbling", "curve", "freekick_accuracy", "long_passing", "ball_control",
    "acceleration", "sprint_speed", "agility", "reactions", "balance",
    "shot_power", "jumping", "stamina", "strength", "long_shots",
    "aggression", "interceptions", "positioning", "vision", "penalties",
    "composure", "marking", "standing_tackle", "sliding_tackle",
]

# A shorter list used when a chart of all 29 attributes would be hard to read.
KEY_ATTRIBUTES = [
    "acceleration", "sprint_speed", "agility", "balance", "dribbling",
    "ball_control", "short_passing", "vision", "finishing", "positioning",
    "reactions", "composure", "stamina", "strength", "jumping",
    "heading_accuracy", "aggression", "interceptions", "marking",
    "standing_tackle", "freekick_accuracy",
]

_GROUP_COLORS = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]


# ---------------------------------------------------------------------------
# Loading and describing
# ---------------------------------------------------------------------------

def load_player_data(path):
    """Read the player file and prepare it for investigation.

    Preparation steps:
      * keeps only field players (goalkeepers are removed)
      * records each player's primary position
      * removes the `potential` column, which is a projection rather than
        a description of the player as they are now
      * adds an `age_group` and a `rating_group` label to every player
    """
    players = pd.read_csv(path)

    players["main_position"] = players["positions"].str.split(",").str[0].str.strip()
    players = players[players["main_position"] != "GK"].copy()

    players = players.drop(
        columns=[c for c in ["potential", "birth_date", "full_name", "player_id"]
                 if c in players.columns]
    )

    players["age_group"] = pd.cut(
        players["age"], bins=AGE_BINS, labels=AGE_GROUPS
    )
    players["rating_group"] = pd.cut(
        players["overall_rating"], bins=RATING_BINS, labels=RATING_GROUPS
    )

    front = ["name", "age", "age_group", "overall_rating", "rating_group",
             "main_position", "positions", "value_euro", "wage_euro"]
    ordered = front + [c for c in players.columns if c not in front]
    return players[ordered].reset_index(drop=True)


def describe_player_data(players):
    """Summarize the dataset's scope and show how many players fall in each group.

    Returns two tables: a scope summary and a table of player counts for every
    combination of age group and rating group.
    """
    scope = pd.DataFrame(
        {"Value": [
            f"{len(players):,}",
            f"{players['age'].min()} to {players['age'].max()}",
            f"{players['overall_rating'].min()} to {players['overall_rating'].max()}",
            f"{players['main_position'].nunique()}",
            f"{players['nationality'].nunique()}",
            f"{len(ATTRIBUTES)}",
            f"EUR {players['value_euro'].min():,.0f} to EUR {players['value_euro'].max():,.0f}",
            f"EUR {players['wage_euro'].min():,.0f} to EUR {players['wage_euro'].max():,.0f}",
            f"{int(players.isna().sum().sum())}",
        ]},
        index=[
            "Field players in the file",
            "Age range (years)",
            "Overall rating range",
            "Primary positions represented",
            "Nationalities represented",
            "Skill attributes recorded",
            "Value range",
            "Wage range",
            "Missing values in the whole file",
        ],
    )

    counts = pd.crosstab(players["rating_group"], players["age_group"])
    counts.index.name = "Rating group"
    counts.columns.name = "Age group"
    return scope, counts


# ---------------------------------------------------------------------------
# Distributions
# ---------------------------------------------------------------------------

def plot_distribution(players, by="overall_rating", title=None):
    """Show how many players fall at each value of one column.

    Settings
    --------
    by : "overall_rating", "age", or another whole-number column.
    """
    counts = players[by].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.bar(counts.index, counts.values, color="#4C72B0", width=0.85)
    ax.set_xlabel(by.replace("_", " ").title())
    ax.set_ylabel("Number of players")
    ax.set_title(title or f"Number of players by {by.replace('_', ' ')}")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

    ax.set_ylim(0, counts.max() * 1.14)

    mean_value = players[by].mean()
    ax.axvline(mean_value, color="#C44E52", linestyle="--", linewidth=1.5)
    ax.annotate(f"mean = {mean_value:.1f}",
                xy=(mean_value, counts.max() * 1.05),
                xytext=(6, 0), textcoords="offset points",
                color="#C44E52", fontsize=9)

    plt.tight_layout()

    summary = players[by].describe()[["count", "mean", "std", "min", "50%", "max"]]
    summary.index = ["players", "mean", "standard deviation", "minimum", "median", "maximum"]
    return ax, summary.round(1).to_frame(by)


# ---------------------------------------------------------------------------
# Comparing attribute profiles between groups
# ---------------------------------------------------------------------------

def compare_attributes(players, group_by="rating_group", within_rating=None,
                       within_age=None, attributes=None, title=None):
    """Compare the average skill attributes of two or more groups of players.

    Settings
    --------
    group_by      : "rating_group" or "age_group" -- which groups to compare.
    within_rating : optional rating-group label. Restricts the comparison to
                    players in that rating group only.
    within_age    : optional age-group label. Restricts the comparison to
                    players in that age group only.
    attributes    : optional list of attribute names. Defaults to KEY_ATTRIBUTES.

    The chart shows the difference between the highest and lowest group,
    sorted so the largest differences appear at the ends.
    """
    attributes = attributes or KEY_ATTRIBUTES
    subset = players

    label_bits = []
    if within_rating is not None:
        subset = subset[subset["rating_group"] == within_rating]
        label_bits.append(f"rating group {within_rating}")
    if within_age is not None:
        subset = subset[subset["age_group"] == within_age]
        label_bits.append(f"age group {within_age}")

    means = (subset.groupby(group_by, observed=True)[attributes]
             .mean().reindex(_labels_for(group_by)).dropna(how="all"))

    table = means.T
    first, last = table.columns[0], table.columns[-1]
    table["difference"] = table[last] - table[first]
    table = table.sort_values("difference")

    fig, ax = plt.subplots(figsize=(9, 8))
    colors = ["#C44E52" if v < 0 else "#4C72B0" for v in table["difference"]]
    ax.barh(table.index, table["difference"], color=colors)
    ax.axvline(0, color="black", linewidth=0.9)
    ax.set_xlabel(f"Difference in average rating points\n('{last}' minus '{first}')")

    default_title = f"Attribute differences by {group_by.replace('_', ' ')}"
    if label_bits:
        default_title += "\n(" + ", ".join(label_bits) + " only)"
    ax.set_title(title or default_title)
    ax.grid(axis="x", alpha=0.3)
    ax.set_axisbelow(True)

    n_note = "Group sizes -- " + ", ".join(
        f"{g}: {int((subset[group_by] == g).sum()):,}" for g in means.index
    )
    fig.text(0.5, -0.005, n_note, ha="center", fontsize=8.5, color="#444444")

    plt.tight_layout(rect=(0, 0.02, 1, 1))
    return ax, table.round(1)


# ---------------------------------------------------------------------------
# Age patterns
# ---------------------------------------------------------------------------

def plot_by_age(players, value="overall_rating", compare=None,
                minimum_players=25, title=None):
    """Show how the average of one column changes across single years of age.

    Settings
    --------
    value   : the column to average, for example "overall_rating".
    compare : set to "rating_group" to draw one line per rating group instead
              of a single line for everyone.
    """
    if compare is None:
        grouped = players.groupby("age")[value].agg(["size", "mean"])
        grouped = grouped[grouped["size"] >= minimum_players]
        table = grouped["mean"].to_frame(f"average {value}").round(1)

        fig, ax = plt.subplots(figsize=(11, 4.8))
        ax.plot(grouped.index, grouped["mean"], marker="o",
                color="#4C72B0", linewidth=2)
        ax.set_ylabel(f"Average {value.replace('_', ' ')}")
    else:
        rows = {}
        for label in _labels_for(compare):
            part = players[players[compare] == label]
            if part.empty:
                continue
            g = part.groupby("age")[value].agg(["size", "mean"])
            rows[label] = g["mean"][g["size"] >= minimum_players]
        table = pd.DataFrame(rows).round(1)

        fig, ax = plt.subplots(figsize=(11, 4.8))
        for i, label in enumerate(table.columns):
            ax.plot(table.index, table[label], marker="o", markersize=4,
                    linewidth=2, label=label,
                    color=_GROUP_COLORS[i % len(_GROUP_COLORS)])
        ax.legend(title=compare.replace("_", " "), fontsize=9)
        ax.set_ylabel(f"Average {value.replace('_', ' ')}")

    ax.set_xlabel("Age (years)")
    ax.set_title(title or f"Average {value.replace('_', ' ')} by age")
    ax.grid(alpha=0.3)
    ax.set_axisbelow(True)
    plt.tight_layout()
    return ax, table


# ---------------------------------------------------------------------------
# The age-by-rating grid
# ---------------------------------------------------------------------------

def summarize_grid(players, value="player_count", statistic="mean",
                   title=None, money=False):
    """Summarize one column for every combination of age group and rating group.

    Settings
    --------
    value     : "player_count", or any numeric column such as "overall_rating",
                "value_euro", "wage_euro", or a skill attribute.
    statistic : "mean" or "median". Ignored when value is "player_count".
    money     : set to True to format the table in euros.

    Rows are rating groups and columns are age groups, so reading across a row
    compares players of different ages who have similar overall ratings.
    """
    if value == "player_count":
        grid = pd.crosstab(players["rating_group"], players["age_group"])
        label = "Number of players"
        fmt = "{:,.0f}"
    else:
        grid = players.pivot_table(
            index="rating_group", columns="age_group",
            values=value, aggfunc=statistic, observed=True,
        )
        label = f"{statistic.title()} {value.replace('_', ' ')}"
        fmt = "EUR {:,.0f}" if money else "{:,.1f}"

    grid = grid.reindex(index=RATING_GROUPS, columns=AGE_GROUPS)
    grid.index.name = "Rating group"
    grid.columns.name = "Age group"

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    values = grid.astype(float).values

    # Colour is scaled within each row, because the comparison that matters is
    # reading ACROSS a row: players of different ages at a similar rating.
    # A single scale across the whole grid would be swamped by the differences
    # between rating groups and would hide the within-row pattern entirely.
    shades = np.full_like(values, np.nan, dtype=float)
    for r in range(values.shape[0]):
        row = values[r]
        lo, hi = np.nanmin(row), np.nanmax(row)
        shades[r] = 0.5 if hi == lo else (row - lo) / (hi - lo)

    ax.imshow(shades, cmap="Blues", vmin=-0.25, vmax=1.15, aspect="auto")

    ax.set_xticks(range(len(grid.columns)), grid.columns)
    ax.set_yticks(range(len(grid.index)), grid.index)
    ax.set_xlabel("Age group")
    ax.set_ylabel("Rating group")
    ax.set_title(title or f"{label} by age group and rating group")

    for r in range(values.shape[0]):
        for c in range(values.shape[1]):
            v = values[r, c]
            if np.isnan(v):
                continue
            ax.text(c, r, fmt.format(v), ha="center", va="center", fontsize=10,
                    color="white" if shades[r, c] > 0.72 else "black")

    fig.text(0.5, 0.005,
             "Shading compares values within each row (darker = larger).",
             ha="center", fontsize=8.5, color="#444444")
    plt.tight_layout(rect=(0, 0.03, 1, 1))

    display_grid = grid.round(0 if money or value == "player_count" else 1)
    return ax, display_grid


# ---------------------------------------------------------------------------
# Internal
# ---------------------------------------------------------------------------

def _labels_for(column):
    if column == "age_group":
        return AGE_GROUPS
    if column == "rating_group":
        return RATING_GROUPS
    raise ValueError("group_by must be 'age_group' or 'rating_group'")
