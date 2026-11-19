"""Student-facing tools for the CROSSROADS Ocean science module.

The public functions in this file support a question-driven investigation of
ocean science publications. Routine data preparation, filtering,
summary calculations, and plotting are kept here so the
main activity notebook can focus on questions, evidence, interpretation, and
limitations."""


"""import relevant libraries"""
from pathlib import Path
import pandas as pd
import numpy as np
import csv

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from pyvis import network as net

from IPython.display import Image

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
import math
import seaborn as sns

"""graphical plotting parameters"""
plt.rcParams["font.family"] = "Arial"
plt.rcParams['figure.constrained_layout.use'] = False
plt.rcParams['axes.formatter.limits'] = (-5,5)
sns.set(rc={'legend.frameon':False})
sns.set_style("whitegrid", {"axes.edgecolor": ".0", "axes.facecolor":"none"})
labelsize = 12
rcParams['xtick.labelsize'] = labelsize
rcParams['ytick.labelsize'] = labelsize 
rcParams['figure.titlesize'] = 24
plt.rc('legend',fontsize=12) 
plt.rc('axes', labelsize=labelsize)

pd.set_option('display.max_columns', 20)

graphing_colours = [
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

sns.set_palette(graphing_colours)


"""Functions"""

"""Load data (Part 1a). Load the dataset into the notebook"""
 
dataset = pd.read_excel('data/module_dataset_anonymized2.xlsx')



def data_summary(): 
    """Used in evaluate dataset (part 2). Will return a number of statistical outputs from the dataset"""

    print("Number of papers: \n{}".format(dataset['id'].nunique())),
    print("Oceans investigated: \n{}".format(sorted(dataset['ocean'].unique().tolist()))),
    print("Publication years: \n{}".format(sorted(dataset['pub year'].unique().tolist()))),
    print("Number of countries that published: \n{}".format(dataset['Country'].nunique())),
    print("Mean number of citations: \n{}".format(dataset[['id','citation count']].drop_duplicates()['citation count'].mean().round(1))),
    print("Number of international publications: \n{}".format(dataset[dataset['international']=='Y']['id'].nunique()))

def missing_data(): 
    """Used in evaluate dataset (part 2). Will return the number of rows with missing data for each column"""
    return pd.DataFrame(dataset.isna().sum()).reset_index().rename(columns={'index':'column',0:'Missing data'})

def publications_by_year(): 
    """Used in evaluate dataset (part 2). Will return the number of publications by year"""
    return pd.DataFrame(dataset.groupby(['pub year'])['id'].nunique()).reset_index().rename(columns={'id':'publication count'})


def country_list(): 
    """Used in evaluate dataset (part 2). Will return all unique countries/territories in the dataset"""
    return sorted(dataset['Country'].unique().tolist())
    
"""Shared investigation functions below"""

  
def country_output(topXcountries):
    """Used in part 4. Will group publications together by country and rank them with the country with most publications at the top. In the function, changing X will change the number of countries listed."""
    result = (dataset.groupby('Country')['id'].nunique().sort_values(ascending=False).reset_index().rename(columns={'id': 'publications'}))

    result['rank'] = result['publications'].rank(ascending=False)

    return result[['rank','Country','publications']].head(topXcountries)


def temporal_output(*args):
    """Used in part 5. Will take one, or a list of countries, publication output and group it by year of publication to create a timeseries graph."""

    plt.figure(figsize=(10,5))
    
    for country in [*args]:
        linegraph_data = dataset[(dataset['Country']==country)]
        linegraph_data = linegraph_data.groupby(['pub year'])['id'].nunique().reset_index()
        
        ax = sns.lineplot(x='pub year',y='id',data=linegraph_data,marker='o',label=country,legend=True)
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.ylabel ('Number of articles')
        plt.xlabel('Publication year')
        plt.xlim(2000,2025)
        #plt.ylim(0,2500)
    
    return plt.show()


def ocean_output(country):
    """Used in part 6. Will group country Xs publications by the ocean the research is relevant to and produce a table."""
    
    return pd.DataFrame(dataset[dataset['Country']==country].groupby(['ocean'])['id'].nunique()
                ).reset_index().rename(columns={'id':'publication count'})
        

def country_by_ocean_barplot(*args):
    """Used in Part 7. Will group publications by the relevant country or countries by ocean and produce a bar graph. Note that multiple countries can be placed in the function"""

    plt.figure(figsize=(10,5))
    
    barplot_data = dataset[dataset['Country'].isin([*args])]
    barplot_data = barplot_data.groupby(['Country','ocean'])['id'].nunique().reset_index()
    
    ax = sns.barplot(data=barplot_data,x='ocean',y='id',hue='Country',)
    sns.despine(top=True, right=True, left=False, bottom=False)
    plt.ylabel ('Number of Publications')
    plt.xlabel('Ocean')
    
    return plt.show()

def country_by_ocean_barplot_data(*args):
    """Used in Part 7. Will display the values of the barplot from function country_by_ocean_barplot. Note that multiple countries can be placed in the function."""

    barplot_data = dataset[dataset['Country'].isin([*args])]
    barplot_data = barplot_data.groupby(['Country','ocean'])['id'].nunique().reset_index().rename(columns={'id':'publications'})
    
    return barplot_data


def country_by_ocean(country):
    """Used in Part 8. Will determine the number of publications relevant to each ocean, as well as the country's publications in each ocean and then calculate a percentage value. These data will be presented in a table."""
    ocean_total_papers = dataset.groupby(['ocean'])['id'].nunique().reset_index().rename(columns={'id':'total ocean publications'})
    canada_ocean_papers = dataset[dataset['Country']==country].groupby(['ocean','Country'])['id'].nunique().reset_index().rename(columns={'id':'{} ocean publications'.format(country)})
    canada_ocean_summary = ocean_total_papers.merge(canada_ocean_papers,on=['ocean'])
    canada_ocean_summary['ocean %'] = ((canada_ocean_summary['{} ocean publications'.format(country)] / canada_ocean_summary['total ocean publications'])*100).round(2)
    return canada_ocean_summary


def ocean_countries(ocean,topXcountries):
    """Used in Part 9. Will filter the dataset to the ocean specified and then calculate the number of publications and the percentage for each country, producing a table. The top X countries will be listed by percentage share, with the highest first."""
    ocean_numberpapers = dataset[dataset['ocean']==ocean]['id'].nunique()
    
    ocean_topcountries = dataset[dataset['ocean']==ocean
        ].groupby(['Country'])['id'].nunique().sort_values(ascending=False
                                                          ).reset_index().rename(columns={'id':'papers'}).head(topXcountries)
    
    ocean_topcountries['percentage'] = ((ocean_topcountries['papers'] / ocean_numberpapers)*100).round(2)
    
    return ocean_topcountries

def collaboration(country,topXcountries):
    """Used in Part 10a. Will filter the data for all internationally collaborative papers and then calculate how many publications the specified country collaborates on with every other country. The top X collaborative partners will be listed by the percentage of collaborative publications, with the highest first. These data will be presented in a table."""
    collaboration_df = pd.DataFrame()
    
    for country in [country]:
        tempdf = dataset[dataset['international']=='Y']
        listofuts = tempdf[tempdf['Country']==country]['id'].unique().tolist()
        tempdf = dataset[dataset['id'].isin(listofuts)]
        tempdf = tempdf[tempdf['Country']!=country]
        tempdf = tempdf.groupby(['Country'])['id'].nunique().reset_index()
        tempdf['main_country_total'] = len(listofuts)
        tempdf['main_country']=country
        tempdf['percentage'] = ((tempdf['id'] / tempdf['main_country_total'])*100).round(2)
        tempdf.rename(columns={'main_country':'Analyzed country','main_country_total':'total publications','Country':'collaborator','id':'collaborating publications'},inplace=True)
        tempdf = tempdf[['Analyzed country','total publications','collaborator','collaborating publications','percentage']]
        
        collaboration_df = pd.concat([collaboration_df,tempdf])
    
    return collaboration_df.sort_values(by='collaborating publications',ascending=False).head(topXcountries)


def collaboration_network(country,min_collab_papers):
    """Used in part 10b. Will follow same approach as def_collaboration but will create a network diagram. Inputs are the country of interest and the minimum number of collaborative papers between the specific country and any country. Only collaborative countries with at least this many collaborating papers with the specified country will be plotted.""" 
    collaboration_df = pd.DataFrame()
    
    for country in [country]:
        tempdf = dataset[dataset['international']=='Y']
        listofuts = tempdf[tempdf['Country']==country]['id'].unique().tolist()
        tempdf = dataset[dataset['id'].isin(listofuts)]
        tempdf = tempdf[tempdf['Country']!=country]
        tempdf = tempdf.groupby(['Country'])['id'].nunique().reset_index()
        tempdf['main_country_total'] = len(listofuts)
        tempdf['main_country']=country
        tempdf['perc'] = ((tempdf['id'] / tempdf['main_country_total'])*100).round(2)
        tempdf.rename(columns={'Country':'collaborator','id':'collaborating_papers'},inplace=True)
        tempdf = tempdf[['main_country','main_country_total','collaborator','collaborating_papers','perc']]
        
    collaboration_df = pd.concat([collaboration_df,tempdf])
    
    data = collaboration_df[(collaboration_df['collaborating_papers']>=min_collab_papers)].sort_values(by=['collaborator'])
    
    g = nx.from_pandas_edgelist(df=data, source='main_country', target='collaborator',edge_attr=['collaborating_papers','perc']) 
    
    durations = [i['collaborating_papers'] for i in dict(g.edges).values()]
    
    nodesize = [i['perc'] for i in dict(g.edges).values()]
    
    labels = [i for i in dict(g.nodes).keys()]
    
    totpapers = data[['collaborator','perc']].drop_duplicates()
    totpapers['coallaborator'] = pd.Categorical(totpapers.collaborator, categories = labels, ordered = True)
    totpapers = totpapers.sort_values(by='collaborator')
    d = totpapers.set_index('collaborator')['perc'].to_dict()
    d_canada = ({"CANADA": 100}) 
    d_canada.update(d)
        
    labels = {i:i for i in dict(g.nodes).keys()}
    
    nodesize = [i for i in dict(d_canada).values()]
    nodesize=[v * 100 for v in d_canada.values()]
    
    colors = []
    for i in nodesize:
        if i ==10000:
            colors.append("red")
        elif 5000 < i < 10000:
            colors.append('orange')
        elif 2000 < i < 5000: 
            colors.append("yellow")
        elif 500 < i < 2000: 
            colors.append("greenyellow")
        elif 200 < i < 500: 
            colors.append("aqua")
        else: 
            colors.append('plum')
            
    fig, ax = plt.subplots(figsize=(15,10))
    pos = nx.spring_layout(g,k=0.7, iterations=19)
    nx.draw_networkx_nodes(g, pos, ax = ax, node_color=colors,node_size=nodesize)
    nx.draw_networkx_edges(g, pos, width=np.sqrt(durations), ax=ax,edge_color='lightblue')
    _ = nx.draw_networkx_labels(g, pos, labels, ax=ax,font_size=12,font_color='black')
    plt.axis('off')
    
    return plt.show()