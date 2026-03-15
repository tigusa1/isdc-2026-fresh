import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from fresh_model import simulate_fresh, summarize_run


st.set_page_config(page_title="FRESH tipping point explorer", layout="wide")

st.title("FRESH tipping point explorer")

st.sidebar.header("Selected trajectory")
c_customer_owner = st.sidebar.slider("C customer owner", 0.0, 1.0, 0.0, 0.05)
c_menu_interest = st.sidebar.slider("C menu interest", 0.0, 1.0, 0.5, 0.05)
fresh_duration = st.sidebar.slider("FRESH duration", 0.0, 3.0, 1.0, 0.25)

restaurant_capacity_hf = st.sidebar.slider("Restaurant capacity for HF", 0.0, 10.0, 8.0, 1.0)

df = simulate_fresh(
    c_customer_owner=c_customer_owner,
    c_menu_interest=c_menu_interest,
    fresh_duration=fresh_duration,
    restaurant_capacity_hf=restaurant_capacity_hf,
)

metrics = summarize_run(df, restaurant_capacity_hf)

c1, c2, c3, c4 = st.columns(4)
c1.metric("HF Menu Items (final)", f"{metrics['HF Menu Items final']:.2f}")
c2.metric("Engagement (final)", f"{metrics['Restaurant owner engagement final']:.2f}")
c3.metric("Interest (final)", f"{metrics['Customer Interest final']:.2f}")
c4.metric("Sustainability score", f"{metrics['HF sustainability score']:.2f}")

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(df["time"], df["Restaurant owner engagement"], label="Restaurant owner engagement")
ax.plot(df["time"], df["HF Menu Items"], label="HF Menu Items")
ax.plot(df["time"], df["Customer Interest in HF"], label="Customer Interest in HF")
ax.axvline(fresh_duration, linestyle="--", alpha=0.7, label="End of intervention")
ax.set_xlabel("Time (years)")
ax.set_ylabel("Level")
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)


st.subheader("2D heatmap")

grid_n = st.slider("Grid size", 10, 50, 25, 5)

x_vals = np.linspace(0, 1, grid_n)
y_vals = np.linspace(0, 1, grid_n)
Z = np.zeros((grid_n, grid_n))

for iy, y in enumerate(y_vals):
    for ix, x in enumerate(x_vals):
        df2 = simulate_fresh(
            c_customer_owner=float(x),
            c_menu_interest=float(y),
            fresh_duration=fresh_duration,
            restaurant_capacity_hf=restaurant_capacity_hf,
        )
        Z[iy, ix] = df2["HF Menu Items"].iloc[-1]

fig2, ax2 = plt.subplots(figsize=(7, 5))
im = ax2.imshow(
    Z,
    origin="lower",
    aspect="auto",
    extent=[0, 1, 0, 1],
)
ax2.set_xlabel("C customer owner")
ax2.set_ylabel("C menu interest")
ax2.set_title("HF Menu Items at final time")
fig2.colorbar(im, ax=ax2)
st.pyplot(fig2)

