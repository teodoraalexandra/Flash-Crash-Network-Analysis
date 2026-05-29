import multiprocessing
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plots.independent.computeMetrics import compute_metrics
from plots.independent.processFile import Price


DIVISORS = [50, 100, 150, 200, 300, 500, 700, 1000]
METRIC_NAMES = [
    "Assortativity",
    "Bipartivity",
    "Number of connected components",
    "Number of stars",
    "Diameter",
    "Maximal independent set size",
    "Closeness centrality",
    "Betweenness centrality",
    "Easley's VPIN",
]

HIGHLIGHTED_DIVISORS = [50, 700]   # low frequency, high frequency
WINDOW_SIZE = 40
TRIM_FRACTION = 0.10

def create_price_object(row):
    p = Price()
    p.price = row[row._fields.index("price")]
    p.quantity = row[row._fields.index("quty")]
    p.direction = row[row._fields.index("dirTrigger")]
    p.first_agent = row[row._fields.index("AgTrigger")]
    p.second_agent = row[row._fields.index("ag2")]
    p.best_ask = row[row._fields.index("bestask")]
    p.best_bid = row[row._fields.index("bestbid")]
    return p


def read_prices_in_chunk(chunk):
    return [create_price_object(row) for row in chunk.itertuples()]


def task(sim_index, bucket_size, tag, results_dict, list_lock):
    """For one simulation tape and one bucket size, compute the per-bucket
    time series of (VPIN, Easley VPIN, network metrics) and store the result
    in results_dict[(sim_index, bucket_size)].
    """
    csv_path = f"plots/csvs/prices{sim_index + 1}{tag}.csv"
    if not os.path.exists(csv_path):
        print(f"WARNING: {csv_path} not found — skipping sim {sim_index}, "
              f"bucket {bucket_size}")
        return

    vpin_series       = []
    evpin_series      = []
    assort_series     = []
    bipart_series     = []
    conn_series       = []
    stars_series      = []
    diam_series       = []
    indep_series      = []
    close_series      = []
    between_series    = []

    with pd.read_csv(csv_path, chunksize=bucket_size, delimiter=";") as reader:
        for chunk in reader:
            price_array = read_prices_in_chunk(chunk)
            if len(price_array) != bucket_size:
                continue   # drop the final short bucket

            (vpin, evpin, _price, assort, bipart, _avg_clust,
             conn, stars, diam, indep, close, between) = compute_metrics(
                price_array, 0
            )

            vpin_series.append(vpin)
            evpin_series.append(evpin)
            assort_series.append(assort)
            bipart_series.append(bipart)
            conn_series.append(conn)
            stars_series.append(stars)
            diam_series.append(diam)
            indep_series.append(indep)
            close_series.append(close)
            between_series.append(between)

    with list_lock:
        results_dict[(sim_index, bucket_size)] = {
            "VPIN":                            vpin_series,
            "Assortativity":                   assort_series,
            "Bipartivity":                     bipart_series,
            "Number of connected components":  conn_series,
            "Number of stars":                 stars_series,
            "Diameter":                        diam_series,
            "Maximal independent set size":    indep_series,
            "Closeness centrality":            close_series,
            "Betweenness centrality":          between_series,
            "Easley's VPIN":                   evpin_series,
        }


def mean_with_padding(list_of_lists):
    if len(list_of_lists) == 0:
        return np.array([])
    max_len = max(len(row) for row in list_of_lists)
    if max_len == 0:
        return np.array([])
    mask = np.array([row + [np.nan] * (max_len - len(row))
                     for row in list_of_lists], dtype=float)
    return np.nanmean(mask, axis=0)


def rolling_correlation(y1, y2, window_size):
    df = pd.DataFrame({"Y1": y1, "Y2": y2})
    corr = df["Y1"].rolling(window=window_size).corr(df["Y2"])
    corr = corr.replace([np.inf, -np.inf], np.nan).dropna()
    if len(corr) == 0:
        return np.nan
    return corr.mean()


def trim(arr, frac):
    n = len(arr)
    k = int(frac * n)
    if k == 0 or 2 * k >= n:
        return arr
    return arr[k:-k]


def get_total_rows(tag, n_simulations):
    for i in range(n_simulations):
        path = f"plots/csvs/prices{i + 1}{tag}.csv"
        if os.path.exists(path):
            with open(path, "r") as f:
                return sum(1 for _ in f)
    raise FileNotFoundError(
        f"No prices*{tag}.csv files found under plots/csvs/"
    )


def plot_heatmap(corr_table, bucket_sizes, highlighted, out_path):
    def peak_abs(m):
        finite = [abs(v) for v in corr_table[m] if not np.isnan(v)]
        return max(finite) if finite else 0.0

    metric_order = sorted(METRIC_NAMES, key=peak_abs, reverse=True)

    matrix = np.array([corr_table[m] for m in metric_order], dtype=float)
    masked = np.ma.masked_invalid(matrix)

    fig, ax = plt.subplots(figsize=(11, 6))
    cmap = plt.get_cmap("coolwarm").copy()
    cmap.set_bad(color="lightgray")

    vmax = 1.0
    im = ax.imshow(
        masked, aspect="auto", cmap=cmap,
        vmin=-vmax, vmax=vmax, interpolation="nearest",
    )

    ax.set_xticks(range(len(bucket_sizes)))
    ax.set_xticklabels(bucket_sizes, rotation=45, ha="right")
    ax.set_yticks(range(len(metric_order)))
    ax.set_yticklabels(metric_order)

    ax.set_xlabel("Bucket size (trades per bucket)")
    ax.set_title("Correlation between real VPIN and network metrics, "
                 "by bucket size")

    for j, b in enumerate(bucket_sizes):
        if b in highlighted:
            ax.axvline(j, color="black", lw=1.5, linestyle="--", alpha=0.7)

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            v = matrix[i, j]
            if np.isnan(v):
                ax.text(j, i, "N/A", ha="center", va="center",
                        fontsize=7, color="dimgray")
            else:
                ax.text(
                    j, i, f"{v:.2f}",
                    ha="center", va="center",
                    fontsize=7,
                    color="black" if abs(v) < 0.6 else "white",
                )

    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Correlation with real VPIN")

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved heatmap to {out_path}")


