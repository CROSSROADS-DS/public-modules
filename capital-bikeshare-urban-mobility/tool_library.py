"""Student-facing tools for the CROSSROADS Capital Bikeshare module.

The public functions in this file support a question-driven investigation of
where and when bikeshare activity occurs. Routine data preparation, filtering,
summary calculations, mapping, plotting, and clustering are kept here so the
main activity notebook can focus on questions, evidence, interpretation, and
limitations.

Core dependencies: pandas, numpy, matplotlib
No live map service or scikit-learn installation is required.

Public functions
----------------
load_bikeshare_data       Load and validate the sampled trip data.
describe_bikeshare_data   Summarize dataset scope and quality.
find_stations             Find station names for later exploration.
plot_station_network      Map stations represented in the sample.
plot_station_activity     Map departures or arrivals, with time filters.
plot_trip_times           Examine temporal patterns for selected trips.
plot_station_times        Examine temporal patterns at selected stations.
cluster_stations_by_time  Optional count-based station clustering.
plot_trip_durations       Explore trip-duration distributions.
compare_trip_groups       Compare counts, percentages, or durations by group.
plot_trips_by_date        Explore daily variation.

All functions operate on findings from the sampled dataset. They do not imply
that the sample contains every Capital Bikeshare trip in the included months.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Configuration and validation
# ---------------------------------------------------------------------------

_REQUIRED_COLUMNS = {
    "ride_id",
    "rideable_type",
    "member_casual",
    "duration_minutes",
    "date",
    "month",
    "weekday",
    "is_weekend",
    "start_hour",
    "time_period",
    "start_station_name",
    "start_lat",
    "start_lng",
    "end_station_name",
    "end_lat",
    "end_lng",
}

_MONTH_ORDER = ["January", "April", "July", "October"]
_WEEKDAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
_TIME_PERIOD_ORDER = [
    "Overnight",
    "Morning commute",
    "Midday",
    "Evening commute",
    "Evening",
]
_BIKE_ORDER = ["classic_bike", "electric_bike"]
_RIDER_ORDER = ["member", "casual"]

_ORDERED_VALUES = {
    "month": _MONTH_ORDER,
    "weekday": _WEEKDAY_ORDER,
    "time_period": _TIME_PERIOD_ORDER,
    "rideable_type": _BIKE_ORDER,
    "member_casual": _RIDER_ORDER,
}

_LABELS = {
    "month": "Month",
    "weekday": "Day of week",
    "time_period": "Time period",
    "start_hour": "Trip start hour",
    "member_casual": "Rider type",
    "rideable_type": "Bike type",
    "is_weekend": "Day type",
}

_AREA_EXTENTS = {
    "central_dc": {
        "xmin": -77.075,
        "xmax": -76.985,
        "ymin": 38.870,
        "ymax": 38.930,
        "label": "Central Washington, DC",
    }
}

_DEFAULT_LANDMARK_FILE = "data/dc_landmarks.csv"


def _as_list(value):
    if value is None:
        return None
    if isinstance(value, str) or not isinstance(value, Iterable):
        return [value]
    return list(value)


def _prepare_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate and standardize a bikeshare DataFrame without changing input."""
    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame.")

    missing = sorted(_REQUIRED_COLUMNS - set(data.columns))
    if missing:
        raise ValueError(
            "The dataset is missing required columns: " + ", ".join(missing)
        )

    df = data.copy()
    for column in ["started_at", "ended_at", "date"]:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    numeric_columns = [
        "duration_minutes",
        "start_hour",
        "start_lat",
        "start_lng",
        "end_lat",
        "end_lng",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if df["is_weekend"].dtype == object:
        weekend_map = {
            "true": True,
            "false": False,
            "yes": True,
            "no": False,
            "1": True,
            "0": False,
        }
        converted = df["is_weekend"].astype(str).str.lower().map(weekend_map)
        df["is_weekend"] = converted.where(converted.notna(), df["is_weekend"])

    return df


def load_bikeshare_data(
    filename: str | Path = "2025_four_month_sampled_trips.csv",
) -> pd.DataFrame:
    """Load and validate the sampled Capital Bikeshare trip dataset.

    Parameters
    ----------
    filename:
        Path to the sampled trip CSV file.

    Returns
    -------
    pandas.DataFrame
        A validated copy with date, time, duration, hour, and coordinate fields
        converted to appropriate types.
    """
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(
            f"Could not find {path}. Place the CSV beside the notebook or "
            "provide the correct filename."
        )
    return _prepare_data(pd.read_csv(path))


def _normalize_day_type(day_type) -> Optional[bool]:
    if day_type is None:
        return None
    if isinstance(day_type, bool):
        return day_type
    value = str(day_type).strip().lower()
    if value in {"weekend", "weekends"}:
        return True
    if value in {"weekday", "weekdays"}:
        return False
    raise ValueError("day_type must be 'weekday', 'weekend', True, False, or None.")


def _normalize_hours(start_hour):
    if start_hour is None:
        return None
    if isinstance(start_hour, (int, np.integer)):
        hours = [int(start_hour)]
    else:
        values = list(start_hour)
        if len(values) == 2 and all(isinstance(v, (int, np.integer)) for v in values):
            low, high = int(values[0]), int(values[1])
            if low > high:
                raise ValueError("start_hour range must be ordered from low to high.")
            hours = list(range(low, high + 1))
        else:
            hours = [int(v) for v in values]
    if any(hour < 0 or hour > 23 for hour in hours):
        raise ValueError("start_hour values must be between 0 and 23.")
    return hours


def _filter_data(
    data: pd.DataFrame,
    *,
    month=None,
    day_type=None,
    start_hour=None,
    rider_type=None,
    bike_type=None,
    stations=None,
    station_role: str = "start",
) -> pd.DataFrame:
    """Apply the filters shared by all public functions."""
    df = _prepare_data(data)

    column_filters = {
        "month": month,
        "member_casual": rider_type,
        "rideable_type": bike_type,
    }
    for column, selected in column_filters.items():
        selected_values = _as_list(selected)
        if selected_values is not None:
            df = df[df[column].isin(selected_values)]

    weekend = _normalize_day_type(day_type)
    if weekend is not None:
        df = df[df["is_weekend"] == weekend]

    hours = _normalize_hours(start_hour)
    if hours is not None:
        df = df[df["start_hour"].isin(hours)]

    selected_stations = _as_list(stations)
    if selected_stations is not None:
        if station_role not in {"start", "end", "either"}:
            raise ValueError("station_role must be 'start', 'end', or 'either'.")
        start_match = df["start_station_name"].isin(selected_stations)
        end_match = df["end_station_name"].isin(selected_stations)
        if station_role == "start":
            df = df[start_match]
        elif station_role == "end":
            df = df[end_match]
        else:
            df = df[start_match | end_match]

    if df.empty:
        raise ValueError("No trips match the selected filters.")
    return df


def _filter_description(**filters) -> str:
    pieces = []
    labels = {
        "month": "month",
        "day_type": "day type",
        "start_hour": "start hour",
        "rider_type": "rider type",
        "bike_type": "bike type",
    }
    for key, value in filters.items():
        if value is None:
            continue
        if key == "start_hour" and not isinstance(value, (str, int, np.integer)):
            vals = list(value)
            if len(vals) == 2:
                value = f"{vals[0]}–{vals[1]}"
        if isinstance(value, (list, tuple, set)) and key != "start_hour":
            value = ", ".join(str(v) for v in value)
        pieces.append(f"{labels.get(key, key)}: {value}")
    return "; ".join(pieces) if pieces else "all trips"


def _ordered_index(series: pd.Series, column: str) -> pd.Series:
    if column == "start_hour":
        return series.reindex(range(24), fill_value=0)
    if column == "is_weekend":
        return series.reindex([False, True], fill_value=0).rename(
            index={False: "Weekday", True: "Weekend"}
        )
    order = _ORDERED_VALUES.get(column)
    return series.reindex(order, fill_value=0) if order else series


def _ordered_rows(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    if column == "start_hour":
        return frame.reindex(range(24), fill_value=0)
    if column == "is_weekend":
        return frame.reindex([False, True], fill_value=0).rename(
            index={False: "Weekday", True: "Weekend"}
        )
    order = _ORDERED_VALUES.get(column)
    return frame.reindex(order, fill_value=0) if order else frame


def _load_landmarks(landmark_file=None) -> pd.DataFrame:
    if landmark_file is False or landmark_file is None:
        if landmark_file is False:
            return pd.DataFrame()
        candidates = [
            Path(_DEFAULT_LANDMARK_FILE),
            Path(__file__).parent / _DEFAULT_LANDMARK_FILE,
            Path("dc_landmarks.csv"),
            Path(__file__).with_name("dc_landmarks.csv"),
        ]
        path = next((p for p in candidates if p.exists()), None)
        if path is None:
            return pd.DataFrame()
    else:
        path = Path(landmark_file)
        if not path.exists():
            raise FileNotFoundError(f"Could not find landmark file: {path}")

    landmarks = pd.read_csv(path)
    required = {"landmark", "latitude", "longitude"}
    missing = sorted(required - set(landmarks.columns))
    if missing:
        raise ValueError("The landmark file is missing: " + ", ".join(missing))
    landmarks["latitude"] = pd.to_numeric(landmarks["latitude"], errors="coerce")
    landmarks["longitude"] = pd.to_numeric(landmarks["longitude"], errors="coerce")
    return landmarks.dropna(subset=["latitude", "longitude"])


def _add_landmarks(ax, landmarks: pd.DataFrame, *, label=True):
    if landmarks.empty:
        return
    shown = landmarks.copy()
    if "show_by_default" in shown.columns:
        keep = shown["show_by_default"].astype(str).str.lower().isin(["true", "1", "yes"])
        shown = shown[keep]
    ax.scatter(
        shown["longitude"],
        shown["latitude"],
        marker="*",
        s=95,
        edgecolor="black",
        linewidth=0.6,
        label="Landmarks",
        zorder=5,
    )
    if label:
        for _, row in shown.iterrows():
            text = row.get("short_label", row["landmark"])
            dx = float(row.get("label_x_offset", 3))
            dy = float(row.get("label_y_offset", 3))
            ax.annotate(
                text,
                (row["longitude"], row["latitude"]),
                xytext=(dx, dy),
                textcoords="offset points",
                fontsize=8,
                weight="semibold",
                zorder=6,
            )


def _station_table(data: pd.DataFrame, trip_end: str = "start") -> pd.DataFrame:
    if trip_end not in {"start", "end"}:
        raise ValueError("trip_end must be 'start' or 'end'.")
    name = f"{trip_end}_station_name"
    lat = f"{trip_end}_lat"
    lng = f"{trip_end}_lng"
    metric = "departures" if trip_end == "start" else "arrivals"
    table = (
        data[[name, lat, lng]]
        .dropna()
        .groupby(name, as_index=False)
        .agg(
            latitude=(lat, "median"),
            longitude=(lng, "median"),
            trips=(name, "size"),
        )
        .rename(columns={name: "station", "trips": metric})
    )
    return table


def _area_subset(table: pd.DataFrame, area: str):
    if area == "all":
        return table.copy(), None
    if area not in _AREA_EXTENTS:
        raise ValueError("area must be 'all' or 'central_dc'.")
    extent = _AREA_EXTENTS[area]
    selected = table[
        table["longitude"].between(extent["xmin"], extent["xmax"])
        & table["latitude"].between(extent["ymin"], extent["ymax"])
    ].copy()
    if selected.empty:
        raise ValueError(f"No stations fall within area={area!r}.")
    return selected, extent


def _set_map_extent(ax, extent, table):
    if extent is not None:
        ax.set_xlim(extent["xmin"], extent["xmax"])
        ax.set_ylim(extent["ymin"], extent["ymax"])
    else:
        xpad = max((table["longitude"].max() - table["longitude"].min()) * 0.04, 0.005)
        ypad = max((table["latitude"].max() - table["latitude"].min()) * 0.04, 0.005)
        ax.set_xlim(table["longitude"].min() - xpad, table["longitude"].max() + xpad)
        ax.set_ylim(table["latitude"].min() - ypad, table["latitude"].max() + ypad)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(alpha=0.2)
    ax.set_aspect("equal", adjustable="datalim")


# ---------------------------------------------------------------------------
# Dataset understanding and station selection
# ---------------------------------------------------------------------------


def describe_bikeshare_data(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return dataset-scope and monthly-sample summaries.

    The monthly table is intentionally included so students can notice that
    January contains fewer sampled trips and avoid treating raw monthly totals
    as complete system-wide ridership.
    """
    df = _prepare_data(data)
    month_order = (
        df[["month", "month_number"]].drop_duplicates().sort_values("month_number")["month"].tolist()
        if "month_number" in df.columns
        else [m for m in _MONTH_ORDER if m in set(df["month"])]
    )
    scope = pd.DataFrame(
        {
            "Value": [
                len(df),
                df["date"].min().date() if df["date"].notna().any() else pd.NA,
                df["date"].max().date() if df["date"].notna().any() else pd.NA,
                ", ".join(month_order),
                df["start_station_name"].nunique(),
                df["end_station_name"].nunique(),
                int(df[["start_lat", "start_lng"]].isna().any(axis=1).sum()),
                int(df[["end_lat", "end_lng"]].isna().any(axis=1).sum()),
                int(df["ride_id"].duplicated().sum()),
            ]
        },
        index=[
            "Trips in sampled dataset",
            "First trip date",
            "Last trip date",
            "Sampled months",
            "Unique start stations",
            "Unique end stations",
            "Trips missing start coordinates",
            "Trips missing end coordinates",
            "Duplicate ride IDs",
        ],
    )
    monthly = (
        df.groupby("month", observed=False).size().rename("sampled_trips").to_frame()
    )
    monthly = monthly.reindex(month_order)
    return scope, monthly


def find_stations(
    data: pd.DataFrame,
    *,
    contains: Optional[str] = None,
    area: str = "all",
    minimum_trips: int = 1,
    trip_end: str = "start",
) -> pd.DataFrame:
    """Find station names and activity levels for independent exploration."""
    if not isinstance(minimum_trips, int) or minimum_trips < 1:
        raise ValueError("minimum_trips must be a positive integer.")
    table = _station_table(_prepare_data(data), trip_end=trip_end)
    table, _ = _area_subset(table, area)
    metric = "departures" if trip_end == "start" else "arrivals"
    table = table[table[metric] >= minimum_trips]
    if contains:
        table = table[table["station"].str.contains(contains, case=False, na=False)]
    return table.sort_values([metric, "station"], ascending=[False, True]).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Spatial investigation
# ---------------------------------------------------------------------------


def plot_station_network(
    data: pd.DataFrame,
    *,
    area: str = "all",
    trip_end: str = "start",
    show_landmarks: bool = True,
    landmark_file=None,
    title: Optional[str] = None,
    ax=None,
):
    """Map station locations represented in the sampled trip data.

    Marker size is constant because this function answers where stations exist,
    not how frequently they are used.
    """
    table = _station_table(_prepare_data(data), trip_end=trip_end)
    table, extent = _area_subset(table, area)

    if ax is None:
        _, ax = plt.subplots(figsize=(10.5, 7.2) if area == "central_dc" else (9, 8))
    ax.scatter(table["longitude"], table["latitude"], s=22 if area == "central_dc" else 13, alpha=0.65, label="Bikeshare stations")

    if show_landmarks and area == "central_dc":
        _add_landmarks(ax, _load_landmarks(landmark_file))

    area_label = _AREA_EXTENTS.get(area, {}).get("label", "the dataset")
    ax.set_title(title or f"Stations represented in {area_label}")
    _set_map_extent(ax, extent, table)
    ax.legend(loc="best")
    plt.tight_layout()
    return ax, table.sort_values("station").reset_index(drop=True)


def plot_station_activity(
    data: pd.DataFrame,
    *,
    area: str = "central_dc",
    trip_end: str = "start",
    month=None,
    day_type=None,
    start_hour=None,
    rider_type=None,
    bike_type=None,
    top_n: Optional[int] = None,
    show_landmarks: bool = True,
    landmark_file=None,
    title: Optional[str] = None,
    ax=None,
):
    """Map station departures or arrivals, optionally within a time context.

    This function supports the module's integrated spatial-temporal exploration.
    For example, students can compare weekday morning departures with weekend
    afternoon departures by changing ``day_type`` and ``start_hour``.

    ``start_hour=(7, 9)`` includes hours 7, 8, and 9.
    """
    df = _filter_data(
        data,
        month=month,
        day_type=day_type,
        start_hour=start_hour,
        rider_type=rider_type,
        bike_type=bike_type,
    )
    table = _station_table(df, trip_end=trip_end)
    table, extent = _area_subset(table, area)
    metric = "departures" if trip_end == "start" else "arrivals"

    if top_n is not None:
        if not isinstance(top_n, int) or top_n < 1:
            raise ValueError("top_n must be a positive integer or None.")
        table = table.nlargest(top_n, metric)

    max_value = table[metric].max()
    sizes = 22 + 320 * np.sqrt(table[metric] / max_value)

    if ax is None:
        _, ax = plt.subplots(figsize=(10.5, 7.2) if area == "central_dc" else (9, 8))
    ax.scatter(
        table["longitude"],
        table["latitude"],
        s=sizes,
        alpha=0.52,
        edgecolor="black",
        linewidth=0.35,
        label=f"Stations (size = {metric})",
    )
    if show_landmarks and area == "central_dc":
        _add_landmarks(ax, _load_landmarks(landmark_file))

    filters = _filter_description(
        month=month,
        day_type=day_type,
        start_hour=start_hour,
        rider_type=rider_type,
        bike_type=bike_type,
    )
    ax.set_title(title or f"Trip {metric}: {filters}")
    _set_map_extent(ax, extent, table)
    ax.legend(loc="best")
    plt.tight_layout()
    return ax, table.sort_values(metric, ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Temporal investigation
# ---------------------------------------------------------------------------


def plot_trip_times(
    data: pd.DataFrame,
    *,
    by: str = "start_hour",
    compare: Optional[str] = None,
    percent: bool = False,
    month=None,
    day_type=None,
    start_hour=None,
    rider_type=None,
    bike_type=None,
    stations=None,
    station_role: str = "start",
    title: Optional[str] = None,
    ax=None,
):
    """Plot when selected trips begin and return the plotted summary.

    Parameters
    ----------
    by:
        'start_hour', 'time_period', 'weekday', 'month', or 'is_weekend'.
    compare:
        None, 'is_weekend', 'rideable_type', or 'member_casual'.
    percent:
        If True, each comparison group's values sum to 100%. This is useful for
        comparing the shapes of weekday and weekend activity when group sizes
        differ.
    stations:
        Optional station name or list of names for spatial-temporal exploration.
    station_role:
        Match selected stations as trip starts, ends, or either.
    """
    allowed_by = {"start_hour", "time_period", "weekday", "month", "is_weekend"}
    allowed_compare = {None, "member_casual", "rideable_type", "is_weekend"}
    if by not in allowed_by:
        raise ValueError(f"by must be one of {sorted(allowed_by)}.")
    if compare not in allowed_compare:
        raise ValueError("compare must be None, 'member_casual', 'rideable_type', or 'is_weekend'.")
    if by == compare:
        raise ValueError("by and compare must use different columns.")

    df = _filter_data(
        data,
        month=month,
        day_type=day_type,
        start_hour=start_hour,
        rider_type=rider_type,
        bike_type=bike_type,
        stations=stations,
        station_role=station_role,
    )

    if compare is None:
        summary = df.groupby(by, observed=False).size()
        summary = _ordered_index(summary, by)
        if percent:
            summary = summary / summary.sum() * 100
    else:
        summary = df.groupby([by, compare], observed=False).size().unstack(compare, fill_value=0)
        summary = _ordered_rows(summary, by)
        order = [False, True] if compare == "is_weekend" else _ORDERED_VALUES.get(compare)
        if order:
            summary = summary.reindex(columns=order, fill_value=0)
        if percent:
            summary = summary.divide(summary.sum(axis=0).replace(0, pd.NA), axis=1) * 100
        if compare == "is_weekend":
            summary = summary.rename(columns={False: "Weekday", True: "Weekend"})

    if ax is None:
        _, ax = plt.subplots(figsize=(9.5, 4.8))
    kind = "line" if by == "start_hour" else "bar"
    summary.plot(kind=kind, marker="o" if kind == "line" else None, ax=ax)
    ax.set_xlabel(_LABELS.get(by, by.replace("_", " ").title()))
    ax.set_ylabel("Percent of trips" if percent else "Number of trips")
    ax.set_title(title or "When do trips begin?")
    if compare is None and ax.get_legend() is not None:
        ax.get_legend().remove()
    elif compare is not None:
        ax.legend(title=_LABELS.get(compare, compare.replace("_", " ").title()))
    if by in {"weekday", "month", "time_period"}:
        ax.tick_params(axis="x", rotation=30)
    if by == "start_hour":
        ax.set_xticks(range(0, 24, 2))
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    return ax, summary.round(2)


def plot_station_times(
    data: pd.DataFrame,
    stations,
    *,
    compare_stations: bool = True,
    percent: bool = True,
    day_type=None,
    month=None,
    bike_type=None,
    rider_type=None,
    station_role: str = "start",
    title: Optional[str] = None,
    ax=None,
):
    """Compare hourly activity at one or more selected stations.

    This is a convenience wrapper for independent spatial-temporal exploration.
    By default, each station's hourly profile sums to 100%, making shapes easier
    to compare even when stations have different total activity.
    """
    selected = _as_list(stations)
    if not selected:
        raise ValueError("Provide at least one station name.")

    df = _filter_data(
        data,
        month=month,
        day_type=day_type,
        rider_type=rider_type,
        bike_type=bike_type,
        stations=selected,
        station_role=station_role,
    )
    station_column = "start_station_name" if station_role == "start" else "end_station_name"
    if station_role == "either":
        raise ValueError("plot_station_times supports station_role='start' or 'end'.")

    compare = station_column if compare_stations and len(selected) > 1 else None
    if compare is None:
        summary = df.groupby("start_hour").size().reindex(range(24), fill_value=0)
        if percent:
            summary = summary / summary.sum() * 100
    else:
        summary = (
            df.groupby(["start_hour", station_column]).size().unstack(fill_value=0).reindex(range(24), fill_value=0)
        )
        summary = summary.reindex(columns=selected, fill_value=0)
        if percent:
            summary = summary.divide(summary.sum(axis=0).replace(0, pd.NA), axis=1) * 100

    if ax is None:
        _, ax = plt.subplots(figsize=(9.5, 4.8))
    summary.plot(ax=ax, marker="o")
    ax.set_xlabel("Trip start hour")
    ax.set_ylabel("Percent of station trips" if percent else "Number of trips")
    ax.set_title(title or "When are the selected stations used?")
    ax.set_xticks(range(0, 24, 2))
    ax.grid(axis="y", alpha=0.25)
    if compare is None and ax.get_legend() is not None:
        ax.get_legend().remove()
    else:
        ax.legend(title="Station")
    plt.tight_layout()
    return ax, summary.round(2)


# ---------------------------------------------------------------------------
# Optional guided clustering (count-based only)
# ---------------------------------------------------------------------------


def _kmeans_numpy(X: np.ndarray, k: int, *, seed: int = 42, n_init: int = 20, max_iter: int = 200):
    """Small NumPy implementation of k-means for JupyterLite compatibility."""
    if len(X) < k:
        raise ValueError("The number of stations must be larger than number_of_groups.")
    best = None
    base_rng = np.random.default_rng(seed)
    seeds = base_rng.integers(0, np.iinfo(np.int32).max, size=n_init)

    for init_seed in seeds:
        rng = np.random.default_rng(int(init_seed))
        centers = X[rng.choice(len(X), size=k, replace=False)].copy()
        labels = np.zeros(len(X), dtype=int)
        for _ in range(max_iter):
            distances = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
            new_labels = distances.argmin(axis=1)
            if np.array_equal(new_labels, labels) and _ > 0:
                break
            labels = new_labels
            new_centers = centers.copy()
            for cluster in range(k):
                members = X[labels == cluster]
                if len(members) == 0:
                    new_centers[cluster] = X[rng.integers(len(X))]
                else:
                    new_centers[cluster] = members.mean(axis=0)
            if np.allclose(new_centers, centers):
                centers = new_centers
                break
            centers = new_centers
        inertia = float(((X - centers[labels]) ** 2).sum())
        if best is None or inertia < best[0]:
            best = (inertia, labels.copy(), centers.copy())
    return best[1], best[2], best[0]


def cluster_stations_by_time(
    data: pd.DataFrame,
    *,
    area: str = "central_dc",
    number_of_groups: int = 3,
    minimum_trips: int = 40,
    show_landmarks: bool = True,
    landmark_file=None,
    random_state: int = 42,
):
    """Group stations using their 24 hourly sampled-departure counts.

    Color shows cluster membership. Marker size is proportional to the square
    root of total sampled departures, making the count-based grouping easier to
    interpret without allowing the busiest stations to overwhelm the map.

    Returns
    -------
    result : dict
        Keys include ``assignments``, ``cluster_profiles``, ``cluster_summary``,
        ``profile_ax``, ``map_ax``, and ``inertia``.
    """
    if not isinstance(number_of_groups, int) or number_of_groups < 2:
        raise ValueError("number_of_groups must be an integer of at least 2.")
    if not isinstance(minimum_trips, int) or minimum_trips < 1:
        raise ValueError("minimum_trips must be a positive integer.")

    df = _prepare_data(data).dropna(subset=["start_station_name", "start_lat", "start_lng", "start_hour"])
    df["start_hour"] = df["start_hour"].astype(int)

    counts = pd.crosstab(df["start_station_name"], df["start_hour"]).reindex(columns=range(24), fill_value=0)
    counts.index.name = "station"
    totals = counts.sum(axis=1).rename("total_trips")
    locations = (
        df.groupby("start_station_name", as_index=False)
        .agg(latitude=("start_lat", "median"), longitude=("start_lng", "median"))
        .rename(columns={"start_station_name": "station"})
    )
    eligible = locations.merge(totals.reset_index(), on="station")
    eligible, extent = _area_subset(eligible, area)
    eligible = eligible[eligible["total_trips"] >= minimum_trips].copy()
    if len(eligible) <= number_of_groups:
        raise ValueError(
            "Too few stations meet the selected area and minimum_trips settings. "
            "Lower minimum_trips or number_of_groups."
        )

    station_names = eligible["station"].tolist()
    X = counts.loc[station_names].to_numpy(dtype=float)
    labels, centers, inertia = _kmeans_numpy(X, number_of_groups, seed=random_state)

    # Order cluster labels by total activity so labels are easier to interpret.
    center_totals = centers.sum(axis=1)
    order = np.argsort(center_totals)
    remap = {old: new for new, old in enumerate(order)}
    labels = np.array([remap[label] for label in labels])
    centers = centers[order]

    assignments = eligible.copy()
    assignments["cluster"] = labels + 1
    assignments["cluster_label"] = assignments["cluster"].map(lambda x: f"Cluster {x}")

    cluster_profiles = pd.DataFrame(centers, columns=range(24))
    cluster_profiles.index = [f"Cluster {i}" for i in range(1, number_of_groups + 1)]
    cluster_profiles.index.name = "cluster"

    cluster_summary = (
        assignments.groupby("cluster_label")
        .agg(
            stations=("station", "size"),
            median_departures=("total_trips", "median"),
            minimum_departures=("total_trips", "min"),
            maximum_departures=("total_trips", "max"),
        )
        .round(1)
    )

    fig1, profile_ax = plt.subplots(figsize=(9.5, 4.8))
    for label, row in cluster_profiles.iterrows():
        profile_ax.plot(range(24), row.values, marker="o", label=label)
    profile_ax.set_title("Average hourly departures by station cluster")
    profile_ax.set_xlabel("Trip start hour")
    profile_ax.set_ylabel("Mean number of departures")
    profile_ax.set_xticks(range(0, 24, 2))
    profile_ax.legend()
    profile_ax.grid(axis="y", alpha=0.25)
    fig1.tight_layout()

    fig2, map_ax = plt.subplots(figsize=(10.5, 7.2) if area == "central_dc" else (9, 8))
    max_total = assignments["total_trips"].max()
    for cluster, part in assignments.groupby("cluster"):
        sizes = 24 + 300 * np.sqrt(part["total_trips"] / max_total)
        map_ax.scatter(
            part["longitude"],
            part["latitude"],
            s=sizes,
            alpha=0.58,
            edgecolor="black",
            linewidth=0.35,
            label=f"Cluster {cluster}",
        )
    if show_landmarks and area == "central_dc":
        _add_landmarks(map_ax, _load_landmarks(landmark_file))
    map_ax.set_title("Stations grouped by hourly departure counts")
    _set_map_extent(map_ax, extent, assignments)
    map_ax.legend(loc="best", title="Color = cluster\nSize = departures")
    fig2.tight_layout()

    return {
        "assignments": assignments.sort_values(["cluster", "total_trips"], ascending=[True, False]).reset_index(drop=True),
        "cluster_profiles": cluster_profiles.round(2),
        "cluster_summary": cluster_summary,
        "profile_ax": profile_ax,
        "map_ax": map_ax,
        "inertia": inertia,
    }


# ---------------------------------------------------------------------------
# Independent exploration tools
# ---------------------------------------------------------------------------


def plot_trip_durations(
    data: pd.DataFrame,
    *,
    compare: Optional[str] = None,
    max_minutes: Optional[float] = 40,
    bins: int = 20,
    month=None,
    day_type=None,
    start_hour=None,
    rider_type=None,
    bike_type=None,
    stations=None,
    station_role: str = "start",
    title: Optional[str] = None,
    ax=None,
):
    """Plot trip-duration distributions for selected trips."""
    allowed_compare = {None, "member_casual", "rideable_type", "month", "is_weekend"}
    if compare not in allowed_compare:
        raise ValueError("Unsupported compare value.")
    if not isinstance(bins, int) or bins < 1:
        raise ValueError("bins must be a positive integer.")
    if max_minutes is not None and max_minutes <= 0:
        raise ValueError("max_minutes must be positive or None.")

    df = _filter_data(
        data,
        month=month,
        day_type=day_type,
        start_hour=start_hour,
        rider_type=rider_type,
        bike_type=bike_type,
        stations=stations,
        station_role=station_role,
    )
    duration = df["duration_minutes"].dropna()
    if duration.empty:
        raise ValueError("No valid trip durations are available.")
    if ax is None:
        _, ax = plt.subplots(figsize=(8.5, 4.8))

    if compare is None:
        shown = duration if max_minutes is None else duration[duration <= max_minutes]
        ax.hist(shown, bins=bins, edgecolor="white")
        summary = pd.DataFrame(
            {
                "trips": [duration.size],
                "mean_minutes": [duration.mean()],
                "median_minutes": [duration.median()],
                "q1_minutes": [duration.quantile(0.25)],
                "q3_minutes": [duration.quantile(0.75)],
            },
            index=["All selected trips"],
        )
    else:
        work = df.copy()
        if compare == "is_weekend":
            work[compare] = work[compare].map({False: "Weekday", True: "Weekend"})
        order = _ORDERED_VALUES.get(compare)
        if compare == "is_weekend":
            order = ["Weekday", "Weekend"]
        if order is None:
            order = list(work[compare].dropna().unique())
        groups, labels = [], []
        for value in order:
            values = work.loc[work[compare] == value, "duration_minutes"].dropna()
            if not values.empty:
                groups.append(values)
                labels.append(str(value).replace("_", " ").title())
        ax.boxplot(groups, labels=labels, showfliers=False)
        summary = work.groupby(compare, observed=False)["duration_minutes"].agg(
            trips="count",
            mean_minutes="mean",
            median_minutes="median",
            q1_minutes=lambda x: x.quantile(0.25),
            q3_minutes=lambda x: x.quantile(0.75),
        )
        if max_minutes is not None:
            ax.set_ylim(0, max_minutes)
        ax.tick_params(axis="x", rotation=25)

    ax.set_xlabel("" if compare is None else _LABELS.get(compare, compare))
    ax.set_ylabel("Number of trips" if compare is None else "Trip duration (minutes)")
    ax.set_title(title or "How long are trips?")
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    return ax, summary.round(2)


def compare_trip_groups(
    data: pd.DataFrame,
    *,
    group: str = "rideable_type",
    measure: str = "trip_count",
    month=None,
    day_type=None,
    start_hour=None,
    rider_type=None,
    bike_type=None,
    stations=None,
    station_role: str = "start",
    title: Optional[str] = None,
    ax=None,
):
    """Compare selected trip groups using counts, percentages, or durations."""
    allowed_groups = {"member_casual", "rideable_type", "month", "weekday", "is_weekend", "time_period"}
    allowed_measures = {"trip_count", "trip_percent", "mean_duration", "median_duration"}
    if group not in allowed_groups:
        raise ValueError(f"group must be one of {sorted(allowed_groups)}.")
    if measure not in allowed_measures:
        raise ValueError(f"measure must be one of {sorted(allowed_measures)}.")

    df = _filter_data(
        data,
        month=month,
        day_type=day_type,
        start_hour=start_hour,
        rider_type=rider_type,
        bike_type=bike_type,
        stations=stations,
        station_role=station_role,
    )
    if measure in {"trip_count", "trip_percent"}:
        summary = df.groupby(group, observed=False).size().rename("value")
        if measure == "trip_percent":
            summary = summary / summary.sum() * 100
    else:
        statistic = "mean" if measure == "mean_duration" else "median"
        summary = df.groupby(group, observed=False)["duration_minutes"].agg(statistic).rename("value")
    summary = _ordered_index(summary, group)

    if ax is None:
        _, ax = plt.subplots(figsize=(8.5, 4.8))
    summary.plot(kind="bar", ax=ax)
    ylabels = {
        "trip_count": "Number of trips",
        "trip_percent": "Percent of trips",
        "mean_duration": "Mean duration (minutes)",
        "median_duration": "Median duration (minutes)",
    }
    ax.set_xlabel(_LABELS.get(group, group.replace("_", " ").title()))
    ax.set_ylabel(ylabels[measure])
    ax.set_title(title or "How do the groups compare?")
    ax.tick_params(axis="x", rotation=30)
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    return ax, summary.round(2).to_frame()


def plot_trips_by_date(
    data: pd.DataFrame,
    *,
    compare: Optional[str] = None,
    rolling_days: Optional[int] = None,
    month=None,
    day_type=None,
    rider_type=None,
    bike_type=None,
    stations=None,
    station_role: str = "start",
    title: Optional[str] = None,
    ax=None,
):
    """Plot daily sampled-trip counts, optionally with a moving average."""
    allowed_compare = {None, "member_casual", "rideable_type"}
    if compare not in allowed_compare:
        raise ValueError("compare must be None, 'member_casual', or 'rideable_type'.")
    if rolling_days is not None and (not isinstance(rolling_days, int) or rolling_days < 1):
        raise ValueError("rolling_days must be a positive integer or None.")

    df = _filter_data(
        data,
        month=month,
        day_type=day_type,
        rider_type=rider_type,
        bike_type=bike_type,
        stations=stations,
        station_role=station_role,
    ).dropna(subset=["date"])

    if compare is None:
        summary = df.groupby("date").size().rename("Trips").sort_index()
    else:
        summary = df.groupby(["date", compare], observed=False).size().unstack(compare, fill_value=0).sort_index()
        order = _ORDERED_VALUES.get(compare)
        if order:
            summary = summary.reindex(columns=order, fill_value=0)

    dates = []
    for _, part in df.groupby(df["date"].dt.to_period("M")):
        dates.extend(pd.date_range(part["date"].min(), part["date"].max(), freq="D"))
    summary = summary.reindex(pd.DatetimeIndex(dates), fill_value=0)
    summary.index.name = "date"
    plotted = summary if rolling_days is None else summary.rolling(rolling_days, min_periods=1).mean()

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 4.8))
    plotted.plot(ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel(f"{rolling_days}-day average trip count" if rolling_days else "Number of trips")
    ax.set_title(title or "How does trip activity vary by date?")
    if compare is None and ax.get_legend() is not None:
        ax.get_legend().remove()
    elif compare is not None:
        ax.legend(title=_LABELS.get(compare, compare.replace("_", " ").title()))
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    return ax, summary
