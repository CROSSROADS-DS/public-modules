# Ocean Science Research Analysis: Activity Guide

## Why This Activity Matters

Scientific research depends on funding from governments, private organizations, foundations, universities, and other sources. Because funding is limited and often competitive, research and funding organizations need credible evidence when considering priorities and possible investments.

This activity shows how publication data can be analyzed to better understand a research field. It focuses on ocean science, but the same question–data–analysis–interpretation process can be applied in many other areas.

## Motivating Context

Imagine that you are a data analyst supporting the Natural Sciences and Engineering Research Council of Canada (NSERC). NSERC is considering future support for ocean science related to the United Nations Sustainable Development Goal 14, **Life Below Water**, and the United Nations Decade of Ocean Science for Sustainable Development.

Before discussing possible funding priorities, the organization wants to better understand Canada's current role in global ocean science research.

This is a hypothetical scenario designed to provide a realistic purpose for the analysis. The activity is not intended to teach or endorse a particular funding policy.

## Questions You Will Investigate

The guided analysis considers questions such as:

- What is Canada's overall ocean science research output?
- How does Canada's output compare with selected partner countries, including Australia, Norway, and Japan?
- How have these patterns changed over time?
- In which ocean basin does Canada have greater output than the selected comparison countries?
- How does Canada rank among countries studying that ocean basin?
- How frequently does Canada collaborate internationally?
- Which countries appear most often as Canada's research partners?

The notebook may also support exploration of other countries, oceans, journals, keywords, and patterns.

## The Dataset

The activity uses publication-level metadata describing global ocean science research. Fields may include:

- `Ut` — a unique publication identifier;
- `Doi` — the article's digital object identifier;
- `pub year` — year of publication;
- `Title` — article title;
- `Journal` — journal in which the article was published;
- `keywords` — author or publication keywords;
- `citation count` — number of recorded citations;
- `ocean` — ocean basin associated with the publication;
- `Country` — countries represented in the authors' institutional affiliations;
- `Country unique` — number of unique contributing countries; and
- `International` — whether authors from at least two countries contributed to the publication.

Each record should be interpreted in light of the dataset's organization. Before drawing conclusions, consider whether values are missing, whether a publication can appear more than once, and which publication years are included.

## What You Will Do

You will move through a guided data science workflow:

1. Examine the dataset and its fields.
2. Check the data for features that affect interpretation.
3. Summarize publication activity for Canada and selected comparison countries.
4. Use tables and visualizations to examine changes over time.
5. Compare research activity across ocean basins.
6. Investigate international collaboration patterns.
7. Interpret the evidence and discuss possible implications.

The activity emphasizes understanding why an analysis is used and what its results mean. You are not expected to understand every line of Python code.

## Analysis and Visualization

The notebook uses descriptive analysis and common visualizations, including counts, percentages, rankings, line charts, and bar charts. Some notebook parameters may be changed to explore a different country or ocean basin.

When reviewing each result, ask:

- What question does this analysis address?
- What does the table or visualization show?
- What conclusion is supported by the evidence?
- What cannot be concluded from the available data?

## Expected Outcomes

By the end of the activity, you should be able to describe important patterns in the dataset, explain how those patterns relate to the motivating questions, and communicate findings that could contribute to a broader discussion of research priorities.

Your conclusions should be framed carefully. Publication counts and collaboration patterns provide useful evidence, but they do not by themselves measure research quality, societal impact, or the amount of funding a country should receive.

## Ways to Use the Activity

- Open `activity_web.html` to view the complete activity and its outputs in a web browser.
- Open `activity_interactive_python.ipynb` to run the analysis and, where indicated, explore alternative inputs.

No prior programming experience is required for either option.
