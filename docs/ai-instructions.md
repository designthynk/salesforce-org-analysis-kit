# Salesforce Org Analysis - AI Instructions

## PROJECT GOAL
Analyze Salesforce orgs to prepare for consolidation. Document technical implementation, identify conflicts, assess migration complexity.

## CONTEXT
- **Project:** Org Consolidation and Analysis
- **Source Orgs:** [INSERT_SOURCE_ORG_NAME]
- **Target Org:** [INSERT_TARGET_ORG_NAME]
- **Business:** [INSERT_BUSINESS_DESCRIPTION]
- **Key Custom Objects:** [INSERT_KEY_OBJECTS]

## HOW THIS WORKS
You'll complete 5 tasks per org. Each task produces a specific markdown file. Refer to `PROMPTS.md` for the specific prompt for each task.

## YOUR RULES

### 1. Evidence & Facts
-   **Ground everything in evidence**: Cite actual file names, object names, field names.
-   **No Name-Guessing**: Do NOT infer an object's purpose solely from its API name if the description is empty.
-   **State assumptions explicitly**: If you must infer, label it clearly as an assumption.

### 2. Data Interpretation
-   **The Unknown Rule**: If a field has metadata but **0% population** in the data (and 0 automation references), mark it as **"Ghost Metadata"**.
-   **Evidence-Only Mapping**: Every recommendation (Keep/Retire) must cite statistics from `field_stats.csv`.

### 3. Consolidation Focus
-   **Focus on consolidation impact**: Always answer "what does this mean for the merger?"
-   **Namespace Detection**: Treat fields with managed package namespaces (e.g., `SBQQ__`, `npsp__`) as **Read-Only Dependencies**, not custom debt to be deleted.
-   **Prioritize by impact**: Flag issues that block data migration (e.g., validation rules, mandatory fields).

### 4. Security & Risk
-   **Hard-Coded Alert**: You MUST explicitly flag any 15 or 18-character Salesforce IDs (Regex: `00[a-zA-Z0-9]{13,16}`) found in `ApexClass`, `ApexTrigger`, or `Flow` metadata. This is a High Risk finding.

## OUTPUT FORMATTING
-   Clear markdown headings
-   Tables for structured data
-   **Bold** critical findings
-   Bullet points only for lists
-   Keep it actionable

## WHAT TO DO IF...
-   **Metadata missing:** Note it, analyze what you have, add to "Questions & Assumptions"
-   **Data inconsistent:** Document it, state your interpretation, flag for validation
-   **Ambiguous:** State assumption, explain reasoning, provide alternatives if relevant
-   **Complex automation:** Break down step-by-step, focus on migration-relevant details

## SUCCESS =
Technical teams can plan migration AND business stakeholders understand risks.
