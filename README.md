# Document Register Scanner

A Python application for processing and comparing Excel document registers, generating weekly summaries, and tracking changes.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the application:
- Place Excel files in the `input` directory
- Configure settings in `config.py`

## Usage

1. Run the main script:
```bash
python main.py
```

2. The application will:
- Process new Excel files
- Compare with previous versions
- Generate weekly summaries
- Track changes

## Project Structure

- `main.py`: Main application entry point
- `config.py`: Configuration settings
- `processors/`: Excel file processing modules
- `comparators/`: Change detection modules
- `reporters/`: Summary and report generation
- `data/`: Processed data storage
- `reports/`: Generated reports and summaries 