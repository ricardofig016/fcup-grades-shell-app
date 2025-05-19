import camelot
import pandas as pd
import argparse
import os


def main():
    parser = argparse.ArgumentParser(
        description="Extract numeric values from a specified column in tables from grades.pdf and store them in grades.csv."
    )
    parser.add_argument(
        "column",
        type=int,
        help="Column number (1-indexed) where numeric grades are located in the table(s).",
    )
    args = parser.parse_args()

    # Construct the path to grades.pdf
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(curr_dir) == "grades":
        curr_dir = os.path.join(curr_dir, "stats")
    pdf_path = os.path.join(curr_dir, "grades.pdf")

    # Read all tables from the PDF file
    try:
        tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")
    except Exception as e:
        print("Error reading PDF:", e)
        return

    if not tables:
        print("No tables found in the provided PDF.")
        return

    # Combine all extracted tables into one DataFrame
    all_tables = [table.df for table in tables if not table.df.empty]

    # Save all tables to a temporary file for debugging
    # temp_file_path = os.path.join(curr_dir, "temp_tables.txt")
    # with open(temp_file_path, "w", encoding="utf-8") as temp_file:
    #     for i, table in enumerate(all_tables, start=1):
    #         temp_file.write(f"Table {i}:\n")
    #         temp_file.write(table.to_string(index=False))
    #         temp_file.write("\n\n")

    if not all_tables:
        print("No valid table data extracted from PDF.")
        return

    combined_df = pd.concat(all_tables, ignore_index=True)

    if args.column < 0 or args.column >= combined_df.shape[1]:
        print(
            f"Error: Column {args.column} is out of range. The table has only {combined_df.shape[1]} columns."
        )
        return

    # Extract the specified column and filter numeric values only
    col_data = combined_df.iloc[:, args.column]
    col_data_str = col_data.astype(str).str.replace(",", ".").str.strip()
    numeric_values = pd.to_numeric(col_data_str, errors="coerce").fillna(0.0)

    if numeric_values.empty:
        print("No numeric values found in the specified column.")
        return

    # Save the numeric grades to a CSV file with one column named 'grades'
    output_df = pd.DataFrame(numeric_values)
    output_df.columns = ["grades"]
    csv_path = os.path.join(curr_dir, "grades.csv")
    output_df.to_csv(csv_path, index=False)
    print(f"Successfully extracted numeric grades to {csv_path}.")


if __name__ == "__main__":
    main()
