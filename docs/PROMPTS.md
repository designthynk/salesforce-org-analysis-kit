# Salesforce Org Analysis Prompts

Copy and paste these prompts to your AI assistant to drive the analysis workflow.

**IMPORTANT:** Before running these prompts, do a Find & Replace in your text editor:
-   Find: `[INSERT_ORG_NAME]` -> Replace with your actual Org Name (e.g., "NorthStar")
-   Find: `[ORG_ALIAS]` -> Replace with your SFDX alias (e.g., "ns-prod")

---

## PROMPT 0: Setup & Context
**Use this first to orient the AI.**

```text
I am starting a new Salesforce Org Analysis project.
I have copied the 'starter-kit' into my root directory.

Please read:
1. `README.md` (for the workflow)
2. `docs/ai-instructions.md` (for your role and rules)
3. `templates/` (files available to us)

My goal is to analyze the org: [INSERT_ORG_NAME]

First, help me verify I have the right project structure. Do I have a 'force-app' folder and a 'scripts/data' folder? If not, help me create them.
```

---

## PROMPT 0.5: Generate Data Export Script
**Use this after retrieving metadata (Step 1 in README).**

```text
I have retrieved the metadata for my org into `force-app/[ORG_ALIAS]`.

Please look at the `templates/export_data.py` file.
I need you to create a custom script `scripts/export_[ORG_ALIAS].py` for me.

CRITICAL:
1. Read the `Account` and `Opportunity` object metadata in `force-app/[ORG_ALIAS]/objects` to see which fields ACTUALLY exist.
2. Update the `TIER_1_OBJECTS` and `TIER_2_OBJECTS` queries in the python script to ONLY include fields that exist in my metadata. Do NOT include fields that are not in the XML.
3. Set the `TARGET_ORG_ALIAS` to '[ORG_ALIAS]'.
4. Save the new script to `scripts/export_[ORG_ALIAS].py`.
```

---

## PROMPT 1: Task 1 - Data Summary
**Use this after running the export script.**

