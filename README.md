# FRESH System Dynamics Model

This repository contains the code and model files for a system dynamics analysis of the FRESH intervention, which aims to increase healthy food (HF) adoption in restaurants in low-income neighborhoods.

## Quick Start

To run the interactive model exploration tool:

```
git clone https://github.com/tigusa1/isdc-2026-fresh
cd ISDC-2026-FRESH
python -m venv venv
source venv/bin/activate
pip install -e .
pip install -r requirements.txt
python -m streamlit run streamlit_app/app.py
```

The Streamlit interface allows interactive exploration of the system dynamics model and visualizes tipping-point behavior in healthy food adoption.

## Contents

- `vensim/` — Vensim PLE model with stock-and-flow graphics
- `fresh_model/` — core Python implementation of the model
- `streamlit_app/` — interactive Streamlit app for tipping-point exploration
- `scripts/` — reproducible figure-generation scripts
- `figures/` — output figures for the paper

## Architecture

The repository separates the reusable simulation model from the user interface:

- `fresh_model` contains the core simulation logic
- `streamlit_app` provides an interactive interface for exploring model behavior

The model can therefore be used independently for scripts, notebooks, or other analyses.

## Main ideas

The model focuses on implementation and sustainability dynamics through three main stocks:

- Restaurant owner engagement
- HF menu items
- Customer interest in HF

The model explores whether reinforcing feedback between customer demand and restaurant
behavior is strong enough to sustain HF adoption after the intervention ends.

The Python implementation reproduces the structure of the Vensim model and allows
systematic parameter exploration and visualization of tipping-point behavior.

## Installation

Clone the repository and install dependencies:

```
git clone https://github.com/tigusa1/isdc-2026-fresh
cd ISDC-2026-FRESH
python -m venv venv
source venv/bin/activate
# Register the repository as an editable Python package
# so `fresh_model` can be imported by the Streamlit app.
pip install -e .
pip install -r requirements.txt
python -m streamlit run streamlit_app/app.py
```

## File structure

```
ISDC-2026-FRESH/
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

Run the app:

`python -m streamlit run streamlit_app/app.py`

Generate the figures used in the paper:

`python scripts/generate_figures.py`

The Streamlit interface allows interactive exploration of key parameters and visualizes
regions where reinforcing feedback produces sustained adoption of healthy food items.

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

`notebooks/`

short notebook showing:
- baseline simulation
- tipping-point heatmap

## Suggested additions later

Once this is working, the next useful files would be:
- scripts/generate_phase_diagram.py
- scripts/validate_against_vensim.py
- notebooks/explore_tipping_points.ipynb
