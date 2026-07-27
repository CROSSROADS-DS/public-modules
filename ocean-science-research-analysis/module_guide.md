# Ocean Science Research Analysis

## Module Overview

This introductory module demonstrates how data science can be used to investigate a real-world question in science and technology policy. Students analyze publication-level data about global ocean science research, with particular attention to research activity, international collaboration, geographic coverage, and Canada's role in the field.

The module follows a practical progression from questions to data, analysis, interpretation, and possible application. A hypothetical research-funding context provides motivation, but the central emphasis is on purposeful data analysis and evidence-based reasoning.

## Intended Audience

The module is designed for introductory undergraduate use and may fit courses or programs in data science, environmental science, geography, sustainability, science and technology studies, public policy, political science, economics, business, journalism, and science communication.

It may also be used as a short interdisciplinary activity for students who are curious about how data can inform decisions outside a traditional computing course.

## Learning Goals

By completing the module, students should be able to:

- explain how data analysis can support domain-specific decisions;
- inspect a real dataset and identify its structure and limitations;
- connect motivating questions with appropriate forms of analysis;
- interpret summary statistics, tables, and common visualizations;
- describe patterns in research activity and international collaboration;
- distinguish observations supported by the dataset from claims that require additional evidence; and
- communicate evidence-based findings and possible recommendations.

## Prerequisites

No prior programming experience is required.

Students should have basic familiarity with:

- percentages and averages;
- tables and simple summaries; and
- line charts and bar charts, including horizontal and vertical axes.

The interactive notebook contains Python code, but students are not expected to write the code themselves. The code serves as the analysis tool; the main learning goals concern the questions being asked, the analyses used to answer them, and the interpretation of the results.

## Estimated Time

Approximately 60–90 minutes, depending on the amount of instructor discussion and whether students explore alternative countries, oceans, or comparisons in the interactive notebook.

## Module Materials

- `module_guide.md` — an overview for educators considering or preparing to use the module;
- `activity_guide.md` — an introduction to the activity, its motivating context, questions, dataset, and analytical approach;
- `activity_interactive_python.ipynb` — the interactive Python notebook;
- `activity_web.html` — a web version with the analysis and outputs already displayed;
- `module_metadata.yml` — structured information used by the module catalog and publication tools; and
- the dataset and any supporting images included with the module.

## Dataset Overview

The dataset contains bibliographic metadata for ocean science research publications. Each record represents a research publication and may include:

- a unique publication identifier;
- a digital object identifier (DOI);
- publication year;
- article title;
- journal;
- author keywords;
- citation count;
- associated ocean basin;
- countries represented in the authors' institutional affiliations;
- number of unique contributing countries; and
- an indicator of international collaboration.

The dataset was derived from bibliographic records used in a published study of the global ocean science community. It supports descriptive analysis of research output, collaboration, geographic coverage, journals, and topics.

## Important Dataset Limitations

Students should consider whether fields are complete, whether a publication appears in more than one row, and what years are covered.

Raw citation counts should not be used for direct comparisons of research impact without accounting for factors such as publication year, discipline, and citation practices. The dataset can reveal patterns in the recorded publications, but it cannot by itself explain why those patterns exist or determine the quality or societal value of particular research programs.

## Suggested Uses

The module can be used as:

- a stand-alone introduction to applied data science;
- an example of bibliometric or scientometric analysis;
- a guided activity in environmental science, sustainability, public policy, or science and technology studies;
- a discussion starter about research funding and evidence-based decision-making; or
- an illustration of how the same analytical workflow can be transferred to other domains.

Instructors may use the web version to review the activity without running a notebook. Instructors comfortable with Python and Jupyter may run the interactive notebook live and modify selected parameters to explore different countries, oceans, or comparisons.
