from pathlib import Path

import matplotlib.pyplot as plt


RESULTS_DIR = Path(__file__).resolve().parent / "results"


def load_results(directory):
    """Return (m + n, CPU time in ms, memory in KB) for each result file."""
    data = []
    if not directory.is_dir():
        return data

    for filepath in directory.glob("*.txt"):
        fields = filepath.read_text().split()
        if len(fields) != 5:
            raise ValueError(f"{filepath}: expected cost, two strings, time, memory")

        _, string1, string2, time, memory = fields
        problem_size = len(string1.replace("_", "")) + len(string2.replace("_", ""))
        data.append((problem_size, float(time), float(memory)))

    return sorted(data)


def plot_metric(basic_data, hybrid_data, column, ylabel):
    plt.figure()
    for label, data in (("Basic", basic_data), ("Hybrid", hybrid_data)):
        if data:
            plt.plot(
                [point[0] for point in data],
                [point[column] for point in data],
                marker="o",
                label=label,
            )

    plt.xlabel("Problem Size (m + n)")
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()


def main():
    basic_data = load_results(RESULTS_DIR / "basic")
    hybrid_data = load_results(RESULTS_DIR / "hybrid")

    plot_metric(basic_data, hybrid_data, 1, "CPU Time (ms)")
    plot_metric(basic_data, hybrid_data, 2, "Memory Usage (KB)")
    plt.show()


if __name__ == "__main__":
    main()
