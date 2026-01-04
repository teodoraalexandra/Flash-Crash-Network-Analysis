import numpy as np

def cusum_change(y):
    T = float(np.mean(y))
    dev = y - T
    S = np.cumsum(dev)
    return int(np.argmax(np.abs(S)))

def pettitt_test(y):
    n = y.size

    # ranks (average ranks for ties)
    ranks = np.argsort(np.argsort(y)) + 1
    ranks = ranks.astype(float)

    cum_ranks = np.cumsum(ranks)
    t = np.arange(1, n + 1, dtype=float)
    U = 2.0 * cum_ranks - t * (n + 1)

    return int(np.argmax(np.abs(U)))

def bai_perron_single_break(y, trim):
    n = y.size
    if not (0.0 < trim < 0.5):
        raise ValueError("trim must be in (0, 0.5).")

    h = int(np.floor(trim * n))
    grid = np.arange(h, n - h, dtype=int)  # candidate break positions

    ssr_path = np.empty(grid.size, dtype=float)
    mu1_path = np.empty_like(ssr_path)
    mu2_path = np.empty_like(ssr_path)

    for j, tau in enumerate(grid):
        seg1 = y[:tau + 1]
        seg2 = y[tau + 1:]

        mu1 = float(np.mean(seg1))
        mu2 = float(np.mean(seg2))

        ssr = float(np.sum((seg1 - mu1) ** 2) + np.sum((seg2 - mu2) ** 2))

        ssr_path[j] = ssr
        mu1_path[j] = mu1
        mu2_path[j] = mu2

    j_star = int(np.argmin(ssr_path))

    return int(grid[j_star])

def interpret(method, tau_y2, tau_y4):
    if tau_y2 < tau_y4:
        return f"{method}: Metric detects earlier (index {tau_y2} vs {tau_y4})."
    elif tau_y2 > tau_y4:
        return f"{method}: EASLEY detects earlier (index {tau_y4} vs {tau_y2})."
    else:
        return f"{method}: Both detect at the same index ({tau_y2})."
