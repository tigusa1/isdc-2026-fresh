from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from fresh_model import simulate_fresh, sustainability_metrics

def main():
    ROOT = Path(__file__).resolve().parents[1]  # repo root
    out_dir = ROOT / "figures"
    out_dir.mkdir(exist_ok=True)

    # Figure 1: baseline trajectories
    df,_ = simulate_fresh(
        c_customer_owner=0.0,
        c_menu_interest=0.5,
        fresh_duration=1.0,
        restaurant_capacity_hf=8.0,
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(df["time"], df["Restaurant owner engagement"], label="Restaurant owner engagement")
    ax.plot(df["time"], df["HF Menu Items"], label="HF Menu Items")
    ax.plot(df["time"], df["Customer Interest in HF"], label="Customer Interest in HF")
    ax.axvline(1.0, linestyle="--", alpha=0.7, label="End of intervention")
    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Level")
    ax.set_title("Baseline FRESH model trajectory")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_dir / "baseline_trajectory.png", dpi=300)
    plt.close(fig)

    # Figure 2: tipping-point heatmap
    flag_HF_slope = True

    grid_n = 40
    x_vals = np.linspace(0, 1, grid_n)
    y_vals = np.linspace(0, 1, grid_n)
    Z = np.zeros((grid_n, grid_n))

    for iy, y in enumerate(y_vals):
        for ix, x in enumerate(x_vals):
            df2,_ = simulate_fresh(
                c_customer_owner=float(x),
                c_menu_interest=float(y),
                fresh_duration=1.0,
                restaurant_capacity_hf=8.0,
            )
            if flag_HF_slope:
                metrics = sustainability_metrics(df, restaurant_capacity_hf=8)
                Z[iy, ix] = metrics["HF slope"]
            else:
                Z[iy, ix] = df2["HF Menu Items"].iloc[-1]

    fig2, ax2 = plt.subplots(figsize=(7, 5.5))
    im = ax2.imshow(
        Z,
        origin="lower",
        aspect="auto",
        extent=[0, 1, 0, 1],
    )
    ax2.set_xlabel("C customer owner")
    ax2.set_ylabel("C menu interest")
    ax2.set_title("HF Menu Items at year 3")
    fig2.colorbar(im, ax=ax2)
    fig2.tight_layout()
    fig2.savefig(out_dir / "tipping_heatmap.png", dpi=300)
    plt.close(fig2)


if __name__ == "__main__":
    main()