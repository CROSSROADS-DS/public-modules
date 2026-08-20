# FIFA Players: Investigating Skill, Age, and Cost

## Module overview

How can data about individual players help someone decide where to spend a limited budget? In this introductory module, students take the role of a manager running a FIFA team who cannot buy in-game credits and must therefore decide what *type* of player is worth paying for.

Students begin by developing questions that could help a manager on a budget. They then evaluate the available data, refine their questions, and follow a shared investigation into what separates highly rated players from the rest and how older players differ from younger ones. The activity emphasizes evidence-based reasoning, cautious interpretation, and the idea that a comparison must be made fair before it can be trusted.

## Intended audience

This module is designed for introductory college courses in data science and statistics, and for courses in sports management, business, economics, and general education. It can also serve as an approachable early activity in a programming course.

No prior programming experience is required. Students run and adjust short helper-function calls while focusing on questions, evidence, and interpretation. Students with more experience may inspect or extend the Python code.

Familiarity with soccer is helpful but not required. The module explains what each attribute measures, and the central reasoning does not depend on knowing the sport.

## Learning goals

By the end of the module, students should be able to:

- formulate and refine questions that can be investigated with available data;
- describe a distribution and compare groups using specific numerical evidence;
- recognize survivorship bias and explain how it distorts an apparent trend;
- construct a controlled comparison by grouping, and check that the control worked;
- distinguish observations from interpretations and implications;
- identify important limitations of a prepared dataset;
- use simple helper functions to continue an independent investigation; and
- explain how data science can support a decision about how to spend limited resources.

## Data

The activity uses player data originally scraped from the **FIFA 2018-2019 video game** and compiled into a public soccer database. Each row describes one player as the game rated them during that season, including age, overall rating, twenty-nine individual skill attributes, transfer value, and weekly wage.

The dataset has been adapted for learning and reliable browser-based use. Goalkeepers were removed, because the twenty-nine attributes describe outfield skills only and none of them describe goalkeeping. The `potential` column was also removed, because it is a projection of a player's future rather than a description of the player as they are now. The prepared file contains 15,675 field players and no missing values.

An important characteristic of this dataset is that the ratings were assigned by the game's designers rather than measured on a field. This is a feature rather than a flaw for a module about interpretation: it gives students an authentic dataset whose limitations are concrete and easy to reason about.

## Classroom use

The guided investigation is designed for approximately **60 minutes**. Instructors may add the optional independent exploration for a **90 minute** session, homework, or follow-up assignment.

The notebook is modular. Instructors may use the shared investigation alone, assign the independent exploration, or select individual sections for a shorter class. Sections 4 and 5, which cover what a high rating is made of, work as a self-contained 20-minute activity if time is very limited.

## Software

The activity is provided as a Python notebook designed to run in Jupyter or JupyterLite. Students use the included `tool_library.py`; no software installation or substantial coding is required when the notebook is launched through the CROSSROADS Hub.

```python

```
