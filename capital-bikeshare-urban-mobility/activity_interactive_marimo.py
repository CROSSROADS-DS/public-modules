# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.16",
#     "matplotlib==3.11.1",
#     "pandas==3.0.5",
#     "polars==1.43.2",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Capital Bikeshare: Investigating Service Across Space and Time

    ## Your role and mission

    Imagine that **Capital Bikeshare has asked your team to examine 2025 trip data**.

    Your goal is to help Capital Bikeshare better understand how its service is currently being used. The insights you develop could help the organization review its service and consider how it might better serve the community.

    The data include information about where and when trips began and ended, rider and bike types, and trip duration.

    Begin by developing **one or more questions** that could help Capital Bikeshare learn something useful about its current service. As you learn more, you may refine, narrow, replace, or add questions.

    > **Your questions:** What would you like to investigate to help Capital Bikeshare understand its current service and better serve the community? Briefly explain why each question could be useful.

    You might consider space and location, time, rider type, bike type, trip duration, or relationships among these attributes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    # Where the data come from

    Capital Bikeshare publishes monthly trip-history files for public analysis. These files contain trip timing, start and end stations, bike type, and rider category. The source files are much larger than needed for a short classroom investigation.

    For this module, we prepared a smaller dataset from four months in 2025: **January, April, July, and October**. Records unsuitable for the planned analyses were excluded, and a manageable subset of eligible trips was retained: 2,500 trips from January and 6,000 from each of the other three months. The resulting file contains 20,500 trips.

    This smaller dataset makes the notebook faster and easier to use in JupyterLite while preserving useful spatial and temporal patterns. Because the months contain different numbers of selected records, raw monthly totals should not be treated as complete monthly ridership.

    We also compared important characteristics of the smaller dataset with the eligible records and original source data to check that it remained suitable for learning. The figure below shows one example: January trip-duration distributions are broadly similar across the original, eligible, and classroom datasets. The purpose here is simply to show that validation was part of the preparation process; the technical details are not needed for this activity.

    ![January trip-duration comparison](images/january_duration_boxplot.png)

    **Data source:** [Capital Bikeshare System Data](https://capitalbikeshare.com/system-data)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why we use a landmark dataset

    A map of station coordinates can be difficult to interpret without familiar geographic reference points. We therefore created a small companion dataset containing selected Washington, DC landmarks, such as Union Station, the U.S. Capitol, the White House, and major memorials and museums.

    The landmark names and coordinates were compiled from official public sources and stored in `data/dc_landmarks.csv`. The helper functions add these landmarks to central-Washington maps so students can orient themselves without relying on a live online map service. The landmark data provide context only; they are not used to calculate trip activity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Load the trip data
    """)
    return


@app.cell
def _(mo):
    import tool_library as tl
    import urllib.request
    from pathlib import Path

    path_to_csv = mo.notebook_location() / "data" / "2025_four_month_sampled_trips.csv"
    path_str = str(path_to_csv)

    if path_str.startswith(("http://", "https://")):
        with urllib.request.urlopen(path_str) as response:
            csv_bytes = response.read()

        wasm_disk_path = Path("/tmp/local_sampled_trips.csv")
        wasm_disk_path.parent.mkdir(parents=True, exist_ok=True)

        with open(wasm_disk_path, "wb") as f:
            f.write(csv_bytes)

        trips = tl.load_bikeshare_data(wasm_disk_path)
    else:
        trips = tl.load_bikeshare_data(path_to_csv)
    trips.head()
    return tl, trips


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examine the output

    The displayed rows provide a first look at the data. Each row represents one trip. Notice the timing, rider and bike categories, duration, and station information.

    > **Question:** What information in these rows seems most relevant to the questions you developed? Cite specific columns as evidence.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Evaluate what the dataset can support
    """)
    return


