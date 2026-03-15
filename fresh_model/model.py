import numpy as np
import pandas as pd

def simulate_fresh(
    final_time=3.0,
    dt=0.02,
    fresh_duration=1.0,
    max_restaurant_capacity=10.0,
    restaurant_capacity_hf=8.0,
    c_increasing_engagement=0.5,
    c_decreasing=0.8,
    c_customer_owner=0.0,
    c_owner_menu=0.25,
    c_depletion=0.8,
    c_owner_community=0.5,
    c_community_interest=0.5,
    c_menu_interest=0.5,
    c_decay=1.5,
    e0=0.0,
    h0=0.0,
    i0=0.0,
):
    """
    Euler simulation of the FRESH 3-stock model.

    Stocks:
        E = Restaurant owner engagement
        H = HF Menu Items
        I = Customer Interest in HF
    """

    n_steps = int(final_time / dt) + 1
    t = np.linspace(0.0, final_time, n_steps)

    E = np.zeros(n_steps)
    H = np.zeros(n_steps)
    I = np.zeros(n_steps)

    E[0] = e0
    H[0] = h0
    I[0] = i0

    for k in range(n_steps - 1):
        intervention_off = 1.0 if t[k] >= fresh_duration else 0.0

        community_exposure = c_owner_community * E[k]

        increasing_interest = (
            (
                c_community_interest * max_restaurant_capacity * community_exposure
                + c_menu_interest
            )
            * H[k]
            * (1.0 - I[k])
        )

        decaying_interest = c_decay * I[k]

        menu_addition = (
            c_owner_menu
            * (max_restaurant_capacity ** 2)
            * E[k]
            * (restaurant_capacity_hf - H[k])
        )

        menu_depletion = c_depletion * max_restaurant_capacity * H[k]

        increasing_engagement = (
            c_customer_owner * I[k] * (1.0 - E[k])
            + c_increasing_engagement * (1.0 - intervention_off)
        )

        decreasing_engagement = c_decreasing * E[k]

        dE = increasing_engagement - decreasing_engagement
        dH = menu_addition - menu_depletion
        dI = increasing_interest - decaying_interest

        E[k + 1] = np.clip(E[k] + dt * dE, 0.0, 1.0)
        H[k + 1] = np.clip(E[k] * 0 + H[k] + dt * dH, 0.0, restaurant_capacity_hf)
        I[k + 1] = np.clip(I[k] + dt * dI, 0.0, 1.0)

    return pd.DataFrame(
        {
            "time": t,
            "Restaurant owner engagement": E,
            "HF Menu Items": H,
            "Customer Interest in HF": I,
        }
    )


def summarize_run(df: pd.DataFrame, restaurant_capacity_hf: float) -> dict:
    final_h = float(df["HF Menu Items"].iloc[-1])
    final_e = float(df["Restaurant owner engagement"].iloc[-1])
    final_i = float(df["Customer Interest in HF"].iloc[-1])

    sustainability_score = final_h / max(restaurant_capacity_hf, 1e-9)

    n = len(df)
    tail = max(5, n // 4)
    slope = np.polyfit(df["time"].iloc[-tail:], df["HF Menu Items"].iloc[-tail:], 1)[0]

    return {
        "HF Menu Items final": final_h,
        "Restaurant owner engagement final": final_e,
        "Customer Interest final": final_i,
        "HF sustainability score": sustainability_score,
        "HF Menu slope (tail)": slope,
    }
