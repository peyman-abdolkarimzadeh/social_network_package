# 📊 Social Network Package

A comprehensive Python toolkit for analyzing social or professional networks and generating individual PDF reports. Supports both command-line usage and standalone executable builds.

---

## 🔍 Repository Structure

```
social_network_package/
├── reports/                          # Report generation modules
├── visualizations/                   # Graph drawing tools
├── __init__.py
├── main.py                			  # CLI entry point
├── config.py               		  # Customizable settings
├── data_loader.py                    # Dynamic Excel data loader
├── network_builder.py                # Graph logic and analysis
├── run_social_report.py              # For PyInstaller builds
├── setup.cfg                         # Package metadata & entry points
├── pyproject.toml                    # Build-system configuration
├── requirements.txt                  # Direct dependencies
└── README.md                         # (This file)

```

---

## ⚙️ Features

- **📈 Data Import:** Dynamic Excel loading (single-sheet), no hard-coded paths.
- **🔧 Graph Construction:** Build directed/weighted graphs and detect mutual ties.
- **📐 Visuals:** Generate clear network diagrams.
- **📝 Reporting:** Personalized PDF reports for individuals.
- **🕹️ CLI Available:** Easily run with:
  ```
  social-report --file data.xlsx [--outdir /your/output/folder]
  ```
- **📦 Optional EXE Packaging:** Use `PyInstaller` to bundle into `social-report.exe`.

---

## ⚠️ Dependencies

- Python 3.10+
- pandas
- matplotlib
- networkx
- openpyxl
- python‑pptx

Install with:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Installation (Editable Mode)

```bash
pip install -e .
```

Ensures `social-report` becomes a valid CLI command from either:

```bash
social-report --file yourfile.xlsx
```

or as a module:

```bash
python -m social_network_package.main --file yourfile.xlsx
```

---

## 🖥️ Build as Standalone `.exe`

With **PyInstaller**:

```bash
pip install pyinstaller
pyinstaller --onefile run_social_report.py --name social-report
```

Then run:

```
dist/social-report.exe --file data.xlsx
```

---

## 🎯 Usage Flow

1. Provide the Excel file using `--file`.
2. CLI lists all names available.
3. Select a name by number.
4. Generates a PDF report in the specified output directory (defaults to Desktop).
