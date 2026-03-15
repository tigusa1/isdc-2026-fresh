# FRESH System Dynamics Model

This repository contains the code and model files for a system dynamics analysis of the FRESH intervention, which aims to increase healthy food (HF) adoption in restaurants in low-income neighborhoods.

## Contents

- `vensim/` — Vensim PLE model with stock-and-flow graphics
- `fresh_model/` — core Python implementation of the model
- `streamlit_app/` — interactive Streamlit app for tipping-point exploration
- `scripts/` — reproducible figure-generation scripts
- `figures/` — output figures for the paper

## Main ideas

The model focuses on implementation and sustainability dynamics through three main stocks:

- Restaurant owner engagement
- HF menu items
- Customer interest in HF

The model explores whether reinforcing feedback between customer demand and restaurant behavior is strong enough to sustain HF adoption after the intervention ends.

## Installation

Clone the repository and install dependencies:

`pip install -r requirements.txt`

## File structure

```
fresh-system-dynamics-model/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── vensim/
│   └── fresh_model_v3b.mdl
├── fresh_model/
│   ├── __init__.py
│   └── model.py
├── streamlit_app/
│   └── app.py
├── scripts/
│   └── generate_figures.py
├── figures/
│   └── .gitkeep
└── notebooks/
    └── .gitkeep
```

This repository contains the simulation code for the system dynamics model used in:

Igusa et al. (2026) Modeling Healthy Food Adoption in Restaurants.

The model explores the implementation and sustainability dynamics of the FRESH intervention.

## Running the Streamlit App

Install dependencies:

`pip install -r requirements.txt`

Run the app:

`streamlit run app.py`

Generate the figures used in the figure

`python scripts/generate_figures.py`

## Tag the Version Used in the Paper

When the paper is submitted, tag the code version:

```
git tag paper-version
git push origin paper-version
```

## Repository contents used in the paper

- Vensim model: `vensim/fresh_model_v3b.mdl`
- Python model: `fresh_model/model.py`
- Streamlit interface: `streamlit_app/app.py`

## License

See LICENSE.

## Optional but Very Nice: Archive the Code with DOI

Before publication, you can connect the GitHub repo to Zenodo.

Zenodo will generate a DOI for the code, which journals and conferences like.

Workflow:

`GitHub repo → Zenodo integration → DOI`

## Very Helpful for Reviewers

Include:

`example_heatmap.png`

or similar outputs in the repo so reviewers can quickly see results without running the code.


## A Tip for Streamlit Apps

Add this file:

`.streamlit/config.toml`

Example:

```
[server]
headless = true
```

This avoids some deployment issues.

## Optional: Share a Live Demo

You can deploy the Streamlit app online using **Streamlit Community Cloud.

Then readers can interact with the tipping-point explorer directly.

## Suggested Citation Block

If you use this code, please cite:

Igusa, T. et al. (2026). System dynamics modeling of healthy food adoption in restaurants.

## Recommendation for your paper

Mention something like:

The simulation code and Streamlit visualization tool used in this study are publicly available on GitHub.

## Notes

`notebook/`

short notebook showing:
- baseline simulation
- tipping-point heatmap