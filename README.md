# Public Modules

This repository contains the learning content used by the Data Science CROSSROADS website.

Each folder inside `public_modules/` represents one module and may include:

```text
public_modules/
└── module-name/
    ├── README.md
    ├── metadata.yml
    ├── notebooks/
    ├── data/
    └── images/
```

* `README.md` is the module’s main page.
* `notebooks/` contains Jupyter notebooks.
* `data/` contains supporting files such as CSV datasets.
* `metadata.yml` contains module-specific metadata.
* `images/` contains figures and other media.

Changes pushed to `public_modules/` automatically trigger a rebuild and deployment of the CROSSROADS website.
