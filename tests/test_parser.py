import pytest
from datetime import datetime
from src.data_parser import DataParser

@pytest.fixture
def parser():
    return DataParser()

def test_parse_date_string(parser):
    test_cases = [
        ("01/15/2025", datetime(2025, 1, 15)),
        ("2025-01-15", datetime(2025, 1, 15)),
        ("15/01/2025", datetime(2025, 1, 15))
    ]
    for date_str, expected in test_cases:
        result = parser._parse_date_string(date_str)
        assert result is not None
        assert result.date() == expected.date()

def test_extract_patient_name(parser):
    text = "Patient Name: John Doe\nDate: 01/15/2025"
    result = parser._extract_patient_name(text)
    assert result == "John Doe"

def test_extract_simple_results(parser):
    text = """
    WBC: 7.5
    Hemoglobin: 14.2
    Platelet: 250
    """
    results = parser._extract_simple_results(text)
    assert len(results) > 0
    assert any(r['test_name'] == 'WBC' for r in results)

def test_parse_blood_test(parser):
    sample_text = """
    Patient Name: Jane Smith
    Test Date: 03/15/2025

    WBC: 6.8 10^3/uL
    Hemoglobin: 13.5 g/dL
    Creatinine: 0.9 mg/dL
    """
    result = parser.parse_blood_test(sample_text, "test.pdf")
    assert result is not None
    assert result['patient_name'] == 'Jane Smith'
    assert result['test_date'] is not None
    assert len(result['results']) > 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])