# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.23.15",
#     "pandas",
#     "openpyxl",
#     "numpy",
#     "matplotlib",
#     "seaborn",
#     "altair",
#     "networkx",
# ]
# ///
import marimo

__generated_with = "0.23.15"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Data science taster module
    ## Data science for science and technology policy
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Analysis task - Ocean science research investigation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is a Jupyter notebook. Here, it is used to create, run and visualise python computer code to analyse the ocean science dataset.

    Each cell in the notebook will carry out the functions within it. If requested (such as displaying a graph), the output of the cell will be displayed directly below it.

    This setup allows easy de-bugging (error fixing) and a clear history of what has been coded.

    For the analysis, inputs can be changed (such as the country of interest) in the cells as needed. Where this can be done will be highlighted in the appropriate cells.

    Run each cell one at a time by holding down the shift and return key simultaneously or by pressing the 'play' button in the icon bar above.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Motivation and questions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You work for the Natural Sciences and Engineering Council of Canada (NSERC)

    NSERC are interested in allocating more funding for research pertaining to UN Sustainable Development Goal 14 - Life below water - particularly in regard to oceans

    For this, they must first understand Canada's current ocean science research output.

    Your boss has procured a dataset for you to analyze and wants to know:
    - Canada's overall ocean science research output.
    - How Canada's output compares to three trade partners (Australia, Norway and Japan) and how this has changed over time.
    - In what ocean does Canada have greater output than these comparators?
    - And where does Canada rank in this ocean in terms of output?
    - How much collaboration does Canada do with these, and other, partners?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Preamble
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### This installs the relevant programming libraries and tools needed
    """)
    return


@app.cell
def _():
    import pandas as pd
    import csv
    import sys
    import numpy as np
    #import dataframe_image as dfi
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import seaborn as sns
    import altair as alt
    # '%matplotlib inline' command supported automatically in marimo

    #pd.set_option('display.max_rows', 100)
    pd.set_option('display.max_columns', 20)

    print('python :',sys.version)
    print('numpy: ',np.__version__)
    print('pandas: ',pd.__version__)
    print('matplotlib: ',pd.__version__)
    print('seaborn: ',sns.__version__)
    return alt, np, pd, plt, sns


@app.cell
def _(plt, sns):
    from matplotlib import rcParams
    from matplotlib.ticker import MaxNLocator
    import matplotlib.ticker as ticker
    import math
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['figure.constrained_layout.use'] = False
    plt.rcParams['axes.formatter.limits'] = (-5, 5)
    sns.set(rc={'legend.frameon': False})
    sns.set_style('whitegrid', {'axes.edgecolor': '.0', 'axes.facecolor': 'none'})
    labelsize = 12
    rcParams['xtick.labelsize'] = labelsize
    rcParams['ytick.labelsize'] = labelsize
    rcParams['figure.titlesize'] = 24
    plt.rc('legend', fontsize=12)
    # '%matplotlib inline' command supported automatically in marimo
    plt.rc('axes', labelsize=labelsize)  # using a size in points  # fontsize of the x and y labels
    return


@app.cell
def _():
    import networkx as nx
    try:
        from networkx.drawing.nx_agraph import graphviz_layout
        from pyvis import network as net
    except ModuleNotFoundError:
        print("Network visualization packages not available in browser mode.")

    return (nx,)


@app.cell
def _(sns):
    isi_colour = [
    "#CF005B" 
    ,"#004AFF"
    ,'green'    
    ,"#12CAC9"
    ,"goldenrod"
    ,'pink'
    ,"#85F0AD"
    ,'gold'
    ,'salmon'
    ,'#000000'
    ,"#646363" 
    ,"#9D9D9C" 
    ,"#DADADA"]

    sns.set_palette(isi_colour)
    sns.palplot(sns.color_palette())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Open dataset and find some basic statistics about it

    ### e.g. How many papers?, What are the publication years?
    """)
    return


@app.cell
def _(pd):
    dataset = pd.read_excel('https://raw.githubusercontent.com/cjschrader/public-modules/python-files/ocean-science-research-analysis/module_dataset.xlsx')
    dataset.head()
    return (dataset,)


@app.cell
def _(dataset):
    dataset['ut'].nunique()
    return


@app.cell
def _(dataset):
    dataset['ocean'].unique()
    return


@app.cell
def _(dataset):
    dataset['pub year'].unique()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Is Canada one of the top producing countries?
    """)
    return


@app.cell
def _(dataset):
    country_list_by_count = dataset.groupby(['Country'])['ut'].nunique().sort_values(ascending=False).reset_index()
    country_list_by_count.head(20)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How does Canada's output change over time and how does this compare to the three trade partners?
    """)
    return


