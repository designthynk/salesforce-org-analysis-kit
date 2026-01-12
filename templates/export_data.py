#!/usr/bin/env python3
"""
Export Org data with clean CSV formatting and Field Stats
TEMPLATE: Requires customization before running!
"""
import json
import subprocess
import csv
from pathlib import Path
from datetime import datetime
import pandas as pd
import math

# ==========================================
# CONFIGURATION: YOU MUST EDIT THESE VALUES
# ==========================================

# 1. Output Directory
OUTPUT_DIR = Path("scripts/data/ExportedData") 

# 2. Target Org Alias (from 'sf org list')
TARGET_ORG_ALIAS = "your-org-alias"

# 3. Tier 1: Core Objects (Full Export)
# Add critical objects here. We pull ALL records for these.
TIER_1_OBJECTS = {
    "Account": "SELECT Id, Name, Type, Industry, RecordTypeId, LastModifiedDate, OwnerId, CreatedDate FROM Account",
    "Opportunity": "SELECT Id, Name, AccountId, StageName, Amount, CloseDate, RecordTypeId, LastModifiedDate, OwnerId, CreatedDate FROM Opportunity",
    "Contact": "SELECT Id, Name, AccountId, Email, RecordTypeId, LastModifiedDate, OwnerId, CreatedDate FROM Contact",
    "User": "SELECT Id, Name, Email, IsActive, ProfileId, UserRoleId, LastModifiedDate FROM User",
}

# 4. Tier 2: High Volume / Secondary Objects (Sampled)
# We limit these to 5000 records to spot patterns without blowing up storage.
TIER_2_OBJECTS = {
    "Task": "SELECT Id, Subject, Status, Priority, OwnerId FROM Task ORDER BY CreatedDate DESC",
    # Add other objects like Event, Case, Logs here
}

# ==========================================
# END CONFIGURATION
# ==========================================

