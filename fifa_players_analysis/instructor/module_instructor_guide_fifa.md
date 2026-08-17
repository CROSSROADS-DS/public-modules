# FIFA Players: Investigating Skill, Age, and Cost

## Module at a glance

In this introductory module, students act as a manager running a FIFA team on a limited budget who must decide what type of player to spend money on. The activity is organized around questions rather than software: students develop questions, evaluate whether the available data can address them, follow a shared investigation, and then conduct further exploration.

The notebook uses short helper-function calls so that students with little or no programming experience can focus on evidence, interpretation, and limitations while becoming more comfortable using computational tools.

The intellectual spine of the module is **fair comparison**. Students meet a pattern that looks obvious, discover that the comparison producing it was not fair, build a better one, and check that it worked. That sequence occurs three times, at increasing subtlety.

Suggested time: **60 minutes** for the shared investigation; **90 minutes** with the optional independent exercise (which could also be assigned as homework).

Programming prerequisite: None. Soccer knowledge: helpful but not required.

## Fields of analysis

This analysis falls under **sports analytics**, the application of statistical methods to athletic performance and team decision-making, and more specifically **recruitment analytics**, which uses data on player characteristics to inform signing decisions. Professional clubs employ analysts who do a more sophisticated version of what students do here.

The statistical ideas underneath are general rather than sport-specific. **Selection bias** describes what happens when the process that put records into a dataset is related to what is being measured, and **confounding** describes what happens when two explanations for a pattern cannot be separated by the comparison being made. Both appear in nearly every applied field, and both are easier to see in this dataset than in most.

## Learning goals

Students should be able to:

- formulate and refine questions that can be investigated with available data;
- describe a distribution and compare groups using specific numerical evidence;
- recognize survivorship bias and explain how it distorts an apparent trend;
- construct a controlled comparison by grouping, and check that the control worked;
- distinguish observations from interpretations and implications;
- identify important limitations of a prepared dataset;
- use simple helper functions to continue an independent investigation; and
- explain how data science can support a decision about how to spend limited resources.

## Before class

- Confirm that the notebook, `tool_library.py`, and `data/` remain in the same folder structure.
- Run the activity notebook once in the intended environment.
- Decide which components fit the available time: shared investigation only, or shared investigation plus independent exercise.
- Consider asking students to work in pairs when developing questions and when writing the three predictions.
- Be ready for the three prediction points. Most students predict that pace separates the best players, that rating declines after a peak, and that equally rated players have similar skills. All three predictions are wrong in instructive ways, and the module works best when students have committed to them in writing first.
- Note that the dataset describes a video game. Students who play FIFA may arrive with strong opinions about which attributes matter; this is useful energy, but it is not evidence, and the distinction is worth naming early.

## Suggested teaching sequence

### 1. Establish the mission and develop questions - 5 minutes

Introduce students to their role as a manager with a fixed budget and no credits to spend. Ask them to develop one or more questions that could help decide what type of player to buy.

Avoid evaluating questions too quickly. At this stage, the goal is curiosity and relevance.

### 2. Meet and evaluate the data - 8 minutes

Students load the data, review the source and preparation explanation, and examine the dataset summary. Emphasize that evaluating the evidence is part of data science, not a preliminary task separate from it.

Draw attention to why goalkeepers were removed: an entire group of players is unmeasurable with the columns available. Ask students to revise, narrow, replace, or add questions after seeing what the data contain and what is missing.

### 3. What a high rating is made of (sections 4-5) - 12 minutes

Students examine the rating distribution, commit to a prediction, and compare attribute averages across rating groups. The result usually surprises them: the mental and technical attributes separate players by roughly 20 rating points while pace separates them by 5.

Have several students read out their predictions before the chart appears. The surprise does most of the teaching here.

### 4. Age and survivorship (sections 6-7) - 10 minutes

Students examine the age distribution, predict the shape of the age-rating relationship, and find that average rating never declines. Give this the time it needs. The explanation is not that players stop aging; it is that the players who declined are no longer in the file.

A useful prompt: "what would have to be true about the data collection for this chart to be honest?"

### 5. Building a fair comparison (section 8) - 8 minutes

Students meet the age-by-rating grid, examine cell counts, and then check whether the grouping actually holds rating constant. One row fails the check. Let students find it rather than pointing it out.

### 6. Skill profiles by age (section 9) - 10 minutes

Students compare age groups within a single rating group, then repeat in a second rating group. The bars point in both directions, which is the central finding of the module: equally rated players are not interchangeable.

### 7. Cost (section 10) - 10 minutes

Students compare transfer value and weekly wage across the grid, then look at what changes in skill alongside the price. The value grid and the wage grid behave differently, which is worth pausing on.

