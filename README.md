# LSAT PDF to CSV Converter

This tool converts LSAT exam result PDFs into structured CSV files for analysis and dashboarding in Power BI or other tools.

## 📁 Folder Structure
```
lsat_pdf_tool/
├── input/               # Drop your LSAT PDF files here
├── output/              # CSVs will be saved here
├── utils/
│   └── parser.py        # Core PDF parsing logic
├── main.py              # Main execution script
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## 📦 Installation
```bash
pip install -r requirements.txt
```

## 🚀 Usage
1. Place your LSAT PDF(s) into the `input/` folder.
2. Run the tool:
```bash
python main.py
```
3. Find the results in the `output/` folder:
   - `Exam_[n]_Questions.csv`
   - `Exam_[n]_Summary.csv`

## 📈 Dashboard Integration
The output files are ready for import into Power BI, allowing you to:
- Track accuracy by question type
- Visualize score improvements
- Analyze timing and difficulty trends

## 🛠 Future Improvements
- Web app with upload feature
- Auto-push to Power BI
- Flag detection

---

For questions or contributions, feel free to fork and submit a pull request!