@app.cell
def _(mo, tl, trips):
    scope_summary, monthly_sample = tl.describe_bikeshare_data(trips)

    mo.vstack([scope_summary, monthly_sample])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examine the output

    Use the first table to examine coverage and completeness. Use the second table to confirm how many records are included from each month.

    > **Question:** Which of your questions can this dataset help answer, and what additional information would Capital Bikeshare need for the questions it cannot answer? Support your response with evidence from the tables and available columns.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Refine your questions

    Good investigations often begin with interesting questions and then adjust those questions to match the available evidence.

    > **Question:** How would you keep, revise, replace, or add to your questions so they are useful to Capital Bikeshare and answerable with these data?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A shared investigation path

    Capital Bikeshare could investigate many aspects of its service. To practice a complete evidence-based investigation, we will now follow **one selected path together**.

    Our shared question is:

    > **What do the locations and timing of trips suggest about how Capital Bikeshare is currently serving Washington, DC?**

    This is not the only useful investigation. The shared path gives us practice using helper functions, examining evidence, and interpreting results cautiously. Afterward, you will return to your own questions and use the same tools for further exploration.

    We begin with geography. Before asking when people use the service, we first need to understand where the represented network extends and where stations are available.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. What does the station network reveal about the geographic reach of the service?
    """)
    return


@app.cell
def _(mo, tl, trips):
    network_ax, all_stations = tl.plot_station_network(
        trips,
        area="all",
        show_landmarks=False,
    )

    stations_ouput = f"Stations represented as trip origins: {len(all_stations):,}"
    mo.vstack([stations_ouput, all_stations, network_ax])

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examine the output

    Look at the overall spread of points, where stations appear especially dense, and what is difficult to distinguish at this scale.

    > **Question:** What observations and service-related insights can you draw about the network's geographic reach? Cite visible map evidence.

    ### Transition

    Because the central area is crowded on the regional map, we now narrow the view to examine station availability more clearly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. What does the station distribution reveal about availability across central Washington?
    """)
    return


@app.cell
def _(mo, tl, trips):
    central_ax, central_stations = tl.plot_station_network(
        trips,
        area="central_dc",
        show_landmarks=True,
    )

    central_stations_output = f"Central-Washington stations represented as trip origins: {len(central_stations):,}"
    mo.vstack([central_stations_output, central_stations, central_ax])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examine the output

    Use the landmarks for orientation. Look for broad coverage, concentrations, and gaps within the displayed area.

    > **Question:** What do you observe about station availability across central Washington, and what map evidence supports your interpretation?

    ### Transition

    Knowing where stations exist tells us about potential availability. It does not tell us how frequently those stations are used. We therefore move from station presence to observed trip activity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How is departure activity distributed among central-Washington stations?
    """)
    return


@app.cell
def _(mo, tl, trips):
    activity_ax, central_activity = tl.plot_station_activity(
        trips,
        area="central_dc",
        trip_end="start",
        show_landmarks=True,
    )

    mo.vstack([central_activity[["station", "departures"]].head(12), activity_ax])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examine the output

    Compare marker sizes across the map, then use the ranked table to identify the stations with the largest departure counts.

    > **Question:** What pattern do you observe in how departures are distributed among stations, and what evidence from the map and table supports your conclusion?

    ### Transition

    The spatial analysis shows where activity occurs. Capital Bikeshare must also understand when use is greatest, so we now shift from place to time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. What does the daily pattern reveal about when use is greatest?
    """)
    return


@app.cell
def _(mo, tl, trips):
    hour_ax, hourly_activity = tl.plot_trip_times(
        trips,
        by="start_hour",
        title="Trips by start hour",
    )

    result_df = hourly_activity.to_frame("trips").T
    result_df.columns = result_df.columns.astype(str)

    mo.vstack([result_df, hour_ax])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examine the output

    Trace the pattern from midnight through the end of the day. Focus on when activity rises and where the largest peaks occur.

    > **Question:** What are the most important features of the daily pattern, and what specific hours or values provide supporting evidence?

    ### Transition

    This overall pattern combines weekdays and weekends. Because daily routines often differ across the week, the combined pattern may hide important distinctions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. How do weekday and weekend timing patterns differ?
    """)
    return


@app.cell
def _(mo, tl, trips):
    daytype_ax, weekday_weekend = tl.plot_trip_times(
        trips,
        by="start_hour",
        compare="is_weekend",
        percent=True,
        title="Trip start times: weekday versus weekend",
    )

    result_weekday_weekend = weekday_weekend.T
    result_weekday_weekend.columns = result_weekday_weekend.columns.astype(str)

    mo.vstack([result_weekday_weekend, daytype_ax])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examine the output

    Compare the shapes of the two lines. Pay particular attention to the morning, midday, and late afternoon.

    > **Question:** What differences do you observe between weekday and weekend timing, and what chart evidence supports your interpretation?

    ### Transition

    We have examined geography and time separately. To understand service patterns more fully, we now ask how the geography of activity changes across selected time contexts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. How does the geography of activity change across time contexts?
    """)
    return