### 8. Strategy, result summation, and limitations - 10-15 minutes

Students turn the evidence into a strategy and state what their team would gain and lose. Both major strategies are defensible; the assessment target is whether the trade-off is named and evidenced.

### 9. Independent analysis - 20-30 minutes outside the core

Students return to their own questions and investigate one using the same helper functions with different settings. Suitable for homework or a follow-up class.

## Facilitation guidance

- Keep questions visible before running code. The visualization is evidence for the question, not the purpose of the activity.
- Ask students to cite specific evidence: table values, bar lengths, differences between cells.
- Separate three levels of claims:
  - **observation**: directly visible in an output;
  - **interpretation**: a plausible explanation;
  - **implication**: a possible consideration for the manager.
- Watch for the phrase "similar players" when students describe older and younger players at the same rating. The evidence in section 9 shows the profiles are not similar, and catching this is a good in-class correction.
- Welcome limited and negative findings. The flat wage grid in section 10 is a result, not a failed chart.
- When a student says a pattern "makes sense," ask what else could produce the same pattern. That question is the module in miniature.

## Classroom adaptations

### 60 minute version

Use the full shared investigation through the evidence-based synthesis.

### 90 minute version

Let students do the independent analysis.

### 20 minute version

Use sections 4 and 5 alone. What a high rating is made of stands on its own and still delivers a surprise.

### Courses with more programming experience

Invite students to inspect `tool_library.py`, alter filters, or develop a new helper-function call. A natural extension is the analysis the notebook deliberately stops short of: holding age constant as well as rating, to test whether the apparent premium on pace is really a premium on youth. Preserve the question-driven structure even when code becomes more prominent.

### Courses emphasizing statistics

Section 8 can be extended into a discussion of why the "64 and under" band fails its check, and what band widths would fix it. The sensitivity of the conclusion to the chosen boundaries is a good short exercise.

## Assessment suggestions

A concise response can be assessed on whether it:

- states a clear question connected to the mission;
- cites appropriate evidence, including specific values;
- communicates a defensible insight;
- distinguishes evidence from interpretation;
- names what a proposed strategy gives up as well as what it gains;
- offers a cautious implication; and
- identifies a meaningful limitation or additional data need.

The solution guide's "Acceptable variation in responses" section lists these criteria in a form that can be used directly as a short rubric, and its "Result summation" section describes the difference between a strong and a weak version of the same recommendation.

## Data and interpretation cautions

- The ratings were assigned by the game's designers, not measured in a match. Conclusions apply to decisions inside the game.
- The file is a single-season snapshot. No player is followed over time, so nothing here describes what happens to an individual as they age.
- Older players appear in the file only if they were still good enough to remain in it. Any comparison across age is a comparison of survivors.
- Because `overall_rating` is itself computed from the attributes, holding it constant forces some trade-off to appear. The direction of the trade-off is the finding; the existence of one is partly built in.
- The "64 and under" rating band is much wider than the others and retains a rating difference across age groups, so results from that row deserve less weight.
- Nothing in the dataset links attributes to match outcomes. Claims about which squad would actually perform better go beyond the evidence.
- Associations and visible patterns do not establish causes.

## Relation to real-world analytics

The decision students practice here is a simplified version of one that professional clubs make continually: how to allocate a finite budget across players with different profiles, ages, and costs. Real recruitment departments work from match event data, tracking data, injury and contract histories, and league-adjusted performance models rather than from ratings assigned by a video game.

That gap is worth discussing explicitly. A productive question for class is what a club would need to collect in order to answer the question this dataset cannot: whether pace or positioning actually wins more matches. Students often assume such data must exist somewhere in a usable form, and the discussion of what it would take to assemble it is itself instructive.

The module is therefore best described to students as authentic in its reasoning and simplified in its evidence.

## Technical notes

The helper library relies on Python, pandas, NumPy, and Matplotlib. It contains the data preparation, grouping, filtering, and plotting used by the notebook.

Three details are worth knowing:

- `load_player_data(...)` removes goalkeepers and the `potential` column and adds the `age_group` and `rating_group` labels. Age groups are 23 and under, 24 to 28, and 29 and over; rating groups are 64 and under, 65 to 69, 70 to 74, and 75 and over.
- `summarize_grid(...)` shades each cell relative to the other cells **in its own row**, because the comparison that matters is reading across a row. A single scale across the whole grid would be dominated by the differences between rating groups and would hide the within-row pattern.
- `compare_attributes(...)` charts the difference between the first and last group and prints group sizes beneath the chart. The group sizes are worth pointing students toward when a difference looks large.
