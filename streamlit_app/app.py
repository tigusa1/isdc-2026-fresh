import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fresh_model.model import simulate_fresh, sustainability_metrics

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="FRESH tipping point explorer", layout="wide")

st.title("FRESH tipping point explorer")

# --------------------------------------------------
# Sidebar: fixed parameters
# --------------------------------------------------

st.sidebar.header("Model constants")

fresh_duration = st.sidebar.slider("FRESH duration", 0.0, 2.0, 1.0, 0.25)
final_time = st.sidebar.slider("Final time", 2.0, 5.0, 3.0, 0.5)
restaurant_capacity_hf = st.sidebar.slider("Restaurant capacity for HF", 0.0, 10.0, 8.0, 1.0)
# dt = st.sidebar.select_slider("Time step", options=[0.01, 0.02, 0.05], value=0.02)
dt = 0.02

c_increasing_engagement = st.sidebar.slider("Owner increasing engagement", 0.0, 1.0, 0.3, 0.05)
c_decreasing = st.sidebar.slider("Owner decreasing engagement", 0.0, 1.5, 0.8, 0.05)
c_owner_menu = st.sidebar.slider("Owner engagement -> menu", 0.0, 1.0, 0.2, 0.05)
c_depletion = st.sidebar.slider("Menu depletion", 0.0, 1.5, 0.6, 0.05)
c_owner_community = st.sidebar.slider("Owner -> community", 0.0, 1.0, 0.5, 0.05)
c_community_interest = st.sidebar.slider("Community interest -> consumer", 0.0, 1.0, 0.3, 0.05)
c_decay = st.sidebar.slider("Consumer interest decay", 0.0, 2.5, 0.6, 0.05)
max_restaurant_capacity = st.sidebar.slider("Max restaurant capacity", 10.0, 20.0, 10.0, 1.0)
# grid_n = st.sidebar.slider("Grid size", 10, 50, 25, 5)
grid_n = 25

# --------------------------------------------------
# Heatmap settings
# --------------------------------------------------
# two column groups
group1, group2 = st.columns(2)

with group1:
    st.subheader("Tipping-point heatmap")
    col_a, col_b = st.columns(2)

with group2:
    st.subheader("Selected point on heatmap")
    col_c, col_d = st.columns(2)

heatmap_metric = col_a.selectbox(
    "Heatmap metric",
    ["HF slope", "HF Menu Items final"]
    # ["HF slope", "HF Menu Items final", "HF sustainability score"]
)

# classification_threshold = col_b.slider(
#     "Sustained threshold for HF Menu Items",
#     0.0,
#     float(max(restaurant_capacity_hf, 0.5)),
#     2.0,
#     0.5
# )

x_lbl = "Customer - owner interaction"
y_lbl = "Menu - customer interest interaction"

selected_x = col_c.slider( x_lbl, 0.0, 1.0, 0.05, 0.05 )
selected_y = col_d.slider( y_lbl, 0.0, 1.0, 0.5, 0.05 )

# --------------------------------------------------
# Compute heatmap grid
# --------------------------------------------------
x_vals = np.linspace(0.0, 1.0, grid_n)
y_vals = np.linspace(0.0, 1.0, grid_n)

Z = np.zeros((grid_n, grid_n))

for iy, y in enumerate(y_vals):
    for ix, x in enumerate(x_vals):
        df_tmp = simulate_fresh(
            final_time=final_time,
            dt=dt,
            fresh_duration=fresh_duration,
            max_restaurant_capacity=max_restaurant_capacity,
            restaurant_capacity_hf=restaurant_capacity_hf,
            c_increasing_engagement=c_increasing_engagement,
            c_decreasing=c_decreasing,
            c_customer_owner=float(x),
            c_owner_menu=c_owner_menu,
            c_depletion=c_depletion,
            c_owner_community=c_owner_community,
            c_community_interest=c_community_interest,
            c_menu_interest=float(y),
            c_decay=c_decay,
        )

        metrics_tmp = sustainability_metrics(df_tmp, restaurant_capacity_hf)

        if heatmap_metric == "HF Menu Items final":
            Z[iy, ix] = metrics_tmp["HF Menu Items final"]

        elif heatmap_metric == "HF sustainability score":
            Z[iy, ix] = metrics_tmp["HF sustainability score"]

        else:
            Z[iy, ix] = metrics_tmp["HF slope"]

Z = np.nan_to_num(Z)