@app.cell
def _(mo, tl, trips):
    weekday_morning_ax, weekday_morning = tl.plot_station_activity(
        trips,
        area="central_dc",
        day_type="weekday",
        start_hour=(7, 9),
        show_landmarks=True,
        title="Weekday morning departures (7–9 AM)",
    )

    mo.vstack([weekday_morning[["station", "departures"]].head(8), weekday_morning_ax])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examine the first output

    Notice which stations have the largest markers during weekday mornings and use the table to confirm the leading locations.
    """)
    return


@app.cell
def _(mo, tl, trips):
    weekend_midday_ax, weekend_midday = tl.plot_station_activity(
        trips,
        area="central_dc",
        day_type="weekend",
        start_hour=(11, 15),
        show_landmarks=True,
        title="Weekend midday and afternoon departures (11 AM–3 PM)",
    )

    mo.vstack([weekend_midday[["station", "departures"]].head(8), weekend_midday_ax])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Compare the outputs

    Look for stations that become more or less prominent, while also noticing locations that remain active in both contexts.

    > **Question:** What spatial similarities and differences do you observe between the two time contexts, and what evidence from the maps or tables supports your account?

    ### Transition

    The integrated maps suggest that Capital Bikeshare may need both broad network coverage and attention to particular place-and-time combinations. We can now bring the spatial and temporal evidence together.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Develop an evidence-based service insight

    > **Question:** What insight could Capital Bikeshare use when reviewing its service? Support it with spatial and temporal evidence, explain a possible service implication, and identify one important limitation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Optional guided data science extension: clustering stations

    Capital Bikeshare manages many stations, making it difficult to examine each one separately. Clustering provides one way to summarize stations with similar hourly activity levels.
    """)
    return


@app.cell
def _(mo, tl, trips):
    cluster_results = tl.cluster_stations_by_time(
        trips,
        area="central_dc",
        number_of_groups=3,
        minimum_trips=40,
    )


    mo.vstack([cluster_results["cluster_summary"], cluster_results["assignments"][["station", "total_trips", "cluster_label"]].head(15), cluster_results["profile_ax"], cluster_results["map_ax"]])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examine the output

    First compare the average hourly profiles to see what distinguishes the clusters. Then examine marker colors and sizes on the map. Use the summary tables to check cluster sizes and station assignments.

    > **Question:** What appears to distinguish the clusters, what evidence supports that interpretation, and how could the grouping help Capital Bikeshare review station activity?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Independent exploration path: understanding rider types

    Capital Bikeshare identifies trips made by **members** and **casual riders**. Better understanding these customer groups could help the organization consider whether they have different service needs.

    The broad investigation question is:

    > **How do the timing and trip characteristics of members and casual riders differ, and what might Capital Bikeshare learn from those differences?**

    This path can be used as an in-class extension or as an assignment. It also gives you practice choosing and interpreting helper-function settings more independently.

    We begin with timing because different daily patterns may suggest that the two groups use the service in different ways.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 11. How do the daily timing patterns of members and casual riders differ?
    """)
    return


@app.cell
def _(mo, tl, trips):
    rider_time_ax, rider_time = tl.plot_trip_times(
        trips,
        by="start_hour",
        compare="member_casual",
        percent=True,
        title="Trip start times by rider type",
    )

    result_rider_time = rider_time.T
    result_rider_time.columns = result_rider_time.columns.astype(str)

    mo.vstack([result_rider_time, rider_time_ax])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examine the output

    Compare the shapes of the two lines rather than their total numbers. Focus on morning, midday, and late-afternoon activity.

    > **Question:** What differences do you observe between the daily patterns of members and casual riders, and what chart evidence supports your interpretation?

    ### Transition

    The overall comparison combines weekdays and weekends. We next examine how the rider-type contrast changes with day type.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12. How does the rider-type comparison change between weekdays and weekends?
    """)
    return


