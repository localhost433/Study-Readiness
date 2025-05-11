import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_logs(log_file='study_readiness_log.csv', n_sessions=5):
    """
    Plot a radar chart for the last N sessions from the log file.
    """
    if not os.path.exists(log_file):
        print(f"Log file not found: {log_file}")
        return

    df = pd.read_csv(log_file, encoding='utf-8-sig')
    if 'timestamp' not in df.columns:
        print("Missing header: please fix log file.")
        return

    # Select the last N sessions
    df = df.tail(n_sessions)
    metrics = ['T_arith', 'E_arith', 'RT', 'stroop', 'two_back', 'word_pair', 'KSS', 'sleep_q', 'stress']
    available_metrics = [metric for metric in metrics if metric in df.columns]

    if not available_metrics:
        print("No valid metrics found in the log file to plot.")
        return

    values = df[available_metrics].values

    # Normalize values (0–1) based on historical data
    normalized = (values - values.min(axis=0)) / (values.ptp(axis=0) + 1e-5)

    # Prepare radar chart angles
    angles = np.linspace(0, 2 * np.pi, len(available_metrics), endpoint=False).tolist()
    angles += angles[:1]  # close the loop

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for i, row in enumerate(normalized):
        data = row.tolist()
        data += data[:1]  # close the loop
        ax.plot(angles, data, label=f"Session {len(df) - i}", linewidth=2)
        ax.fill(angles, data, alpha=0.25)

    # Configure chart labels and title
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(available_metrics, fontsize=10)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=8)
    ax.set_title("Study Readiness Radar", fontsize=16, pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), title="Sessions")
    plt.tight_layout()
    plt.show()