@app.cell
def _(alt, dataset):
    countries = ['CANADA', 'JAPAN', 'AUSTRALIA', 'NORWAY']
    filtered_df = dataset[dataset['Country'].isin(countries)]
    plot_data = (
        filtered_df.groupby(['Country', 'pub year'])['ut']
        .nunique()
        .reset_index(name='Number of articles')
    )
    chart = (
        alt.Chart(plot_data)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                'pub year:Q',
                title='Publication year',
                scale=alt.Scale(domain=[2000, 2025], clamp=True),
                axis=alt.Axis(values=[2000, 2005, 2010, 2015, 2020, 2025], format="d")
            ),
            y=alt.Y(
                'Number of articles:Q',
                title='Number of articles'
            ),
            color=alt.Color(
                'Country:N',
                title='Country'
            ),
            tooltip=['Country', 'pub year', 'Number of articles']
        )
        .properties(
            width=600,
            height=300
        )
        .interactive()
    )
    chart
    return


@app.cell
def _(dataset, plt, sns):
    plt.figure(figsize=(10, 5))
    for _country in ['CANADA', 'JAPAN', 'AUSTRALIA', 'NORWAY']:
        linegraph_data = dataset[dataset['Country'] == _country]
        linegraph_data = linegraph_data.groupby(['pub year'])['ut'].nunique().reset_index()
        _ax = sns.lineplot(x='pub year', y='ut', data=linegraph_data, marker='o', label=_country, legend=True)
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.ylabel('Number of articles')
        plt.xlabel('Publication year')
        plt.xlim(2000, 2025)
    plt.gca()  #plt.ylim(0,2500)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What is the distrubtion of Canadian research output by ocean?
    """)
    return


@app.cell
def _(dataset):
    dataset[dataset['Country']=='CANADA'].groupby(['ocean'])['ut'].nunique()
    return


@app.cell
def _(alt, dataset):
    barplot_data_grouped = dataset[dataset['Country'].isin(['CANADA', 'JAPAN', 'AUSTRALIA', 'NORWAY'])]
    plot_data_bar = (
        barplot_data_grouped.groupby(['Country', 'ocean'])['ut']
        .nunique()
        .reset_index(name='Number of articles')
    )
    bar_chart = (
        alt.Chart(plot_data_bar)
        .mark_bar()
        .encode(
            x=alt.X(
                'ocean:N', 
                title='Ocean'
            ),
            y=alt.Y(
                'Number of articles:Q', 
                title='Number of articles'
            ),
            color=alt.Color(
                'Country:N', 
                title='Country'
            ),
            xOffset='Country:N',
            tooltip=['Country', 'ocean', 'Number of articles']
        )
        .properties(
            width=600,   
            height=300
        )
        .interactive()   
    )
    bar_chart
    return


@app.cell
def _(dataset, plt, sns):
    plt.figure(figsize=(10, 5))
    barplot_data = dataset[dataset['Country'].isin(['CANADA', 'JAPAN', 'AUSTRALIA', 'NORWAY'])]
    barplot_data = barplot_data.groupby(['Country', 'ocean'])['ut'].nunique().reset_index()
    _ax = sns.barplot(data=barplot_data, x='ocean', y='ut', hue='Country')
    sns.despine(top=True, right=True, left=False, bottom=False)
    plt.ylabel('Number of articles')
    plt.xlabel('Ocean')
    plt.gca()
    return (barplot_data,)


@app.cell
def _(barplot_data):
    barplot_data
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What is the percentage of papers that Canada publishes?
    """)
    return


@app.cell
def _(dataset):
    ocean_total_papers = dataset.groupby(['ocean'])['ut'].nunique().reset_index().rename(columns={'ut':'total ocean papers'})
    canada_ocean_papers = dataset[dataset['Country']=='CANADA'].groupby(['ocean','Country'])['ut'].nunique().reset_index().rename(columns={'ut':'Canada ocean papers'})
    canada_ocean_summary = ocean_total_papers.merge(canada_ocean_papers,on=['ocean'])
    canada_ocean_summary['ocean %'] = ((canada_ocean_summary['Canada ocean papers'] / canada_ocean_summary['total ocean papers'])*100).round(2)
    canada_ocean_summary
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Arctic ocean is where Canada has its largest share. Is is the largest contributor in that ocean?
    """)
    return


@app.cell
def _(dataset):
    arctic_ocean_numberpapers = dataset[dataset['ocean']=='arctic']['ut'].nunique()

    arctic_ocean_topcountries = dataset[dataset['ocean']=='arctic'
        ].groupby(['Country'])['ut'].nunique().sort_values(ascending=False
                                                          ).reset_index().rename(columns={'ut':'papers'}).head(10)

    arctic_ocean_topcountries
    return arctic_ocean_numberpapers, arctic_ocean_topcountries


@app.cell
def _(arctic_ocean_numberpapers, arctic_ocean_topcountries):
    arctic_ocean_topcountries['percentage'] = (arctic_ocean_topcountries['papers'] / arctic_ocean_numberpapers)*100
    return


@app.cell
def _(arctic_ocean_topcountries):
    arctic_ocean_topcountries
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What countries does Canada collaborate with considering all its output?
    """)
    return


