import math
import numpy as np
import pandas as pd

# Tablicowe stałe dla m=3
D2_BY_M = {3: 1.693}
D4_BY_M = {3: 2.574}
K1_BY_M = {3: 0.5908}  # EV = k1 * Rbar

def average_range_method(df: pd.DataFrame, lsl: float | None, usl: float | None):
    # df: [sample_index, series_index, operator_name, value]
    m = int(df['series_index'].max())
    if m not in D2_BY_M:
        raise ValueError(f"Metoda Range wspiera tu m=3 (otrzymano m={m}).")

    d2 = D2_BY_M[m]
    D4 = D4_BY_M[m]
    k1 = K1_BY_M[m]

    grp = df.groupby(['operator_name','sample_index'])['value']
    means = grp.mean()
    ranges = grp.max() - grp.min()

    Rbar_by_op = ranges.groupby('operator_name').mean()
    Rbar = Rbar_by_op.mean()

    EV = k1 * Rbar

    xbar_by_part = df.groupby('sample_index')['value'].mean()
    R_parts = xbar_by_part.max() - xbar_by_part.min()

    xbar_by_op = df.groupby('operator_name')['value'].mean()
    R_ops = xbar_by_op.max() - xbar_by_op.min()

    k2 = 0.523  # aproksymacja dla m=3
    AV = k2 * math.sqrt(max(R_ops**2 - EV**2, 0.0))

    GRR = math.sqrt(EV**2 + AV**2)
    PV = (R_parts / 5.15)  # klasyczny przelicznik AIAG

    TV = math.sqrt(GRR**2 + PV**2)

    pct_EV = 100 * EV / TV if TV > 0 else np.nan
    pct_AV = 100 * AV / TV if TV > 0 else np.nan
    pct_GRR = 100 * GRR / TV if TV > 0 else np.nan
    pct_PV = 100 * PV / TV if TV > 0 else np.nan

    UCL_R_by_op = {op: D4 * rbar for op, rbar in Rbar_by_op.items()}
    D_diff = float(R_ops)

    pct_GRR_tol = pct_EV_tol = pct_AV_tol = np.nan
    if lsl is not None and usl is not None and (usl - lsl) > 0:
        tol = float(usl - lsl)
        pct_GRR_tol = 100 * (6 * GRR) / tol
        pct_EV_tol = 100 * (6 * EV) / tol
        pct_AV_tol = 100 * (6 * AV) / tol

    components = [
        {"Metric": "Rbar (global)", "Value": float(Rbar)},
        {"Metric": "EV", "Value": float(EV), "%StudyVar": pct_EV, "%Tolerance (6σ)": pct_EV_tol},
        {"Metric": "AV", "Value": float(AV), "%StudyVar": pct_AV, "%Tolerance (6σ)": pct_AV_tol},
        {"Metric": "GRR", "Value": float(GRR), "%StudyVar": pct_GRR, "%Tolerance (6σ)": pct_GRR_tol},
        {"Metric": "PV", "Value": float(PV), "%StudyVar": pct_PV},
        {"Metric": "TV", "Value": float(TV)},
        {"Metric": "D diff (ops)", "Value": float(D_diff)},
        *[{"Metric": f"UCL_R ({op})", "Value": float(u)} for op, u in UCL_R_by_op.items()],
    ]

    return {
        "summary": {
            "Rbar": float(Rbar),
            "%GRR": pct_GRR,
            "%PV": pct_PV,
        },
        "range_table": components,
    }
