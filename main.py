import os
import pandas as pd
from utils.parser import parse_lsat_pdf

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_exam_number(filename):
    name_part = os.path.splitext(filename)[0]
    digits = ''.join(filter(str.isdigit, name_part))
    return int(digits) if digits else 1

def main():
    pdf_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("No PDFs found in the input folder.")
        return

    for pdf_file in pdf_files:
        try:
            exam_number = get_exam_number(pdf_file)
            file_path = os.path.join(INPUT_FOLDER, pdf_file)

            print(f"Processing Exam {exam_number}: {pdf_file}")
            questions_df, summary_df = parse_lsat_pdf(file_path, exam_number)

            # Save outputs
            questions_df.to_csv(os.path.join(OUTPUT_FOLDER, f"Exam_{exam_number}_Questions.csv"), index=False)
            summary_df.to_csv(os.path.join(OUTPUT_FOLDER, f"Exam_{exam_number}_Summary.csv"), index=False)

            print(f"Saved Exam {exam_number} CSVs.\n")
        except Exception as e:
            print(f"Failed to process {pdf_file}: {e}")

if __name__ == "__main__":
    main()