# --------------------------------------------------
# Static heatmap with selected point
# --------------------------------------------------
fig_hm, ax_hm = plt.subplots(figsize=(7, 5.5))
im = ax_hm.imshow(
    Z,
    origin="lower",
    extent=[x_vals.min(), x_vals.max(), y_vals.min(), y_vals.max()],
    aspect="auto"
)
ax_hm.scatter(
    selected_x,
    selected_y,
    color="red",
    marker="x",
    s=140,
    linewidths=2
)
ax_hm.set_xlabel(x_lbl)
ax_hm.set_ylabel(y_lbl)
ax_hm.set_title(f"Heatmap of {heatmap_metric}")
fig_hm.colorbar(im, ax=ax_hm)
st.pyplot(fig_hm)

# --------------------------------------------------
# Run simulation at selected point
# --------------------------------------------------
df = simulate_fresh(
    final_time=final_time,
    dt=dt,
    fresh_duration=fresh_duration,
    max_restaurant_capacity=max_restaurant_capacity,
    restaurant_capacity_hf=restaurant_capacity_hf,
    c_increasing_engagement=c_increasing_engagement,
    c_decreasing=c_decreasing,
    c_customer_owner=selected_x,
    c_owner_menu=c_owner_menu,
    c_depletion=c_depletion,
    c_owner_community=c_owner_community,
    c_community_interest=c_community_interest,
    c_menu_interest=selected_y,
    c_decay=c_decay,
)

metrics = sustainability_metrics(df, restaurant_capacity_hf)

# --------------------------------------------------
# Plot trajectories
# --------------------------------------------------
fig_ts, ax1_ts = plt.subplots(figsize=(8, 4.8))
ax1_ts.plot(df["time"], df["Restaurant owner engagement"], label="Restaurant owner engagement", color="black")
ax1_ts.plot(df["time"], df["Customer Interest in HF"], label="Customer Interest in HF", color="blue")
ax2_ts = ax1_ts.twinx()  # Instantiate a second axes that shares the same x-axis
color2 = 'green'
ax2_ts.set_ylabel("HF Menu Items", color=color2)
ax2_ts.plot(df["time"], df["HF Menu Items"], label="HF Menu Items", linestyle="dashed",
            color=color2)
ax2_ts.tick_params(axis='y', labelcolor=color2)
ax2_ts.tick_params(axis='y', colors=color2)
ax2_ts.axvline(fresh_duration, linestyle=":", alpha=0.7, label="End of intervention")
ax1_ts.set_xlabel("Time (years)")
ax1_ts.set_ylabel("Interest, Engagement")
ax1_ts.set_title(
    f"Trajectory for selected point: "
    f"C customer owner={selected_x:.2f}, "
    f"C menu interest={selected_y:.2f}"
)
# ax1_ts.legend()
h1, l1 = ax1_ts.get_legend_handles_labels()
h2, l2 = ax2_ts.get_legend_handles_labels()
ax1_ts.legend(h1 + h2, l1 + l2, loc='upper left')
ax1_ts.grid(True)
st.pyplot(fig_ts)

# --------------------------------------------------
# Display summary metrics
# --------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("HF Menu Items (final)", f"{metrics['HF Menu Items final']:.2f}")
c2.metric("Engagement (final)", f"{metrics['Restaurant owner engagement final']:.2f}")
c3.metric("Interest (final)", f"{metrics['Customer Interest final']:.2f}")
c4.metric("HF slope", f"{metrics['HF slope']:.3f}")

# --------------------------------------------------
# Binary sustainability map
# --------------------------------------------------
# st.subheader("Binary sustainability map")
#
# if heatmap_metric == "HF Menu Items final":
#
#     Z_binary = (Z > classification_threshold).astype(int)
#
#     fig_bin, ax_bin = plt.subplots(figsize=(7, 5.5))
#
#     im2 = ax_bin.imshow(
#         Z_binary,
#         origin="lower",
#         extent=[x_vals.min(), x_vals.max(), y_vals.min(), y_vals.max()],
#         aspect="auto",
#         vmin=0,
#         vmax=1
#     )
#
#     ax_bin.scatter(
#         selected_x,
#         selected_y,
#         color="red",
#         marker="x",
#         s=140,
#         linewidths=2
#     )
#
#     ax_bin.set_xlabel("C customer owner")
#     ax_bin.set_ylabel("C menu interest")
#     ax_bin.set_title("Binary sustainability region")
#
#     fig_bin.colorbar(im2, ax=ax_bin)
#
#     st.pyplot(fig_bin)