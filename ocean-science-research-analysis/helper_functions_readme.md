# Investigating ocean science research: Who, Where, When?

## Helper functions

These functions are used in the interactive activity notebook to run code and produce results. The file defines all functions and provides example usages.

### Summary functions

**Function** *country_list()*

Will output a list of all countries and territories that participate in ocean science (i.e., have published at least one article in the period 2000-2020). There is no user input option. When entering country/territory names into other functions, be mindful of the spelling and abbreviated forms in this list. If names are incorrect, no data will be outputted. 

Functions *dataset.head(), data_summary(), publications_by_year() and missing_data()* in Parts 1 and 2 of the activity notebook have no inputs. 
These functions are only run when opening the dataset. The outputs of these will not change and these are not needed for investigating countries/terroritories in the shared investigation nor in the independent extension.

### Shared investigation path functions

Functions below are ordered by their use in the activity notebook

**Function** *country_output(X)*

Will group publications together by country, rank them, and output the top *X* countries, with the country with most publications at the top. Note that a maximum of 60 continuous entries can be listed in a table. **See Part 4 of the activity notebook.**

    Example use: country_output(20)


**Function** *temporal_output(X [,Y, Z])*

Will take the publication output of country, *X*, or a list of countries *X, Y, Z* etc. and group it by publication year to create a timeseries graph. Note that countries/territories must be between single (') quotation marks. **See Part 5.**

    Example 1 use: temporal_output('CANADA')

    Example 2 use: temporal_output('CANADA', 'JAPAN', 'AUSTRALIA', 'NORWAY’)

**Function** *ocean_output(X)*

Will group publications of country, *X*, by the ocean the research is relevant to and produce a table. **See Part 6.**

    Example use: ocean_output('CANADA')

**Function** *country_by_ocean_barplot(X [,Y, Z])*

Will group publications by country *X* or a list of countries *X, Y and Z* etc., as well as by ocean, and produce a bar graph. **See Part 7.**

    Example 1: country_by_ocean_barplot(‘CANADA’)
    Example 2: country_by_ocean_barplot(‘CANADA’, ‘NORWAY’)

**Function** *country_by_ocean_barplot_data(X [,Y, Z]))*

Will group publications by country *X* or a list of countries *X, Y and Z* etc., as well as by ocean, and produce a bar table. **See Part 7.**

    Example use: country_by_ocean_barplot('CANADA','JAPAN','AUSTRALIA','NORWAY')


**Function** *country_by_ocean(X)*

Will determine the number of publications relevant to each ocean, as well as the publications by Country *X* in each ocean and then calculate a percentage value share for that country in each ocean. These data will be presented in a table. **See Part 8.**

    Example use: country_by_ocean('CANADA')

**Function** *ocean_countries(O, Y)*

Will filter the dataset to ocean, *O*, and then calculate the number of publications and the percentage for each country, producing a table. *Y* countries will be listed by percentage share, with the highest first. **See Part 9.**

    Example use ocean_countries('arctic',10)


**Function** *collaboration(X, Y)*

Will filter the data for all internationally collaborative papers and then calculate how many publications Country *X* collaborates on with every other country.*Y* collaborative partners will be listed by the percentage of collaborative publications, with the highest first in a table. **See Part 10a.**

    Example use: collaboration('CANADA', 10)

**Function** *collaboration_network(X, Y)*

Will filter the data for all internationally collaborative papers and then calculate how many publications Country *X* collaborates on with every other country. It will then plot a network diagram of countries who have collaborated with Country *X* on a minimum of *Y* papers. **See Part 10b.**

    Example use: collaboration_network('CANADA', 50)
