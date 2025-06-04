import fitz  # PyMuPDF
import re
import pandas as pd

def parse_lsat_pdf(file_path: str, exam_number: int):
    doc = fitz.open(file_path)
    page_texts = [doc[i].get_text() for i in range(len(doc))]
    overview = page_texts[0]

    # === Summary Info ===
    summary = {
        "Exam Number": exam_number,
        "Raw Score": None,
        "Scaled Score": None,
        "Total Time": None,
        "Section 1 Score": None,
        "Section 2 Score": None,
        "Section 3 Score": None,
        "Section 4 Score": None,
        "Variable Section": None
    }

    # Extract main stats
    summary["Total Time"] = re.search(r"Test Time: ([\dm\s]+)", overview).group(1)
    summary["Raw Score"] = re.search(r"Raw Score: (\d+/\d+)", overview).group(1)
    summary["Scaled Score"] = int(re.search(r"Scaled Score: (\d+)", overview).group(1))

    for i in range(1, 5):
        match = re.search(rf"Section {i}( \(\*\))?.*?Section Score: (\d+/\d+)", overview.replace("\n", " "))
        if match:
            summary[f"Section {i} Score"] = match.group(2)
            if match.group(1):
                summary["Variable Section"] = i

    # === Answer Keys ===
    answer_blocks = re.findall(r"# Response\n\n(.*?)\n\n", overview, re.DOTALL)
    answer_keys = [[line.split()[1] for line in block.strip().splitlines()] for block in answer_blocks]

    # === Questions ===
    question_rows = []

    for page_num in range(1, 5):
        section = page_num
        lines = page_texts[page_num].splitlines()
        answer_key = answer_keys[section - 1] if section - 1 < len(answer_keys) else []

        start_idx = 0
        for i, line in enumerate(lines):
            if line.strip().isdigit() and lines[i + 1].strip() in ["A", "B", "C", "D", "E"]:
                start_idx = i
                break
        lines = lines[start_idx:]

        for i in range(0, len(lines) - 4, 5):
            try:
                q_num = int(lines[i].strip())
                response = lines[i + 1].strip()
                subtype = lines[i + 2].strip()
                difficulty = lines[i + 3].strip()
                time_spent = lines[i + 4].strip()
                correct = 1 if (q_num <= len(answer_key) and response == answer_key[q_num - 1]) else 0

                question_rows.append({
                    "Exam Number": exam_number,
                    "Section": section,
                    "Question #": q_num,
                    "Subtype": subtype,
                    "Difficulty": difficulty,
                    "Time": time_spent,
                    "Flagged": False,
                    "Correct": correct,
                    "Variable Section": section == summary["Variable Section"]
                })
            except:
                continue

    questions_df = pd.DataFrame(question_rows)
    summary_df = pd.DataFrame([summary])
    return questions_df, summary_df
