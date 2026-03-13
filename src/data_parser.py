import re
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

from src.config import Config

class DataParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = Config()
        
        # Category mappings based on section headers
        self.section_categories = {
            'ΕΡΥΘΡΟΚΥΤΤΑΡΙΚΗ ΣΕΙΡΑ': 'CBC',
            'ΛΕΥΚΟΚΥΤΤΑΡΙΚΗ ΣΕΙΡΑ': 'CBC',
            'ΑΙΜΟΠΕΤΑΛΙΑ': 'CBC',
            'ΒΙΟΧΗΜΙΚΕΣ ΕΞΕΤΑΣΕΙΣ': 'METABOLIC',
            'ΘΥΡΕΟΕΙΔΗΣ': 'THYROID',
            'ΟΡΜΟΝΕΣ': 'HORMONAL',
            'ΛΙΠΙΔΙΑ': 'LIPID'
        }
        
        self.date_patterns = [
            r'Ημ/νία Εξέτασης[\s:]+(\d{1,2}/\d{1,2}/\d{2,4})',
            r'(?:Date|Test Date|Collection Date)[\s:]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})'
        ]
        self.patient_patterns = [
            r'Ονομ/μο[\s:]+([Α-ΩA-ZΆ-Ώ\s]+?)(?:\s+Ημ/νία|$)',
            r'(?:Patient|Name|Patient Name)[\s:]+([A-Za-z\s]+)',
            r'(?:ID|Patient ID)[\s:]+(\w+)'
        ]
    
    def parse_blood_test_from_tables(self, tables: List, text: str, filename: str) -> Optional[Dict[str, Any]]:
        """Parse blood test data from extracted tables (extended for Greek + hormone/lipid panels)."""
        if not tables:
            return None
        try:
            patient_name = self._extract_patient_name(text)
            test_date = self._extract_date(text)
            results: List[Dict[str, Any]] = []
            seen_keys = set()
            for table in tables:
                active_category = 'CBC'
                for row in table:
                    if not row:
                        continue
                    # Join all non-empty cells to capture tests that appear across columns
                    row_text = ' '.join([str(c) for c in row if c])
                    # Section header detection
                    for section, cat in self.section_categories.items():
                        if section in row_text:
                            active_category = cat
                            break
                    # Extract tests from the row
                    for test in self._parse_table_row(row_text, active_category):
                        key = (test['test_name'], test['result_value'], test['reference_range'], test['unit'])
                        if key not in seen_keys:
                            seen_keys.add(key)
                            results.append(test)
            if not results:
                return None
            return {
                'patient_name': patient_name or 'Unknown',
                'test_date': test_date,
                'test_month': test_date.month if test_date else None,
                'test_year': test_date.year if test_date else None,
                'pdf_filename': filename,
                'results': results
            }
        except Exception as e:
            self.logger.error(f"Error parsing table data: {str(e)}", exc_info=True)
            return None
    
    def _parse_table_row(self, text: str, category: str = 'CBC') -> List[Dict[str, Any]]:
        """Parse a table row for multiple possible test formats (Greek + international)."""
        results: List[Dict[str, Any]] = []
        
        # Split on newlines since PDF tables often collapse multiple tests into one cell
        lines = text.split('\n')
        
        for line in lines:
            # Normalize decimal commas to dots
            norm_text = re.sub(r'(\d),(\d)', r'\1.\2', line)
            
            # Patterns (allow spaces between dots/colons: [.\s:]+):
            # Include numbers in test names (HbA1c, B12, etc.)
            # Allow Greek letters after numbers (71α%) and optional < or > before value (<0.2)
            # Allow hyphens and parentheses in test names (D-3, Lp (α), etc.)
            patterns = [
                # Greek name (ABBR) [. . . . :] value unit ref_min - ref_max
                # Value may have Greek letters like 71α% or start with < like <0.2
                r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-\(\)]+?)\s*\(([A-Z0-9][A-Z0-9]{1,6})\)\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)\s+(\d+\.?\d*)\s*-\s*(\d+\.?\d*)',
                # ABBR [. . . :] value unit ref_min - ref_max
                r'\b([A-Z0-9][A-Z0-9]{1,6})\b\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)\s+(\d+\.?\d*)\s*-\s*(\d+\.?\d*)',
                # Name [. . . :] value unit ref_min - ref_max (include numbers, hyphens, parentheses)
                r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-\(\)]{3,}?)\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)\s+(\d+\.?\d*)\s*-\s*(\d+\.?\d*)'
            ]
            for patt in patterns:
                for m in re.finditer(patt, norm_text):
                    if len(m.groups()) == 6:  # name(abbr) pattern
                        greek_name, abbr, val, unit, ref_min, ref_max = m.groups()
                        # Use full name format: "Greek Name (ABBR)"
                        test_token = f"{greek_name.strip()} ({abbr.strip()})"
                    elif len(m.groups()) == 5 and patt.startswith('\\b'):
                        test_token, val, unit, ref_min, ref_max = m.groups()
                        greek_name = test_token
                    else:  # name without abbrev
                        greek_name, val, unit, ref_min, ref_max = m.groups()
                        test_token = greek_name.strip()
                    
                    test_token = test_token.strip()
                    # Skip numeric-only or punctuation tokens mistakenly captured
                    if not re.search(r'[A-ZΑ-Ωα-ωά-ώa-z]', test_token):
                        continue
                    test_category = self.config.get_category_for_test(test_token)
                    if test_category == 'OTHER':
                        test_category = self.config.get_category_for_test(greek_name.strip())
                    if test_category == 'OTHER':
                        test_category = category
                    try:
                        flag = self._determine_flag(float(val), float(ref_min), float(ref_max))
                    except ValueError:
                        flag = 'Unknown'
                    results.append({
                        'test_name': test_token,
                        'result_value': val,
                        'unit': unit,
                        'reference_range': f'{ref_min}-{ref_max}',
                        'flag': flag,
                        'category': test_category
                    })
            
            # Additional pattern for biochemical tests with comparison operators <, >, <=, >=
            # Handles both: "Name (ABBR) . . . : value unit < threshold" and "Name . . . : value unit < threshold"
            # Also handles Greek text between unit and operator: "Name . . . : value unit Φυσιολογικό: < threshold"
            # Include numbers in test names (HbA1c, B12, etc.)
            # Allow < or > before value (<0.2) and Greek letters after value (71α%)
            # Allow hyphens and parentheses in names (D-3, Lp (α), etc.)
            bio_pattern = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-\(\)]+?)\s*(?:\(([A-Z0-9\-]+)\))?\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)\s+.*?([<>]=?)\s*(\d+\.?\d*)'
            for m in re.finditer(bio_pattern, norm_text):
                groups = m.groups()
                if len(groups) == 6:
                    greek_name, abbr, val, unit, operator, threshold = groups
                    # Use full name when both Greek name and abbreviation exist
                    if abbr:
                        test_token = f"{greek_name.strip()} ({abbr.strip()})"
                    else:
                        test_token = greek_name.strip()
                    
                    # Skip numeric-only tokens, allow Greek or Latin letters
                    if not re.search(r'[A-ZΑ-Ωα-ωά-ώa-z]', test_token):
                        continue
                    
                    test_category = self.config.get_category_for_test(test_token)
                    if test_category == 'OTHER':
                        test_category = self.config.get_category_for_test(greek_name.strip())
                    if test_category == 'OTHER':
                        test_category = category
                    
                    # Determine flag based on operator
                    try:
                        val_f = float(val)
                        thresh_f = float(threshold)
                        if operator == '<':
                            flag = 'Normal' if val_f < thresh_f else 'High'
                            ref_range = f'< {threshold}'
                        else:  # >
                            flag = 'Normal' if val_f > thresh_f else 'Low'
                            ref_range = f'> {threshold}'
                    except ValueError:
                        flag = 'Unknown'
                        ref_range = f'{operator} {threshold}'
                    
                    results.append({
                        'test_name': test_token,
                        'result_value': val,
                        'unit': unit,
                        'reference_range': ref_range,
                        'flag': flag,
                        'category': test_category
                    })
        
        return results
    
    def _determine_flag(self, value: float, ref_min: float, ref_max: float) -> str:
        """Determine if a test result is Normal, High, or Low"""
        if value < ref_min:
            return 'Low'
        elif value > ref_max:
            return 'High'
        else:
            return 'Normal'
    
    def parse_blood_test_from_text(self, text: str, filename: str) -> Optional[Dict[str, Any]]:
        """Parse blood test data from plain text (for pages without tables like biochemical tests)."""
        if not text:
            return None
        try:
            patient_name = self._extract_patient_name(text)
            test_date = self._extract_date(text)
            results = []
            seen_keys = set()
            
            # Split text into lines for processing
            lines = text.split('\n')
            active_category = 'METABOLIC'
            
            for line in lines:
                # Check for category headers
                for header, cat in self.section_categories.items():
                    if header in line:
                        active_category = cat
                        break
                
                # Pattern 1: Greek name with optional abbreviation and range (e.g., "Σάκχαρο . . . : 80 mg/dL 70 - 115")
                # Include numbers in test names (e.g., B12, D3, HbA1c)
                # Allow Greek letters after value (71α%) and < or > before value (<0.2)
                # Allow hyphens and parentheses in names (D-3, Lp (α), etc.)
                pattern1 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-\(\)]+?)\s*(?:\(([A-Z0-9\-]+)\))?\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)\s+(\d+\.?\d*)\s*-\s*(\d+\.?\d*)'
                m1 = re.search(pattern1, line)
                if m1:
                    greek_name, abbr, val, unit, ref_min, ref_max = m1.groups()
                    # Use full name when Greek name exists, otherwise use abbreviation
                    if abbr:
                        test_token = f"{greek_name.strip()} ({abbr.strip()})"
                    else:
                        test_token = greek_name.strip()
                    
                    # Skip numeric-only tokens, allow Greek or Latin letters
                    if not re.search(r'[A-ZΑ-Ωα-ωά-ώa-z]', test_token):
                        continue
                    
                    # Create unique key for deduplication
                    key = (test_token, val, unit, f'{ref_min}-{ref_max}')
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)
                    
                    # Determine category
                    test_category = self.config.get_category_for_test(test_token)
                    if test_category == 'OTHER':
                        test_category = self.config.get_category_for_test(greek_name.strip())
                    if test_category == 'OTHER':
                        test_category = active_category
                    
                    # Determine flag
                    try:
                        flag = self._determine_flag(float(val), float(ref_min), float(ref_max))
                    except ValueError:
                        flag = 'Unknown'
                    
                    results.append({
                        'test_name': test_token,
                        'result_value': val,
                        'unit': unit,
                        'reference_range': f'{ref_min}-{ref_max}',
                        'flag': flag,
                        'category': test_category
                    })
                    continue
                
                # Pattern 2: Threshold-based references with <, >, <=, >= operators
                # Handle cases like "127 mg/dL Φυσιολογικό: < 150" or "5.0 % >= 1"
                # Include numbers in test names (e.g., HbA1c, B12)
                # Allow < or > before value (<0.2) and Greek letters after value (71α%)
                # Allow hyphens and parentheses in names (D-3, Lp (α), etc.)
                pattern2 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-\(\)]+?)\s*(?:\(([A-Z0-9\-]+)\))?\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)\s+.*?([<>]=?)\s*(\d+\.?\d*)'
                m2 = re.search(pattern2, line)
                if m2:
                    greek_name, abbr, val, unit, operator, threshold = m2.groups()
                    # Use full name when Greek name exists, otherwise use abbreviation
                    if abbr:
                        test_token = f"{greek_name.strip()} ({abbr.strip()})"
                    else:
                        test_token = greek_name.strip()
                    
                    # Skip numeric-only tokens
                    if not re.search(r'[A-ZΑ-Ωα-ωά-ώ]', test_token):
                        continue
                    
                    # Create unique key for deduplication
                    ref_range = f'{operator} {threshold}'
                    key = (test_token, val, unit, ref_range)
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)
                    
                    # Determine category
                    test_category = self.config.get_category_for_test(test_token)
                    if test_category == 'OTHER':
                        test_category = self.config.get_category_for_test(greek_name.strip())
                    if test_category == 'OTHER':
                        test_category = active_category
                    
                    # Determine flag based on operator
                    try:
                        val_f = float(val)
                        thresh_f = float(threshold)
                        if operator == '<':
                            flag = 'Normal' if val_f < thresh_f else 'High'
                        else:  # >
                            flag = 'Normal' if val_f > thresh_f else 'Low'
                    except ValueError:
                        flag = 'Unknown'
                    
                    results.append({
                        'test_name': test_token,
                        'result_value': val,
                        'unit': unit,
                        'reference_range': ref_range,
                        'flag': flag,
                        'category': test_category
                    })
                    continue
                
                # Pattern 3: Simple value-only pattern (no reference range)
                # For tests like "Μη- HDL χοληστερόλη(non-HDL-C) . . . : 153.0 mg/dL Σύμφωνα..."
                pattern3 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-\(\)]+?)\s*(?:\(([A-Za-z0-9\-]+)\))?\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)\s*(?:[Α-ΩΆ-Ώα-ωά-ώ]|\.|$)'
                m3 = re.search(pattern3, line)
                if m3:
                    greek_name, abbr, val, unit = m3.groups()
                    # Use full name when both Greek name and abbreviation exist
                    if abbr:
                        test_token = f"{greek_name.strip()} ({abbr.strip()})"
                    else:
                        test_token = greek_name.strip()
                    
                    # Skip numeric-only tokens
                    if not re.search(r'[A-ZΑ-Ωα-ωά-ώa-z]', test_token):
                        continue
                    
                    # Create unique key for deduplication
                    key = (test_token, val, unit, '')
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)
                    
                    # Determine category
                    test_category = self.config.get_category_for_test(test_token)
                    if test_category == 'OTHER':
                        test_category = self.config.get_category_for_test(greek_name.strip())
                    if test_category == 'OTHER':
                        test_category = active_category
                    
                    results.append({
                        'test_name': test_token,
                        'result_value': val,
                        'unit': unit,
                        'reference_range': '',
                        'flag': 'Unknown',
                        'category': test_category
                    })
                    continue
            
            if not results:
                return None
            
            return {
                'patient_name': patient_name or 'Unknown',
                'test_date': test_date,
                'test_month': test_date.month if test_date else None,
                'test_year': test_date.year if test_date else None,
                'pdf_filename': filename,
                'results': results
            }
        except Exception as e:
            self.logger.error(f"Error parsing text data from {filename}: {str(e)}")
            return None
    
    def parse_blood_test(self, text: str, filename: str) -> Optional[Dict[str, Any]]:
        if not text:
            return None
        try:
            patient_name = self._extract_patient_name(text)
            test_date = self._extract_date(text)
            results = self._extract_test_results(text)
            if not results:
                self.logger.warning(f"No test results found in {filename}")
                return None
            return {
                'patient_name': patient_name or 'Unknown',
                'test_date': test_date,
                'test_month': test_date.month if test_date else None,
                'test_year': test_date.year if test_date else None,
                'pdf_filename': filename,
                'results': results
            }
        except Exception as e:
            self.logger.error(f"Error parsing test data: {str(e)}")
            return None
    
    def _extract_patient_name(self, text: str) -> Optional[str]:
        for pattern in self.patient_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                name = re.sub(r'\s+', ' ', name)
                if len(name) > 3:
                    return name
        return None
    
    def _extract_date(self, text: str) -> Optional[datetime]:
        for pattern in self.date_patterns:
            match = re.search(pattern, text)
            if match:
                date_str = match.group(1)
                return self._parse_date_string(date_str)
        return None
    
    def _parse_date_string(self, date_str: str) -> Optional[datetime]:
        date_formats = [
            '%d/%m/%Y','%m/%d/%Y','%d/%m/%Y','%m-%d-%Y','%d-%m-%Y','%Y-%m-%d','%m/%d/%y','%d/%m/%y'
        ]
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        self.logger.warning(f"Could not parse date: {date_str}")
        return None
    
    def _extract_test_results(self, text: str) -> List[Dict[str, Any]]:
        results = []
        pattern = r'([A-Za-z0-9\s\-]+?)\s+([\d.]+)\s+([A-Za-z0-9/\^%]+)\s+([\d.\-]+)\s*(?:-\s*[\d.]+)?\s*(Normal|High|Low|Critical)?'
        matches = re.finditer(pattern, text)
        for match in matches:
            test_name = match.group(1).strip()
            result_value = match.group(2).strip()
            unit = match.group(3).strip()
            reference_range = match.group(4).strip()
            flag = match.group(5).strip() if match.group(5) else 'Normal'
            category = self.config.get_category_for_test(test_name)
            results.append({
                'test_name': test_name,
                'result_value': result_value,
                'unit': unit,
                'reference_range': reference_range,
                'flag': flag,
                'category': category
            })
        if not results:
            results = self._extract_simple_results(text)
        return results
    
    def _extract_simple_results(self, text: str) -> List[Dict[str, Any]]:
        results = []
        common_tests = list(self.config.config_data.get('test_name_mappings', {}).keys())
        for test_name in common_tests:
            pattern = rf'{re.escape(test_name)}\s*:?\s*([\d.]+)\s*([A-Za-z0-9/\^%]*)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                category = self.config.get_category_for_test(test_name)
                results.append({
                    'test_name': test_name,
                    'result_value': match.group(1),
                    'unit': match.group(2) if match.group(2) else '',
                    'reference_range': '',
                    'flag': 'Unknown',
                    'category': category
                })
        return results
