import pandas as pd
import matplotlib.pyplot as plt
import os


MY_GRADE = 11.95
MAX_GRADE = 20


def print_and_plot_stats(df):
    grades = df["grades"]
    print("\tCount:", grades.count())
    print("\tMean:", grades.mean())
    print("\tMedian:", grades.median())
    print("\tMin:", grades.min())
    print("\tMax:", grades.max())
    print("\tStandard Deviation:", grades.std())
    print("\tVariance:", grades.var())
    print("\t25th Percentile:", grades.quantile(0.25))
    print("\t50th Percentile:", grades.quantile(0.50))
    print("\t75th Percentile:", grades.quantile(0.75))

    plt.figure(figsize=(12, 5))

    # Histogram subplot
    plt.subplot(1, 2, 1)
    plt.hist(grades.dropna(), bins=10, edgecolor="black")
    plt.axvline(
        MY_GRADE, color="red", linestyle="dashed", linewidth=2, label="MY_GRADE"
    )
    plt.title("Grades Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Frequency")
    plt.legend()

    # Boxplot subplot
    plt.subplot(1, 2, 2)
    plt.boxplot(grades.dropna(), vert=False)
    plt.axvline(
        MY_GRADE, color="red", linestyle="dashed", linewidth=2, label="MY_GRADE"
    )
    plt.title("Grades Boxplot")
    plt.xlabel("Grade")
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(curr_dir) == "grades":
        curr_dir = os.path.join(curr_dir, "stats")
    grades_path = os.path.join(curr_dir, "grades.csv")
    df = pd.read_csv(grades_path)

    print("General stats:")
    print_and_plot_stats(df)

    print("\nStats for grades >= 10%:")
    print_and_plot_stats(df[df["grades"] * 100 / MAX_GRADE >= 10])

    print("\nStats for grades >= 45%:")
    print_and_plot_stats(df[df["grades"] * 100 / MAX_GRADE >= 45])

    print("\nOrdered Unique Grades (highest to lowest):")
    unique_counts = df.value_counts().sort_index(ascending=False)
    for grade, count in unique_counts.items():
        entry_label = "entry" if count == 1 else "entries"
        print(f"{grade} ({count} {entry_label})")
