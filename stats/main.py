import camelot
import argparse
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


def pdf_to_csv(data_dir, file_name, column):
    pdf_file_path = os.path.join(data_dir, file_name)

    # Read all tables from the PDF file
    try:
        tables = camelot.read_pdf(pdf_file_path, pages="all", flavor="stream")
    except Exception as e:
        print("Error reading PDF:", e)
        return

    if not tables:
        print("No tables found in the provided PDF.")
        return

    # Combine all extracted tables into one DataFrame
    all_tables = [table.df for table in tables if not table.df.empty]

    if not all_tables:
        print("No valid table data extracted from PDF.")
        return

    combined_df = pd.concat(all_tables, ignore_index=True)

    if column < 0 or column >= combined_df.shape[1]:
        print(
            f"Error: Column {column} is out of range. The table has only {combined_df.shape[1]} columns."
        )
        return

    # Extract the specified column and filter numeric values only
    col_data = combined_df.iloc[:, column]
    col_data_str = col_data.astype(str).str.replace(",", ".").str.strip()
    numeric_values = pd.to_numeric(col_data_str, errors="coerce").fillna(0.0)

    if numeric_values.empty:
        print("No numeric values found in the specified column.")
        return

    # Save the numeric grades to a CSV file with one column named 'grades'
    output_df = pd.DataFrame(numeric_values)
    output_df.columns = ["grades"]
    csv_file_path = os.path.join(data_dir, file_name.replace(".pdf", ".csv"))
    output_df.to_csv(csv_file_path, index=False)
    print(f"Successfully extracted numeric grades to {csv_file_path}.")


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
        my_grade,
        color="red",
        linestyle="dashed",
        linewidth=2,
        label=f"my grade ({my_grade})",
    )
    plt.title("Grades Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Frequency")
    plt.legend()

    # Boxplot subplot
    plt.subplot(1, 2, 2)
    plt.boxplot(grades.dropna(), vert=False)
    plt.axvline(
        my_grade,
        color="red",
        linestyle="dashed",
        linewidth=2,
        label=f"my grade ({my_grade})",
    )
    plt.title("Grades Boxplot")
    plt.xlabel("Grade")
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            "Usage: > python main.py <pdf_file_name> <column_number> <my_grade> <max_grade>"
        )
        print(
            "\tpdf_file_name: The name of the PDF file to process, stored in data/ directory."
        )
        print(
            "\tcolumn_number: The index of the column to extract grades from (0-based)."
        )
        print("\tmy_grade: Your grade to be highlighted in the plots.")
        print("\tmax_grade: The maximum possible grade.")
        print("Example: > python main.py test1.pdf 2 11.95 20")
        sys.exit(1)

    pdf_file_name = sys.argv[1]
    column_number = int(sys.argv[2])
    my_grade = float(sys.argv[3])
    max_grade = float(sys.argv[4])

    data_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(data_dir) == "grades":
        data_dir = os.path.join(data_dir, "stats")
    data_dir = os.path.join(data_dir, "data")
    if not os.path.exists(data_dir):
        print(f"Error: Directory {data_dir} does not exist.")
        sys.exit(1)

    pdf_to_csv(data_dir, pdf_file_name, column_number)

    csv_file_name = pdf_file_name.replace(".pdf", ".csv")
    grades_path = os.path.join(data_dir, csv_file_name)
    df = pd.read_csv(grades_path)

    print("General stats:")
    print_and_plot_stats(df)

    print("\nStats for grades >= 10%:")
    print_and_plot_stats(df[df["grades"] * 100 / max_grade >= 10])

    print("\nStats for grades >= 45%:")
    print_and_plot_stats(df[df["grades"] * 100 / max_grade >= 45])

    print("\nOrdered Unique Grades (highest to lowest):")
    unique_counts = df.value_counts().sort_index(ascending=False)
    for grade, count in unique_counts.items():
        entry_label = "entry" if count == 1 else "entries"
        print(f"{grade} ({count} {entry_label})")