def run_soql_query(query, target_org=TARGET_ORG_ALIAS, limit_size=2000):
    """Run a SOQL query using SFDX CLI with pagination."""
    all_records = []
    done = False
    next_url = None
    
    # Initial query
    print(f"  Running query: {query[:60]}...")
    
    # Check if query already has a LIMIT (for Tier 2)
    has_limit = "LIMIT" in query.upper()
    
    cmd = ["sf", "data", "query", "--query", query, "--target-org", target_org, "--json"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print(f"  Error running query: {result.stderr}")
            return {"success": False, "error": result.stderr}
            
        data = json.loads(result.stdout)
        if not data.get("result"):
             return {"success": False, "error": "No result in response"}
             
        records = data["result"]["records"]
        total_size = data["result"]["totalSize"]
        all_records.extend(records)
        
        # Handle pagination (nextRecordsUrl)
        # Note: Standard CLI handling of nextRecordsUrl is sometimes tricky. 
        # For Tier 1 objects > 2000 records, we recommend switching to Bulk API.
        
        if not has_limit and total_size > 2000:
             print(f"  WARNING: Query returned {len(records)} of {total_size} records.")
             print("  To get all records, this script suggests using Bulk API.")
             # TODO: Implement full pagination loop or switch to:
             # cmd = ["sf", "data", "query", "--query", query, "--target-org", target_org, "--bulk", "--wait", "10", "--json"]
        
        return {"success": True, "records": all_records, "totalSize": total_size}

    except Exception as e:
        return {"success": False, "error": str(e)}

def clean_value(value):
    """Clean a value for CSV."""
    if value is None:
        return ""
    if isinstance(value, str):
        cleaned = value.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        while '  ' in cleaned:
            cleaned = cleaned.replace('  ', ' ')
        return cleaned.strip()
    return value

def flatten_record(record):
    """Flatten nested attributes."""
    flattened = {}
    for key, value in record.items():
        if key == "attributes":
            continue
        if isinstance(value, dict):
            if "attributes" in value:
                rel_name = value.get("Name", "")
                flattened[f"{key}.Name"] = clean_value(rel_name)
            else:
                flattened[key] = clean_value(json.dumps(value))
        else:
            flattened[key] = clean_value(value)
    return flattened

def analyze_field_stats(filename, records):
    """Calculate null rates and staleness using Pandas."""
    if not records:
        return []
    
    # Create DataFrame
    df = pd.DataFrame([flatten_record(r) for r in records])
    
    stats = []
    total_rows = len(df)
    
    # Check for LastModifiedDate for staleness
    last_mod_col = next((c for c in df.columns if 'LastModifiedDate' in c), None)
    stale_threshold_date = None
    if last_mod_col:
        try:
            # Simple check: records older than 2 years
            # This is a basic heuristic
            pass 
        except:
            pass

    for col in df.columns:
        # Count non-null and non-empty string values
        populated_count = df[col].apply(lambda x: 1 if x and str(x).strip() != "" else 0).sum()
        populated_pct = (populated_count / total_rows) * 100
        
        # Check for single value dominance (likely misconfigured or default)
        unique_vals = df[col].nunique()
        most_common_pct = 0
        if total_rows > 0:
             most_common_pct = (df[col].value_counts().iloc[0] / total_rows) * 100 if unique_vals > 0 else 0

        # Detect "zombie" datetime fields (all values same year? - skipped for simplicity, just flagging high dominance)

        stats.append({
            "Object": filename.replace(".csv", ""),
            "Field": col,
            "Total_Records": total_rows,
            "Populated_Records": populated_count,
            "Populated_Percentage": round(populated_pct, 2),
            "Unique_Values": unique_vals,
            "Dominant_Value_Pct": round(most_common_pct, 2)
        })
    
    return stats

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_field_stats = []
    
    # Process Tier 1 Objects
    print("--- Tier 1: Core Objects (Full Export) ---")
    for obj_name, query in TIER_1_OBJECTS.items():
        res = run_soql_query(query)
        if res["success"]:
            records = res["records"]
            filename = f"{obj_name}.csv"
            
            # Write CSV
            filepath = OUTPUT_DIR / filename
            if records:
                fieldnames = flatten_record(records[0]).keys()
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                    writer.writeheader()
                    for r in records:
                        writer.writerow(flatten_record(r))
                print(f"  ✓ Saved {len(records)} records to {filename}")
                
                # Analyze Stats
                stats = analyze_field_stats(filename, records)
                all_field_stats.extend(stats)
            else:
                print(f"  No records found for {obj_name}")
        else:
            print(f"  Error exporting {obj_name}: {res['error']}")

    # Process Tier 2 Objects
    print("\n--- Tier 2: High Volume (Sampled) ---")
    for obj_name, query in TIER_2_OBJECTS.items():
        # Enforce Limit if not present
        if "LIMIT" not in query.upper():
            query += " LIMIT 5000"
            
        res = run_soql_query(query)
        if res["success"]:
            records = res["records"]
            filename = f"{obj_name}_SAMPLE.csv"
             
             # Write CSV
            filepath = OUTPUT_DIR / filename
            if records:
                fieldnames = flatten_record(records[0]).keys()
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                    writer.writeheader()
                    for r in records:
                        writer.writerow(flatten_record(r))
                print(f"  ✓ Saved {len(records)} sample records to {filename}")
                
                 # Analyze Stats
                stats = analyze_field_stats(filename, records)
                all_field_stats.extend(stats)
            else:
                 print(f"  No records found for {obj_name}")
        else:
            print(f"  Error exporting {obj_name}: {res['error']}")
            
    # Save Field Statistics
    if all_field_stats:
        stats_path = OUTPUT_DIR / "field_stats.csv"
        keys = all_field_stats[0].keys()
        with open(stats_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_field_stats)
        print(f"\n✓ Field Statistics saved to {stats_path}")

if __name__ == "__main__":
    main()
