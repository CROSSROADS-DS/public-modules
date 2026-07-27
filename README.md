# Public Modules

This repository contains the learning content used by the Data Science CROSSROADS website.

Each top-level folder in this repository represents a separate learning module and may contain the following structure:

```text
module-name/
├── README.md
├── metadata.yml
├── notebooks/
├── data/
└── images/
```

* `README.md` contains the module’s main content and serves as its landing page.
* `metadata.yml` contains module-specific metadata and configuration.
* `notebooks/` contains Jupyter notebooks associated with the module.
* `data/` contains supporting files, such as CSV datasets.
* `images/` contains figures, diagrams, and other media used by the module.

Changes pushed to the `main` branch of this repository automatically trigger a rebuild and deployment of the Data Science CROSSROADS website.