@app.cell
def _(dataset, pd):
    collaboration_df = pd.DataFrame()
    for _country in ['CANADA']:
        tempdf = dataset[dataset['international'] == 'Y']
        listofuts = tempdf[tempdf['Country'] == _country]['ut'].unique().tolist()
        tempdf = dataset[dataset['ut'].isin(listofuts)]
        tempdf = tempdf[tempdf['Country'] != _country]
        tempdf = tempdf.groupby(['Country'])['ut'].nunique().reset_index()
        tempdf['main_country_total'] = len(listofuts)
        tempdf['main_country'] = _country
        tempdf['perc'] = (tempdf['ut'] / tempdf['main_country_total'] * 100).round(2)
        tempdf.rename(columns={'Country': 'collaborator', 'ut': 'collaborating_papers'}, inplace=True)
        tempdf = tempdf[['main_country', 'main_country_total', 'collaborator', 'collaborating_papers', 'perc']]
        collaboration_df = pd.concat([collaboration_df, tempdf])
    collaboration_df.sort_values(by='collaborating_papers', ascending=False).head(20)
    return (collaboration_df,)


@app.cell
def _(collaboration_df, np, nx, pd, plt):
    data = collaboration_df[collaboration_df['collaborating_papers'] >= 50].sort_values(by=['collaborator'])
    g = nx.from_pandas_edgelist(df=data, source='main_country', target='collaborator', edge_attr=['collaborating_papers', 'perc'])
    durations = [i['collaborating_papers'] for i in dict(g.edges).values()]
    nodesize = [i['perc'] for i in dict(g.edges).values()]
    labels = [i for i in dict(g.nodes).keys()]
    totpapers = data[['collaborator', 'perc']].drop_duplicates()
    totpapers['coallaborator'] = pd.Categorical(totpapers.collaborator, categories=labels, ordered=True)
    totpapers = totpapers.sort_values(by='collaborator')
    d = totpapers.set_index('collaborator')['perc'].to_dict()
    d_canada = {'CANADA': 100}
    d_canada.update(d)
    labels = {i: i for i in dict(g.nodes).keys()}
    nodesize = [i for i in dict(d_canada).values()]
    nodesize = [v * 100 for v in d_canada.values()]
    colors = []
    for i in nodesize:
        if i == 10000:
            colors.append('red')
        elif 5000 < i < 10000:
            colors.append('orange')
        elif 2000 < i < 5000:
            colors.append('yellow')
        elif 500 < i < 2000:
            colors.append('greenyellow')
        elif 200 < i < 500:
            colors.append('aqua')
        else:
            colors.append('plum')
    fig, _ax = plt.subplots(figsize=(15, 10))
    pos = nx.spring_layout(g, k=0.7, iterations=19)
    nx.draw_networkx_nodes(g, pos, ax=_ax, node_color=colors, node_size=nodesize)
    nx.draw_networkx_edges(g, pos, width=np.sqrt(durations), ax=_ax, edge_color='lightblue')
    _ = nx.draw_networkx_labels(g, pos, labels, ax=_ax, font_size=12, font_color='black')
    plt.axis('off')
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Canada is the sixth largest producer of ocean research
    - Yearly output has stagnated (around 450 papers) and now lower than Australia
    - Canada has most papers covering the Atlantic but its largest share is in the Arctic, where it is the thid biggest contributor
    - Fifty percent of Canada's collaboration is with the US
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## NSERC potential funding calls
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Canadian Arctic research (increase output to become the leading contributor)
    - Trade partner collaborations (increase collaborations with Norway, Australia or Japan to strengthen trade agreements and knowledge transfer)
    - Lessen or remove funding for Indian or Southern ocean research (due to low contributions)
    """)
    return


if __name__ == "__main__":
    app.run()