```text
Task 1: [INSERT_ORG_NAME] Data Summary
Summary
Count and catalog what we have. Verify data completeness and produce summary statistics.

Context
Read `docs/ai-instructions.md` for full project context
This is TASK 1 for [INSERT_ORG_NAME] org
Inputs
- `scripts/data/[ORG_ALIAS]/*.csv` (Raw data files)
- `scripts/data/[ORG_ALIAS]/field_stats.csv` (Field population statistics)
- Metadata XML files (objects, flows, layouts, workflows, etc.) in `force-app/[ORG_ALIAS]`

Steps
1. Count and list all CSV files with record counts
2. Review `field_stats.csv` to identify overall data health (e.g., empty tables)
3. Count metadata components:
   - Custom objects
   - Flows (Active vs Inactive)
   - Workflow Rules
   - Validation Rules
   - Apex Classes & Triggers
   - Sharing Rules (to assess security model complexity)
4. Flag any missing expected files or suspicious gaps

Deliverable
Create file: `outputs/[INSERT_ORG_NAME]_data_summary.md`

Use this structure:

# [INSERT_ORG_NAME] Org - Data Summary

## Data Files Received
| File Name | Record Count | Date Range |
|-----------|--------------|------------|
| Account.csv | X | ... |
| ... | ... | ... |

## Metadata Components
- Custom Objects: X
- Active Flows: X
- Apex Classes: X
- Validation Rules: X
- Sharing Rules: X

## Data Health (from field_stats.csv)
- **Empty Tables:** [List objects with 0 records]
- **Low Usage:** [List objects with <10 records]

## Initial Observations
- [Missing files]
- [Data quality concerns]

Acceptance Criteria
- [ ] All CSV files counted
- [ ] Metadata counts include Apex, Flows, and Sharing Rules
- [ ] Empty tables identified explicitly using field_stats.csv

tags: [ORG_ALIAS], task-1, data-inventory
```

---

## PROMPT 1.5: Security Model Analysis
**Use this after Task 1.**

```text
Task 1.5: [INSERT_ORG_NAME] Security Model Analysis
Summary
Analyze Profiles, Permission Sets, and Sharing settings to understand access control complexity.

Context
Read `docs/ai-instructions.md` for full project context
This is TASK 1.5 for [INSERT_ORG_NAME] org
Inputs
- Profiles and PermissionSets metadata
- SharingRules metadata
- Object metadata (for OWD/SharingModel)

Steps
1. **Profile Breakdown**:
   - List all custom profiles.
   - Count users assigned to each profile (if User export data is available).
2. **Permission Set Analysis**:
   - List Permission Sets and their primary function (e.g., "CPQ Admin", "Read Only").
3. **Sharing Model**:
   - Check `Account` and `Opportunity` sharingModel (Private, ReadWrite, etc.) in Object metadata.
   - List Sharing Rules by object.
4. **Field Level Security (FLS)**:
   - Identify profiles with overly broad modify all data or view all data permissions.

Deliverable
Create file: `outputs/[INSERT_ORG_NAME]_security_analysis.md`

Use this structure:

# [INSERT_ORG_NAME] Org - Security Analysis

## Organization-Wide Defaults (OWD)
| Object | Internal Sharing | External Sharing |
|--------|------------------|------------------|
| Account | Private | Private |
| ... | ... | ... |

## Profile Analysis
| Profile Name | User Count | Key Permissions |
|--------------|------------|-----------------|
| Sales User | 150 | ... |

## Sharing Rules Complexity
- **Account:** 5 Criteria-based rules, 2 Owner-based rules
- **Opportunity:** ...

tags: [ORG_ALIAS], task-1.5, security
```

---

## PROMPT 2: Task 2 - Data Model & Process Map
**Use this after Task 1.**

```text
Task 2: [INSERT_ORG_NAME] Data Model & Process Map
Summary
Map objects, fields, and relationships. Document the sales and delivery process.

Context
Read `docs/ai-instructions.md` for project context
This is TASK 2 for [INSERT_ORG_NAME] org
Builds on Task 1 output
Inputs
- All [INSERT_ORG_NAME] object metadata XML files
- `scripts/data/[ORG_ALIAS]/field_stats.csv` (Crucial for Field Analysis)
- `outputs/[INSERT_ORG_NAME]_data_summary.md`
- RecordTypes and GlobalValueSets metadata

Steps
1. Create object inventory (standard + custom)
2. Map object relationships (Master-Detail, Lookup)
3. Analyze fields using `field_stats.csv`:
   - Identify "Ghost Metadata" (Fields that exist in XML but have 0% population)
4. Check `RecordType` folder for business process variations (e.g., "Enterprise" vs "SMB").
5. Map sales & delivery process (LeadStatus, StageName)

Deliverable
Create file: `outputs/[INSERT_ORG_NAME]_data_model_and_process.md`

Use this structure:

# [INSERT_ORG_NAME] Org - Data Model & Process Map

## Object Inventory
...

## Field Analysis (Field Vitality)
**Ghost Metadata (0% Population):**
- Account: [List fields]
- Opportunity: [List fields]

**Field Population Summary:**
| Object | Field | Populated % |
|--------|-------|-------------|
| Account | Industry | 85% |
| ... | ... | ... |

## Record Types & Processes
- **Account Record Types:** [List found types]
- **Opportunity Record Types:** [List found types]

## Sales & Delivery Process Map
...

tags: [ORG_ALIAS], task-2, data-model
```

---

## PROMPT 2.5: CPQ & Billing Analysis (Optional)
**Use this if the org uses Salesforce CPQ or Billing.**

```text
Task 2.5: [INSERT_ORG_NAME] CPQ & Billing Analysis
Summary
Analyze SBQQ configuration and Quote-to-Cash automation dependencies.

Context
Read `docs/ai-instructions.md` for full project context
This is TASK 2.5 for [INSERT_ORG_NAME] org
Inputs
- InstalledPackages (to confirm CPQ/SBQQ version)
- Objects: `SBQQ__Quote__c`, `SBQQ__QuoteLine__c`, `Product2`, `Pricebook2`
- Automation on CPQ objects

Steps
1. **Configuration Analysis**:
   - Check for custom scripts in `SBQQ__QuoteCalculatorPlugin__c`.
   - Identify active Price Rules and Product Rules.
2. **Product & Price Book Overlap**:
   - Analyze Product codes and Price Book entries for potential duplicates with target org.
3. **Automation Dependencies**:
   - Map dependencies between Quote status changes and downstream billing/ordering.

Deliverable
Create file: `outputs/[INSERT_ORG_NAME]_cpq_analysis.md`

tags: [ORG_ALIAS], task-2.5, cpq
```

---

## PROMPT 3: Task 3 - Automation & Validation
**Use this after Task 2.**

```text
Task 3: [INSERT_ORG_NAME] Automation & Validation
Summary
Document all flows, workflows, and validation rules. Identify hard-coded values.

Context
Read `docs/ai-instructions.md` for project context
This is TASK 3 for [INSERT_ORG_NAME] org
Inputs
- All Flow metadata (*.flow-meta.xml)
- Apex Classes (*.cls) and Triggers (*.trigger)
- Validation Rules (from object metadata)

Steps
1. List all active flows (Trigger type, Object, Purpose)
   - **CRITICAL**: Flag any Flows/Process Builder using "Fast Field Updates" (Before-Save) as these can block migration if not handled.
   - Check for Schedule-Triggered Flows (these often need to be rebuilt or deactivated during migration).
2. Scan Apex Classes and Flows for HARD-CODED IDs (Regex: `00[a-zA-Z0-9]{13,16}`)
3. Identify cross-object formula fields (performance risk).
4. List validation rules by object with migration risk level.

**Risk Definitions:**
- **Low Risk**: Simple validation (e.g., `NOT(ISBLANK(Email))`).
- **Medium Risk**: Cross-object references (e.g., `Account.Type = 'Partner' && !ISBLANK(Partner_ID__c)`).
- **High Risk**: Hard-coded IDs, specific Profile names, or references to org-specific metadata.

Deliverable
Create file: `outputs/[INSERT_ORG_NAME]_automation.md`

Use this structure:

# [INSERT_ORG_NAME] Org - Automation & Validation Analysis

## Hard-Coded Values (High Risk)
| File Name | Type | Value Found | Context |
|-----------|------|-------------|---------|
| MyTrigger.trigger | Apex | 001... | `if(acc.Id == '001...')` |
| DealFlow.flow | Flow | 005... | User ID assignment |

## Active Flows
...

## Validation Rules
...

tags: [ORG_ALIAS], task-3, automation
```

---

## PROMPT 4: Task 4 - Tech Debt & Integrations
**Use this after Task 3.**

```text
Task 4: [INSERT_ORG_NAME] Technical Debt & Integrations
Summary
Identify unused fields, inactive automation, and external system integrations.

Context
Read `docs/ai-instructions.md` for project context
This is TASK 4 for [INSERT_ORG_NAME] org
Inputs
- `scripts/data/[ORG_ALIAS]/field_stats.csv`
- Page Layout metadata
- Named Credentials, Remote Site Settings, InstalledPackages

Steps
1. **Tech Debt**:
   - Identify "Ghost Metadata" (0% population in field_stats.csv)
   - Identify Inactive Flows
2. **Integrations**:
   - List Named Credentials & Connected Apps
   - Check for Managed Package namespaces (e.g., SBQQ__, npsp__) and flag them as Read-Only Dependencies.

Deliverable
Create file: `outputs/[INSERT_ORG_NAME]_tech_debt_and_integrations.md`

Use this structure:

# [INSERT_ORG_NAME] Org - Technical Debt & Integration Analysis

## Technical Debt

### Ghost Fields (0% Usage)
| Object | Field API Name | Recommendation |
|--------|---------------|----------------|
| Account | Legacy_ID__c | Retire |

### Inactive Automation
...

## Integration Points
### Installed Packages (Read-Only)
| Name | Namespace | Version |
|------|-----------|---------|
| ... | ... | ... |

### Named Credentials
...

tags: [ORG_ALIAS], task-4, tech-debt
```

---

## PROMPT 5: Task 5 - Final Report
**Use this after Task 4.**

```text
Task 5: [INSERT_ORG_NAME] Final Report
Summary
Synthesize all findings into one executive-ready comprehensive report.

Context
Read `docs/ai-instructions.md` for project context
This is TASK 5 for [INSERT_ORG_NAME] org
Inputs
- Outputs from Tasks 1-4

Steps
1. Write Executive Summary
2. **Quality Check**: Ensure all "Red Flags" listed are backed by evidence from previous tasks.
3. Compile detailed findings.

Deliverable
Create file: `outputs/[INSERT_ORG_NAME]_ORG_ANALYSIS_REPORT.md`

Use this structure:

# [INSERT_ORG_NAME] Org - Comprehensive Analysis Report
...

tags: [ORG_ALIAS], task-5, final-report
```

---

## PROMPT 5.5: Data Quality Report
**Use this for a deep dive into data integrity.**

```text
Task 5.5: [INSERT_ORG_NAME] Data Quality Report
Summary
Identify duplicates, orphaned records, and specific data quality violations.

Context
Read `docs/ai-instructions.md` for full project context
This is TASK 5.5 for [INSERT_ORG_NAME] org
Inputs
- `scripts/data/[ORG_ALIAS]/*.csv`
- `scripts/data/[ORG_ALIAS]/field_stats.csv`

Steps
1. **Duplicate Detection**:
   - Perform fuzzy matching on Account Name and Contact Email.
   - Flag potential duplicates.
2. **Orphan Check**:
   - Identify Contacts with no AccountId.
   - Identify Opportunities with no AccountId.
3. **Validation Issues**:
   - Check for Required Field violations (e.g., records where mandatory fields are null or empty).
   - Detect "Zombie" data (records not modified in > 5 years).

Deliverable
Create file: `outputs/[INSERT_ORG_NAME]_data_quality.md`

tags: [ORG_ALIAS], task-5.5, data-quality
```
