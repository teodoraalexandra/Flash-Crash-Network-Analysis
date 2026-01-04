import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss, zivot_andrews
from hampel import hampel
import warnings


def hampel_filter(series):
    data = pd.Series(series)
    result = hampel(data, window_size=3, n_sigma=3.0)
    return result.filtered_data

def run_stationarity_tests(series):
    warnings.filterwarnings(
        "ignore",
        message=".*outside of the range of p-values available.*"
    )
    x = pd.Series(series).dropna().astype(float)

    # ADF (null: unit root)
    adf_stat, adf_p, adf_lags, adf_nobs, adf_crit, adf_icbest = adfuller(x, autolag='AIC')
    adf_res = {
        'stat': adf_stat, 'pvalue': adf_p, 'lags': adf_lags, 'nobs': adf_nobs,
        'crit': adf_crit, 'icbest': adf_icbest
    }

    # KPSS level (null: level-stationary)
    kpss_L_stat, kpss_L_p, kpss_L_lags, kpss_L_crit = kpss(x, regression="c", nlags='auto')
    kpss_L_res = {'stat': kpss_L_stat, 'pvalue': kpss_L_p, 'lags': kpss_L_lags, 'crit': kpss_L_crit}

    # Zivot-Andrews (null: unit root with single endogenous break)
    za_stat, za_p, za_crit, za_lags, za_bpidx = zivot_andrews(x, regression="ct", trim=0.15, autolag="AIC")
    za_res = {'stat': za_stat, 'pvalue': za_p, 'crit': za_crit, 'lags': za_lags, 'break_index': int(za_bpidx)}

    return {'ADF': adf_res, 'KPSS_L': kpss_L_res, 'ZA': za_res}

def interpret_stationarity(results, alpha):
    adf_p = results['ADF']['pvalue']
    kpssL_p = results['KPSS_L']['pvalue']
    za_p = results['ZA']['pvalue']

    # Primary rule: ADF rejects unit root AND KPSS does not reject level-stationarity
    if (adf_p < alpha) and (kpssL_p >= alpha):
        return "Treat as stationary"

    # Prioritize ZA: rejection suggests piecewise/trend-stationary with a break
    if za_p < alpha:
        return "Treat as stationary (Piecewise/trend-stationary with break)"

    # Otherwise, classic contradictory case: ADF fails and KPSS rejects
    if (adf_p >= alpha) and (kpssL_p < alpha):
        return "Treat as non-stationary"

    # Fallback
    return "Treat as non-stationary"

