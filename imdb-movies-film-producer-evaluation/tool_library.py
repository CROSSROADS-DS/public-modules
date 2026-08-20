from IPython.display import display
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def load_movie_data():
    df = pd.read_csv("./data/movies.csv").dropna(axis=0)
    display(df.head())
    return df

class SideBySide(object):
    def __init__(self, *items):
        self.items = items

    def __repr__(self):
        return "hi"

    def _repr_html_(self):
        return '<div style="display:flex;flex-wrap:wrap; gap: 1em">'  + ''.join( [ 
           s._repr_html_()
           for s in self.items
           ]) + "</div>"

def show_dataset_scope(data):
    display(SideBySide(pd.DataFrame({
        "Value": [
            len(data),
            data["year"].min(),
            data["year"].max(),
            data["genre"].nunique(),
            data["country"].nunique(),
            data["company"].nunique(),
        ]
    },
    index=[
        "Number of Movies",
        "Earliest movie (year)",
        "Latest movie (year)",
        "Unique genres",
        "Unique countries",
        "Unique production companies",
    ]),

    pd.DataFrame({"# of Movies per Genre": data["genre"].value_counts()}),
    pd.DataFrame({"# of Movies per Country (top 10)": data["country"].value_counts().head(n=10)}),
    pd.DataFrame({"# of Movies per Company (top 10)": data["company"].value_counts().head(n=10)})))

def plot_number_of_movies_by_genre(data):
    data['genre'].value_counts().plot.bar(title="Number of Movies by Genre")
    plt.show()

def show_movies_in_genre(data, genre):
    display(data[data["genre"] == genre])

def without_small_categories(data, limit=30, by="Enter a field in the 'by' option."):
    vc = data[by].value_counts()

    return data[data[by].isin(vc[vc > limit].index)]


def show_recent_summary_details(df, genres, property, years, category_property="genre"):
    target_gt_year = df["year"].max() - years

    stat_columns = [(genre, df[ (df[category_property] == genre) & (df["year"] > target_gt_year)][property]) for genre in genres]

    dataframes = [pd.DataFrame({f"{property} for {genre} Movies": [
            described_column.mean(),
            described_column.median(),
            described_column.min(),
            described_column.max(),
        ]}, index=[
            "Mean (Average)",
            "Median",
            "Minimum",
            "Maximum"
        ]) for genre, described_column in stat_columns]

    display(SideBySide(*dataframes))

def show_plot_over_time(df, genres, property, category_property="genre", time_property="year"):
    rating_counts = df[
        df[category_property].isin(list(genres))
        ].groupby([time_property, category_property])[[property]].median().unstack()

    f = plt.figure()
    ax = f.gca()

    units = {
        1_000_000_000: 'B',
        1_000_000: 'M',
        1_000: 'K',        
    }
    for (unit_boundary, unit) in units.items():
        #if rating_counts.min(axis=None) > unit_boundary: (original code)
        if rating_counts[property].min().min() > unit_boundary:
            def fmt_millions(x, pos):
                return f"{int(x / unit_boundary)}{unit}"
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(fmt_millions))
            break

    rating_counts[property].plot(title=f"Median movie {property} over {time_property}s, by genre", ylabel=f"Median {property}", ax=ax)
    plt.show()

def compare_categories(data, size=..., category=..., compare=..., compared_by=..., chart_by=...):
    if size == ...:
        print("You must define the minimum size for categories. For example, use size=30 to specify a minimum size of 30")
        return
    if category == ...:
        print("You must define the category. For example, use category=\"genre\" to compare different genres")
        return
    
    data = without_small_categories(data, limit=size, by=category)
    plot_number_of_movies_by_genre(data)

    if compare == ...:
        print("In the next step, specify the categories to compare; e.g. compare=(\"a\", \"b\")")
        return
    if compared_by == ...:
        print("In the next step, specify the properties to compare categories by; e.g. compare_by=(\"a\", \"b\")")
        return

    for compare_by_property in compared_by:
        show_recent_summary_details(data, genres=compare, property=compare_by_property, years=10, category_property=category)

    if chart_by == ...:
        print("In the next step, specify the chart comparison property; e.g. chart_by=\"year\"")
        return
    
    for compare_by_property in compared_by:
        show_plot_over_time(data, genres=compare, property=compare_by_property, category_property=category, time_property=chart_by)