# Public Modules

This repository contains the learning modules published on the **Data Science CROSSROADS** website.

Each top-level folder represents a separate learning module. A module may contain the following files and directories:

```text
module-name/
├── module_metadata.yml
├── module_guide.md
├── activity_guide.md
├── activity_interactive_python.ipynb
├── activity_interactive_r.ipynb
├── activity_web.html
├── data/
├── images/
└── additional supporting files
```

## Module files

### `module_metadata.yml`

Contains the module metadata used to validate, organize, and publish the module.

Important metadata fields include:

* the module slug and title;
* primary and secondary disciplines;
* intended audience and estimated completion time;
* skills and learning goals;
* dataset information;
* available activity formats;
* files included in the public download;
* catalog and website display settings.

At minimum, a module must define the following fields to be included in the generated discipline catalog:

```yaml
slug: example-module
title: Example Module
primary_disciplines:
  - Data Science
```

Modules with missing or invalid required fields may be omitted from the generated website navigation.

### `module_guide.md`

Contains the main instructional content for the module and serves as its primary landing page.

### `activity_guide.md`

Provides instructions for completing the module activity, including the motivating questions, analysis process, and expected outcomes.

### `activity_interactive_python.ipynb`

Contains the interactive Python version of the activity.

### `activity_interactive_r.ipynb`

Contains the interactive R version of the activity when one is available.

### `activity_web.html`

Contains a browser-based version of the activity when one is available.

### `data/`

Contains datasets and other files required by the module activities, such as CSV or JSON files.

### `images/`

Contains figures, diagrams, screenshots, and other media used by the module.

## Website generation

The Data Science CROSSROADS website reads the metadata from each module and automatically generates:

* discipline-specific module pages;
* folders for each primary discipline;
* the hierarchical MyST table of contents;
* the public module catalog;
* links to interactive notebooks and web activities;
* downloadable module resources.

A module assigned to multiple primary disciplines appears under each corresponding discipline in the website navigation.

For example:

```yaml
primary_disciplines:
  - Computer Science
  - Data Science
```

generates entries similar to:

```text
disciplines/
├── computer-science/
│   └── example-module.md
└── data-science/
    └── example-module.md
```

## Deployment

Changes pushed to the `main` branch automatically trigger a rebuild and deployment of the **Data Science CROSSROADS** website.
