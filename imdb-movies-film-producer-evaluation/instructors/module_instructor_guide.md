# Instructor Guide: Movies - Investigating Patterns, Types of Data, and Distribution of Data

## Module at a Glance

In this module, students act as **film producers** identifying trends in order to **pitch a movie** to be made by a major studio. 

The notebook uses short helper-function calls so that students with little or no programming experience can focus on evidence, interpretation, and limitations while becoming more comfortable using computational tools. The module may be taught with little-to-no focus on coding, or as a basic introduction to coding. 

**Suggested time**: 60 minutes for the shared investigation; 75–90 minutes with additional independent investigation.

## Learning Goals

Students will:

- Understand different types of data, such as categorical; textual; numerical; and time-series
- Interpret patterns, outliers, and the distribution of data.
- Form useful real-world questions about a field of research
- Use simple helper functions to investigate multiple properties (genre, commercial gross, critical rating, and time)
- Chart 2 different properties in order to use them to predict future values

By the end of this module, students should be able to:

- Tell the difference between types of data
- Create and investigate self-directed questions
- Explain interpretations of data using specific details
- Recognize limitations or issues in the data 

## Before Class

1. Confirm that the notebook, `tool_library.py`, and `data/` remain in the same folder structure.
2. Run `solution_interactive_python.ipynb` once in your intended Python environment.
3. Decide which components fit the available time:
   - shared investigation only;
   - shared investigation plus independent investigation
4. Consider asking students to work in pairs for the investigations.

## Suggested teaching sequence

### Introduction: Establish Module and Develop Questions (5 minutes):

    Students load the module on their computers. Instructor explains their role of movie producer and details how data is used by large film studios. Students develop some questions from this perspective, which may be utilitarian (e.g. "how can studios make the most money"), or creative (e.g. "how can I make the best Western film?", "how can I make a film that is like Star Wars", "how can I make a good family film"). Instructors should emphasize that forming a specific question is part of a real data scientist's job, not just a classroom activity!

### Questions 1-3: Data Evaluation (10 minutes):
    
Instructors highlight example questions which can be answered by the data, and model choosing the relevant columns for a question. Students examine the data and review the different kinds of column available. Students identify which parts of the data are relevant to their questions, and refine their questions based on the available data. Students may be prone to removing questions that _can_, in fact, be answered by the data; instructors should be prepared to ensure that students have at least 3 questions at the end. Students may form new questions if needed. Instructors inform students of shared investigation question. Instructor explains that for instruction's sake, the class will be answering the same question, but the same process can be used for any of students' questions.

### Questions 4-6: Distributions and Data Cleaning (15 minutes):
    
Instructors guide students through the start of the "Shared Investigation" section of the notebook, identifying uncommon categories and ideating possible explanations. Students may have different answers for questions in this section; this is okay, and instructors should emphasize that explanations may be subjective. Instructors guide students through removing these uncommon categories to produce clean data to investigate.

### Questions 6-9. Investigating Categories (15 minutes):
    
Instructors guide students through next section of the notebook. Students identify patterns for different genres of movie. Students may be tempted to jump ahead of summary statistics to only look at charts; instructors should emphasize that summary statistics are important to look at because they are easy to make arguments about, while visual lines are easy to interpret but harder to concretely and concisely define with words.

### Question 10. Investigating Questions & Producing Reports (10 minutes):
    
Students produce an answer to the shared investigation question. Students support their answer by citing specific elements of the data. Students copy/paste the relevant widgets to support their answer with graphics.

### Summation (5 minutes):

Instructors briefly walk students through a class investigation of the question (contained in solution_guide.md). Instructor highlights possible pitfalls and limitations in the data or methodology. Students contribute their answers: students notice similarities or differences across the class's answers.

### Questions 11-14: Optional independent investigation (15-30 minutes):

This optional further investigation allows students freedom to repeat the shared investigation while picking their own genres to look into. Instructors may choose to support an open, self-directed exploration; or provide the two following options for students to pick from. Instructors choosing to support an open self-directed exploration should be prepared to provide advice to students who do not have any interesting results from their chosen combination. It's important to emphasize in this case that data science is sometimes unconclusive.

Students may compare the Biography and Crime genres for an example of how a single outlying movie may affect the statistics. In 2019, the movie The Irishman was released, a blockbuster biopic from Martin Scorsese and Robert De Niro. Students should come to a conclusion that this outlier is likely not repeatable, and crime/biography movies are mostly comparable. Students should examine the summary statistics as well as the graph for full information! They may conclude that biography movies are more critically well-received and have the same financial success, and are therefore preferable, but students do not have to come to this conclusion to be successful at the investigation.

Alternatively, students may examine the Action and Adventure genres for a comparison of genres which don't present any notable differences. Students may note that both of these genres are rather similar. If any differences are noted, the median for adventure movies is slightly higher for critical score and slightly lower for financial success, but students may also only conclude that the genres are very similar.

## Facilitation guidance

- Keep questions visible before running code. The visualization is evidence for the question, not the purpose of the activity.
- Ask students to cite specific evidence: numbers, specific patterns of graphs, or specific datapoints where applicable.
- Ask students to decide about three levels of claims:
  - **observation:** directly visible in an output;
  - **interpretation:** a plausible explanation;
  - **implication:** a possible consideration for the job of a movie producer
- Welcome limited and negative findings. Emphasize that acknowledging the lack of a finding can prevent unnecessary decisions.


## Classroom adaptations

### 30–40 minute version

Use the Introduction, Data Evaluation, Investigating Categories, and Summation. Show the "Data Cleaning" and "Producing Reports" sections briefly or skip it. Expand Summation slightly, as students will not have done this activity individually.

### 60 minute version

Use the full shared investigation through to Question 10. Leave the optional investigation for independent work or a lab.

### 75–90 minute version

Begin the independent investigation in class.

### Courses with more programming experience

Invite students to inspect `tool_library.py`, alter code, or develop a new helper-function call. Preserve the question-driven structure even when code becomes more prominent. Invite students to modify the independent investigation to address other categories than "genre"; compare other fields than "gross" and "score"; or view time by month instead of year. 


## Assessment suggestions

A concise response can be assessed on whether it:

- states a clear question connected to the job of a producer;
- cites appropriate evidence;
- communicates a defensible insight;
- distinguishes evidence from interpretation;
- offers a cautious implication; and
- identifies any meaningful limitations or additional data needs.

## Data and interpretation cautions

- The movies provided are an arbitrary sample, and may have bias in skew towards IMDB's user preference.
- Yearly sample sizes differ.
- Movies without budget data or box office data, such as indie movies, are not included.
- All budgets are converted to dollars by IMDB. This is opaque and it's unclear of the rates used.
- Social impact and rich series/franchise information are not included. Actors who are not top-billed are not included.
- Associations and visible patterns do not establish causes.

## Technical notes

The helper library relies on Python 3, pandas, NumPy, and Matplotlib. It contains the data preparation, filtering, plotting, and clustering implementation used by the notebook.