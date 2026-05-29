import os
import re

CONFIGS = {
    "Baseline (γ=10, τ=0.5, risk=2%, inf=2%)": "results_baseline",
    "Alt: log diffusion":                        "results_alt_log",
    "γ=5%":                                      "results_g5",
    "γ=20%":                                     "results_g20",
    "1% informed":                               "results_inf1",
    "8% informed":                               "results_inf8",
    "τ=0.30":                                    "results_t03",
    "τ=0.70":                                    "results_t07",
    "risk=1%":                                   "results_risk1",
    "risk=5%":                                   "results_risk5",
}

METRIC_PAIRS = [
    ("VPIN", "Assortativity (low frequency)"),
    ("VPIN", "Assortativity (high frequency)"),
    ("VPIN", "Bipartivity (low frequency)"),
    ("VPIN", "Bipartivity (high frequency)"),
    ("VPIN", "Number of connected components (low frequency)"),
    ("VPIN", "Number of connected components (high frequency)"),
    ("VPIN", "Maximal independent set size (low frequency)"),
    ("VPIN", "Maximal independent set size (high frequency)"),
    ("VPIN", "Number of stars (low frequency)"),
    ("VPIN", "Number of stars (high frequency)"),
    ("VPIN", "Diameter (low frequency)"),
    ("VPIN", "Diameter (high frequency)"),
    ("VPIN", "Closeness centrality (low frequency)"),
    ("VPIN", "Closeness centrality (high frequency)"),
    ("VPIN", "Betweenness centrality (low frequency)"),
    ("VPIN", "Betweenness centrality (high frequency)"),
    ("VPIN", "Easley's VPIN (low frequency)"),
    ("VPIN", "Easley's VPIN (high frequency)"),
]


def extract_correlations(stats_path):
    if not os.path.exists(stats_path):
        return None

    with open(stats_path, "r") as f:
        content = f.read()

    pattern = re.compile(
        r"Correlation between VPIN and (.+?):\s*([-\d.]+)"
    )

    results = {}
    for match in pattern.finditer(content):
        metric = match.group(1).strip()
        value  = float(match.group(2))
        if metric not in results:
            results[metric] = []
        results[metric].append(value)

    averaged = {k: sum(v) / len(v) for k, v in results.items()}
    return averaged


def rank_metrics(corr_dict):
    return sorted(corr_dict.keys(),
                  key=lambda k: abs(corr_dict[k]),
                  reverse=True)


def main():
    all_results = {}
    for label, folder in CONFIGS.items():
        stats_path = os.path.join(folder, "stats.txt")
        corrs = extract_correlations(stats_path)
        if corrs is None:
            print(f"WARNING: {stats_path} not found — skipping {label}")
            continue
        all_results[label] = corrs

    if not all_results:
        print("No results found. Check that all results folders exist.")
        return

    all_metrics = sorted(set(
        m for corrs in all_results.values() for m in corrs.keys()
    ))

    lines = []
    SEP  = "=" * 120
    SEP2 = "-" * 120

    lines.append(SEP)
    lines.append("SENSITIVITY ANALYSIS — CORRELATION COMPARISON TABLE")
    lines.append("Correlation between real VPIN and each network metric")
    lines.append(SEP)

    # Header
    col_label = 45
    col_val   = 10
    header = f"{'Metric':<{col_label}}"
    for label in all_results.keys():
        short = label[:col_val].strip()
        header += f" {short:>{col_val}}"
    lines.append(header)
    lines.append(SEP2)

    # One row per metric
    for metric in all_metrics:
        row = f"  {metric:<{col_label - 2}}"
        for label, corrs in all_results.items():
            val = corrs.get(metric, None)
            if val is not None:
                row += f" {val:>{col_val}.4f}"
            else:
                row += f" {'N/A':>{col_val}}"
        lines.append(row)

    lines.append(SEP2)

    # Ranking per configuration
    lines.append("\nMETRIC RANKING PER CONFIGURATION (by |correlation|, top 5):")
    lines.append(SEP2)
    for label, corrs in all_results.items():
        ranked = rank_metrics(corrs)[:5]
        lines.append(f"\n  {label}:")
        for i, m in enumerate(ranked):
            lines.append(f"    {i+1}. {m:<50} {corrs[m]:.4f}")

    lines.append("\n" + SEP)

    # Stability check vs baseline
    baseline_label = "Baseline (γ=10, τ=0.5, risk=2%, inf=2%)"
    if baseline_label in all_results:
        baseline_corrs = all_results[baseline_label]
        baseline_top3  = set(rank_metrics(baseline_corrs)[:3])

        lines.append("\nSTABILITY CHECK vs BASELINE (top-3 metrics match):")
        lines.append(SEP2)
        for label, corrs in all_results.items():
            if label == baseline_label:
                continue
            top3  = set(rank_metrics(corrs)[:3])
            match = top3 == baseline_top3
            lines.append(f"  {label:<50} Top-3 match: {'YES' if match else 'NO'}"
                         f"   cfg top-3: {top3}")

    lines.append("\n" + SEP)

    output = "\n".join(lines)
    print(output)

    with open("sensitivity_results.txt", "w") as f:
        f.write(output)
    print("\nSaved to sensitivity_results.txt")


if __name__ == "__main__":
    main()