def write_text_table(corr_table, bucket_sizes, total_rows, divisors, out_path):
    sep_w = 10 + 14 * len(bucket_sizes)
    SEP   = "=" * sep_w
    SEP2  = "-" * sep_w

    lines = []
    lines.append(SEP)
    lines.append("BUCKET-SIZE SENSITIVITY")
    lines.append("Correlation between real VPIN and each network metric, "
                 "as a function of bucket size.")
    lines.append(f"Total trade-tape length: {total_rows} rows")
    lines.append(SEP)

    header = f"{'Metric':<35}"
    for b, d in zip(bucket_sizes, divisors):
        tag = f"k={d}({b})"
        header += f" {tag:>12}"
    lines.append(header)
    lines.append(SEP2)

    def peak_abs(m):
        finite = [abs(v) for v in corr_table[m] if not np.isnan(v)]
        return max(finite) if finite else 0.0

    metric_order = sorted(METRIC_NAMES, key=peak_abs, reverse=True)

    for metric in metric_order:
        row = f"{metric:<35}"
        for c in corr_table[metric]:
            if np.isnan(c):
                row += f" {'N/A':>12}"
            else:
                row += f" {c:>12.4f}"
        lines.append(row)

    lines.append(SEP2)
    lines.append("Notes:")
    lines.append("  - k = divisor, bucket_size = total_rows / k")
    lines.append(SEP)

    text = "\n".join(lines)
    with open(out_path, "w") as f:
        f.write(text)
    print(text)
    print(f"\nSaved text table to {out_path}")


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 bucket_sensitivity.py "
              "<n_simulations> <tag> <days>")
        sys.exit(1)

    n_simulations = int(sys.argv[1])
    tag           = sys.argv[2]
    _days         = int(sys.argv[3])

    os.makedirs("results", exist_ok=True)

    total_rows = get_total_rows(tag, n_simulations)
    bucket_sizes = [max(1, total_rows // d) for d in DIVISORS]
    highlighted  = [max(1, total_rows // d) for d in HIGHLIGHTED_DIVISORS]

    print(f"Total rows in trade tape: {total_rows}")
    print(f"Bucket-size grid (k -> bucket): "
          f"{list(zip(DIVISORS, bucket_sizes))}")
    print(f"Running {n_simulations} simulations x "
          f"{len(bucket_sizes)} bucket sizes "
          f"= {n_simulations * len(bucket_sizes)} tasks\n")

    manager = multiprocessing.Manager()
    results_dict = manager.dict()
    lock = manager.Lock()

    processes = []
    for sim_index in range(n_simulations):
        for bucket_size in bucket_sizes:
            p = multiprocessing.Process(
                target=task,
                args=(sim_index, bucket_size, tag, results_dict, lock),
            )
            processes.append(p)

    cap = max(1, multiprocessing.cpu_count())
    running = []
    for p in processes:
        if len(running) >= cap:
            running.pop(0).join()
        p.start()
        running.append(p)
    for p in running:
        p.join()

    print("All tasks complete. Aggregating...\n")

    corr_table = {m: [] for m in METRIC_NAMES}

    for bucket_size in bucket_sizes:
        per_metric = {m: [] for m in METRIC_NAMES + ["VPIN"]}
        for sim_index in range(n_simulations):
            key = (sim_index, bucket_size)
            if key not in results_dict:
                continue
            for m, series in results_dict[key].items():
                per_metric[m].append(series)

        avg_vpin = mean_with_padding(per_metric["VPIN"])
        avg_vpin = trim(avg_vpin, TRIM_FRACTION)

        for metric in METRIC_NAMES:
            avg_m = mean_with_padding(per_metric[metric])
            avg_m = trim(avg_m, TRIM_FRACTION)

            if metric == "Easley's VPIN" and len(avg_m) > 0:
                lo, hi = np.nanmin(avg_m), np.nanmax(avg_m)
                if hi > lo:
                    avg_m = (avg_m - lo) / (hi - lo)

            n = min(len(avg_vpin), len(avg_m))
            if n < WINDOW_SIZE:
                corr_table[metric].append(np.nan)
                continue

            c = rolling_correlation(
                avg_vpin[:n], avg_m[:n], window_size=WINDOW_SIZE
            )
            corr_table[metric].append(c)

    write_text_table(
        corr_table, bucket_sizes, total_rows, DIVISORS,
        "results/bucket_sensitivity.txt",
    )
    plot_heatmap(
        corr_table, bucket_sizes, highlighted,
        "results/bucket_sensitivity_heatmap.png",
    )


if __name__ == "__main__":
    main()
