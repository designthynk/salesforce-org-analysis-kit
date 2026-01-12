#!/usr/bin/env python3
"""
Extract Field Metadata from Salesforce Metadata XML Files
TEMPLATE: Requires customization of the paths in main()!
"""

import os
import re
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import sys

@dataclass
class FieldMetadata:
    """Field metadata extracted from Salesforce XML."""
    api_name: str
    label: str
    field_type: str
    required: bool
    description: str = ""
    formula: str = ""
    default_value: str = ""
    has_lookup_filter: bool = False
    picklist_values: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if self.picklist_values is None:
            self.picklist_values = []

# Standard Salesforce fields that don't always have metadata XML files
STANDARD_FIELDS = {
    'Account': {
        'Id': FieldMetadata('Id', 'Account ID', 'Id', True),
        'Name': FieldMetadata('Name', 'Account Name', 'Text', True),
        'OwnerId': FieldMetadata('OwnerId', 'Owner', 'Lookup', True),
        'CreatedDate': FieldMetadata('CreatedDate', 'Created Date', 'DateTime', True),
        # ... Add other standard fields as needed
    },
    'Opportunity': {
        'Id': FieldMetadata('Id', 'Opportunity ID', 'Id', True),
        'Name': FieldMetadata('Name', 'Opportunity Name', 'Text', True),
        'StageName': FieldMetadata('StageName', 'Stage', 'Picklist', True),
        'Amount': FieldMetadata('Amount', 'Amount', 'Currency', False),
        'CloseDate': FieldMetadata('CloseDate', 'Close Date', 'Date', True),
        # ... Add other standard fields as needed
    }
}

def parse_field_xml(file_path: Path) -> Optional[FieldMetadata]:
    """Parse a field-meta.xml file and extract field metadata."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        ns = {'sf': 'http://soap.sforce.com/2006/04/metadata'}
        
        def get_text(element_name):
            elem = root.find(f'sf:{element_name}', ns)
            if elem is None:
                elem = root.find(element_name)
            return elem.text if elem is not None else ""
        
        api_name = get_text('fullName') or file_path.stem.replace('.field-meta', '')
        label = get_text('label') or api_name
        field_type = get_text('type') or 'Unknown'
        required = get_text('required').lower() == 'true' if get_text('required') else False
        description = get_text('description') or ""
        formula = get_text('formula') or ""
        default_value = get_text('defaultValue') or ""
        
        has_lookup_filter = True if (root.find('sf:lookupFilter', ns) is not None or root.find('lookupFilter') is not None) else False
        
        picklist_values = []
        value_set = root.find('sf:valueSet', ns) or root.find('valueSet')
        if value_set:
            for value in value_set.iter():
                if value.tag.endswith('fullName') and value.text:
                    picklist_values.append(value.text)
        
        return FieldMetadata(api_name, label, field_type, required, description, formula, default_value, has_lookup_filter, picklist_values)
    except Exception as e:
        print(f"  Warning: Could not parse {file_path}: {e}")
        return None

def extract_fields_from_org(org_path: Path, object_name: str) -> Dict[str, FieldMetadata]:
    """Extract all field metadata for an object from an org's metadata folder."""
    fields = {}
    possible_paths = [
        org_path / 'objects' / object_name / 'fields',
        org_path / 'main' / 'default' / 'objects' / object_name / 'fields',
    ]
    
    fields_path = None
    for path in possible_paths:
        if path.exists():
            fields_path = path
            break
            
    if fields_path:
        for field_file in fields_path.glob('*.field-meta.xml'):
            field_meta = parse_field_xml(field_file)
            if field_meta:
                fields[field_meta.api_name] = field_meta
                
    if object_name in STANDARD_FIELDS:
        for api_name, std_field in STANDARD_FIELDS[object_name].items():
            if api_name not in fields:
                fields[api_name] = std_field
                
    return fields

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_metadata.py <OrgPath> <Object1> [Object2 ...]")
        print("Example: python extract_metadata.py force-app/my-org Account Opportunity")
        return

    org_path_str = sys.argv[1]
    object_names = sys.argv[2:]
    
    base_path = Path.cwd()
    org_path = base_path / org_path_str
    
    if not org_path.exists():
        print(f"Error: Org path '{org_path}' does not exist.")
        return

    print(f"Extracting metadata from: {org_path}")
    
    for object_name in object_names:
        print(f"\nProcessing {object_name}...")
        fields = extract_fields_from_org(org_path, object_name)
        
        print(f"  Found {len(fields)} fields.")
        for api_name, meta in sorted(fields.items())[:5]: # Print first 5 as sample
            print(f"    - {api_name} ({meta.field_type})")
        
        # Here you would typically write this to a CSV or JSON file
        # For the starter kit, we just print summary to verify it works.

if __name__ == '__main__':
    main()
