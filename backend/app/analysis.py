import numpy as np
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

def analyze_grr_crossed(df: pd.DataFrame, lsl: float | None, usl: float | None):
    df = df.copy()
    df["Part"] = df["sample_index"].astype(str)
    df["Operator"] = df["operator_name"].astype(str)
    df["Trial"] = df["series_index"].astype(int)
    df["Measurement"] = df["value"].astype(float)

    df["Part"] = df["Part"].astype("category")
    df["Operator"] = df["Operator"].astype("category")

    model = ols("Measurement ~ C(Part) + C(Operator) + C(Part):C(Operator)", data=df).fit()
    anova = anova_lm(model, typ=2)

    n_parts = df["Part"].nunique()
    n_ops = df["Operator"].nunique()
    r = df.groupby(["Part", "Operator"])['Measurement'].count().mean()

    MS_part = anova.loc["C(Part)", "mean_sq"] if "C(Part)" in anova.index else np.nan
    MS_op   = anova.loc["C(Operator)", "mean_sq"] if "C(Operator)" in anova.index else np.nan
    MS_pxo  = anova.loc["C(Part):C(Operator)", "mean_sq"] if "C(Part):C(Operator)" in anova.index else np.nan
    MS_e    = anova.loc["Residual", "mean_sq"] if "Residual" in anova.index else np.nan

    var_repeat = max(MS_e, 0.0)
    var_pxo = max((MS_pxo - MS_e) / r, 0.0)
    var_op = max((MS_op - MS_pxo) / (n_parts * r), 0.0)
    var_part = max((MS_part - MS_pxo) / (n_ops * r), 0.0)

    var_grr = var_repeat + var_pxo + var_op
    var_total = var_grr + var_part

    sd_repeat = np.sqrt(var_repeat)
    sd_pxo = np.sqrt(var_pxo)
    sd_op = np.sqrt(var_op)
    sd_grr = np.sqrt(var_grr)
    sd_part = np.sqrt(var_part)
    sd_total = np.sqrt(var_total)

    pct_repeat = 100 * sd_repeat / sd_total if sd_total > 0 else np.nan
    pct_pxo = 100 * sd_pxo / sd_total if sd_total > 0 else np.nan
    pct_op = 100 * sd_op / sd_total if sd_total > 0 else np.nan
    pct_grr = 100 * sd_grr / sd_total if sd_total > 0 else np.nan
    pct_pv = 100 * sd_part / sd_total if sd_total > 0 else np.nan

    ndc = 1.41 * (sd_part / sd_grr) if sd_grr > 0 else np.nan

    pct_grr_tol = pct_repeat_tol = np.nan
    if lsl is not None and usl is not None and (usl - lsl) > 0:
        tol = float(usl - lsl)
        pct_grr_tol = 100.0 * (6 * sd_grr) / tol
        pct_repeat_tol = 100.0 * (6 * sd_repeat) / tol

    components = pd.DataFrame({
        "Component": [
            "Repeatability (Equipment)",
            "Reproducibility – Operator",
            "Reproducibility – Part*Operator",
            "GRR (Total)",
            "Part-to-Part",
            "Total",
        ],
        "Variance": [var_repeat, var_op, var_pxo, var_grr, var_part, var_total],
        "SD": [sd_repeat, sd_op, sd_pxo, sd_grr, sd_part, sd_total],
        "%StudyVar": [pct_repeat, pct_op, pct_pxo, pct_grr, pct_pv, 100.0],
        "%Tolerance (6σ)": [pct_repeat_tol, np.nan, np.nan, pct_grr_tol, np.nan, np.nan],
    })

    anova_json = (
        anova.reset_index()
             .rename(columns={"index": "Source"})
             .to_dict(orient="records")
    )

    summary = {
        "Parts": int(n_parts),
        "Operators": int(n_ops),
        "Replicates (avg)": float(r),
        "%GRR": float(pct_grr) if not np.isnan(pct_grr) else None,
        "%PV": float(pct_pv) if not np.isnan(pct_pv) else None,
        "ndc": float(ndc) if not np.isnan(ndc) else None,
    }

    return {
        "summary": summary,
        "anova": anova_json,
        "components": components.to_dict(orient="records"),
    }
