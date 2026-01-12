# Salesforce Org Analysis Kit

Automated Salesforce org analysis framework for merger/acquisition due diligence. Uses AI + metadata extraction to identify technical debt, automation conflicts, and migration blockers.

## Features
- **Data Inventory**: Catalog record counts and field usage statistics.
- **Metadata Analysis**: Identify "ghost metadata" (unused fields), hard-coded IDs, and automation complexity.
- **Security Audit**: Analyze profiles, permission sets, and sharing models.
- **Process Mapping**: Visualize sales and delivery processes based on record types and stages.
- **Migration Risk Assessment**: Flag validation rules, cross-object formulas, and dependencies that block migration.

## Prerequisites
- **Salesforce CLI (sf)**: [Install here](https://developer.salesforce.com/tools/salesforcecli)
- **Python 3.x**: [Install here](https://www.python.org/downloads/)
- **Git**: [Install here](https://git-scm.com/)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/designthynk/salesforce-org-analysis-kit.git
   cd salesforce-org-analysis-kit
   ```

2. **Run the Setup Script**:
   Initialize the project for your target org alias.
   ```bash
   ./setup.sh [ORG_ALIAS]
   # Example: ./setup.sh my-org-prod
   ```
   This will:
   - Create the necessary directory structure (`force-app`, `scripts/data`).
   - Install Python dependencies from `requirements.txt`.
   - create a custom export script for your org.

## Workflow

### 1. Retrieve Metadata
Retrieve the org's metadata to analyze structure and customization.
```bash
sf project retrieve start --manifest templates/package.xml --target-org [ORG_ALIAS] --output-dir force-app/[ORG_ALIAS]
```

### 2. Export Data & Statistics
Modify the generated export script in `scripts/` if needed, then run it to get data samples and field usage stats.
```bash
python scripts/export_[ORG_ALIAS].py
```

### 3. AI-Driven Analysis
Use the prompts in `docs/PROMPTS.md` with an AI assistant (like ChatGPT, Claude, or Cursor) to generate analysis reports.

**Process:**
1.  **Setup**: Use **Prompt 0** to orient the AI with the project context (`docs/ai-instructions.md`).
2.  **Tasks**: Run prompts sequentially (Task 1 to Task 5) to generate specific reports in `outputs/`.
    -   Task 1: Data Summary
    -   Task 1.5: Security Analysis
    -   Task 2: Data Model & Process
    -   Task 3: Automation & Validation
    -   Task 4: Tech Debt & Integrations
    -   Task 5: Final Comprehensive Report

## Project Structure
```text
.
├── docs/
│   ├── PROMPTS.md          # Copy/Paste prompts for AI analysis
│   └── ai-instructions.md  # Context for the AI assistant
├── templates/
│   ├── export_data.py      # Template for data export script
│   ├── extract_metadata.py # Helper to parse XML metadata
│   └── package.xml         # Manifest for retrieving metadata
├── setup.sh                # Project initialization script
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## License
See [LICENSE](LICENSE) file.