@app.cell
def _(mo, tl, trips):
    weekday_rider_ax, weekday_rider_time = tl.plot_trip_times(
        trips,
        by="start_hour",
        compare="member_casual",
        percent=True,
        day_type="weekday",
        title="Weekday trip start times by rider type",
    )

    result_weekday_rider_time = weekday_rider_time.T
    result_weekday_rider_time.columns = result_weekday_rider_time.columns.astype(str)

    mo.vstack([result_weekday_rider_time, weekday_rider_ax])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examine the weekday output

    Notice the timing and relative prominence of the member and casual peaks.
    """)
    return


@app.cell
def _(mo, tl, trips):
    weekend_rider_ax, weekend_rider_time = tl.plot_trip_times(
        trips,
        by="start_hour",
        compare="member_casual",
        percent=True,
        day_type="weekend",
        title="Weekend trip start times by rider type",
    )

    result_weekend_rider_time = weekend_rider_time.T
    result_weekend_rider_time.columns = result_weekend_rider_time.columns.astype(str)

    mo.vstack([result_weekend_rider_time, weekend_rider_ax])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Compare the outputs

    Compare the weekday and weekend charts. Look for changes in the size, timing, and shape of the differences between rider types.

    > **Question:** How does the member–casual contrast change between weekdays and weekends, and what evidence supports your conclusion?

    ### Transition

    Timing provides one view of customer behavior. Trip duration offers another perspective on how their use may differ.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 13. How do trip durations differ between members and casual riders?
    """)
    return


@app.cell
def _(mo, tl, trips):
    import matplotlib.axes

    _original_boxplot = matplotlib.axes.Axes.boxplot
    def _patched_boxplot(self, *args, **kwargs):
        if 'labels' in kwargs:
            kwargs['tick_labels'] = kwargs.pop('labels')
        return _original_boxplot(self, *args, **kwargs)

    matplotlib.axes.Axes.boxplot = _patched_boxplot

    rider_duration_ax, rider_duration = tl.plot_trip_durations(
        trips,
        compare="member_casual",
        max_minutes=40,
        title="Trip duration by rider type",
    )

    mo.vstack([rider_duration, rider_duration_ax])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examine the output

    Compare the shapes and centers of the distributions. In the summary table, pay particular attention to the medians because trip duration is skewed.

    > **Question:** What differences do you observe in member and casual trip durations, and what numerical or visual evidence supports your conclusion?

    ### Transition

    We now have evidence about both timing and duration. The final assignment step is to translate those patterns into a useful but appropriately cautious service insight.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14. What could Capital Bikeshare learn about members and casual riders?

    > **Assignment question:** What evidence-based insight could help Capital Bikeshare better understand and serve members and casual riders? Cite at least two pieces of supporting evidence and identify an important limitation.

    Prepare a concise response with:

    - **Question**
    - **Evidence examined**
    - **Main finding**
    - **Possible service implication**
    - **Important limitation**
    - **Additional information needed**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Return to your own questions

    The shared investigation and rider-type path illustrate how to move from a service mission to questions, evidence, interpretation, possible implications, and limitations.

    Return to the questions you developed at the beginning. You may now investigate one of them, revise or combine questions, or develop a new question suggested by the guided work.

    Use the provided helper functions and adjust their settings to gather evidence.

    > **Your exploration:** What question or questions will you investigate? What evidence will you examine, what observations and insights do you develop, and what limitations affect your conclusions?

    A concise response can include:

    - **Question or questions**
    - **Helper function and settings used**
    - **Supporting evidence**
    - **Insight for Capital Bikeshare**
    - **Possible service implication**
    - **Limitation or next question**
    """)
    return


if __name__ == "__main__":
    app.run()
