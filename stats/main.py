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


def print_and_plot_stats(df, my_grade=0.0):
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
    parser = argparse.ArgumentParser(
        description="Process grades from a PDF file or use an existing CSV file."
    )
    parser.add_argument(
        "--csv",
        type=str,
        help="Provide a CSV file name to skip PDF processing.",
        default=None,
    )
    parser.add_argument(
        "pdf_file_name",
        nargs="?",
        help="PDF file name to process (required if --csv is not used).",
    )
    parser.add_argument(
        "column_number",
        nargs="?",
        type=int,
        help="Column index (0-based) to extract grades from (required if --csv is not used).",
    )
    parser.add_argument(
        "my_grade", type=float, help="Your grade to highlight in the plots."
    )
    parser.add_argument("max_grade", type=float, help="The maximum possible grade.")
    args = parser.parse_args()

    data_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(data_dir) == "grades":
        data_dir = os.path.join(data_dir, "stats")
    data_dir = os.path.join(data_dir, "data")
    if not os.path.exists(data_dir):
        print(f"Error: Directory {data_dir} does not exist.")
        sys.exit(1)

    if args.csv:
        csv_file_name = args.csv
    else:
        if args.pdf_file_name is None or args.column_number is None:
            parser.error(
                "For PDF processing, both pdf_file_name and column_number are required."
            )
        pdf_to_csv(data_dir, args.pdf_file_name, args.column_number)
        csv_file_name = args.pdf_file_name.replace(".pdf", ".csv")

    grades_path = os.path.join(data_dir, csv_file_name)
    df = pd.read_csv(grades_path)

    print("General stats:")
    print_and_plot_stats(df, my_grade=args.my_grade)

    print("\nStats for grades >= 10%:")
    print_and_plot_stats(
        df[df["grades"] * 100 / args.max_grade >= 10], my_grade=args.my_grade
    )

    print("\nStats for grades >= 45%:")
    print_and_plot_stats(
        df[df["grades"] * 100 / args.max_grade >= 45], my_grade=args.my_grade
    )

    print("\nOrdered Unique Grades (highest to lowest):")
    unique_counts = df.value_counts().sort_index(ascending=False)
    for grade, count in unique_counts.items():
        entry_label = "entry" if count == 1 else "entries"
        print(f"{grade} ({count} {entry_label})")
