import yaml
from pathlib import Path
from typing import Dict, Any

class Config:
    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = Path(config_file)
        self.config_data = self._load_config()
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.pdf_dir = self.data_dir / "pdfs"
        self.database_path = self.data_dir / "ms_blood_tests.db"
        self.data_dir.mkdir(exist_ok=True)
        self.pdf_dir.mkdir(exist_ok=True)
    def _load_config(self) -> Dict[str, Any]:
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f) or {}
        return self._get_default_config()
    def _get_default_config(self) -> Dict[str, Any]:
        return {
            'test_categories': {
                'CBC': 'Complete Blood Count',
                'LFT': 'Liver Function Tests',
                'KFT': 'Kidney Function Tests',
                'LIPID': 'Lipid Panel',
                'THYROID': 'Thyroid Function Tests',
                'VITAMIN_D': 'Vitamin D',
                'VITAMIN_B12': 'Vitamin B12',
                'INFLAMMATORY': 'Inflammatory Markers',
                'HORMONAL': 'Hormonal Panel',
                'METABOLIC': 'Metabolic Panel',
                'HEMATOLOGY': 'Hematology Special Tests'
            },
            'test_name_mappings': {
                'WBC': 'CBC','RBC': 'CBC','HGB': 'CBC','HCT': 'CBC','PLT': 'CBC',
                'NEUT': 'CBC','LYM': 'CBC','MONO': 'CBC','EOS': 'CBC','BASO': 'CBC',
                'MCV': 'CBC','MCH': 'CBC','MCHC': 'CBC','RDW-CV': 'CBC','RDW': 'CBC',
                'MPV': 'CBC','PDW': 'CBC','PCT': 'CBC',
                'Hemoglobin': 'CBC','Hematocrit': 'CBC','Platelet': 'CBC','White Blood Cell': 'CBC','Red Blood Cell': 'CBC',
                # Liver function tests
                'ALT': 'LFT','SGPT': 'LFT','AST': 'LFT','SGOT': 'LFT','ALP': 'LFT',
                'Bilirubin': 'LFT','Albumin': 'LFT','γ-GT': 'LFT','GGT': 'LFT',
                'LDH': 'LFT','Amylase': 'LFT',
                # Greek liver function tests
                'Τρανσαμινάση AST': 'LFT','Τρανσαμινάση ALT': 'LFT',
                'γ-Γλουταμυλοτρανσφεράση': 'LFT','Αλκαλική Φωσφατάση': 'LFT',
                'Χολερυθρίνη Ολική': 'LFT','Χολερυθρίνη Αμεση': 'LFT',
                'Γαλακτική αφυδρογονάση': 'LFT',
                # Kidney function tests
                'Creatinine': 'KFT','BUN': 'KFT','eGFR': 'KFT','Urea': 'KFT',
                'Κρεατινίνη': 'KFT','Ουρία': 'KFT',  # Greek names
                # Metabolic/Glucose
                'Glucose': 'METABOLIC','Sugar': 'METABOLIC','Σάκχαρο': 'METABOLIC',  # Greek
                # Electrolytes
                'Calcium': 'METABOLIC','Ca': 'METABOLIC','Magnesium': 'METABOLIC','Mg': 'METABOLIC',
                'Potassium': 'METABOLIC','K': 'METABOLIC','Sodium': 'METABOLIC','Na': 'METABOLIC',
                # Greek electrolytes
                'Κάλιο Ορού': 'METABOLIC','Νάτριο Ορού': 'METABOLIC',
                # Iron
                'Iron': 'METABOLIC','Fe': 'METABOLIC','Ferritin': 'METABOLIC',
                'Σίδηρος': 'METABOLIC','Φερριτίνη': 'METABOLIC',
                # Enzymes
                'CPK': 'METABOLIC','CK': 'METABOLIC',
                # Lipids
                'Cholesterol': 'LIPID','Total Cholesterol': 'LIPID','HDL': 'LIPID','LDL': 'LIPID','Triglycerides': 'LIPID','TG': 'LIPID',
                'Χοληστερίνη': 'LIPID','Τριγλυκερίδια': 'LIPID',  # Greek names
                'HDL - Χοληστερόλη': 'LIPID','LDL - Χοληστερόλη': 'LIPID',
                # Thyroid
                'TSH': 'THYROID','T3': 'THYROID','T4': 'THYROID','Free T4': 'THYROID','FT3': 'THYROID','FT4': 'THYROID',
                # Greek thyroid
                'Θυρεοτρόπος Ορμόνη': 'THYROID','Θυροξίνη Ελεύθερη': 'THYROID','Καλσιτονίνη': 'THYROID',
                # Vitamins
                'Vitamin D': 'VITAMIN_D','25-OH Vitamin D': 'VITAMIN_D','Vitamin B12': 'VITAMIN_B12','Cobalamin': 'VITAMIN_B12',
                'Βιταμίνη B12': 'VITAMIN_B12','Φυλλικό Οξύ': 'VITAMIN_B12',
                # Inflammatory
                'CRP': 'INFLAMMATORY','ESR': 'INFLAMMATORY','C-Reactive Protein': 'INFLAMMATORY',
                # Hormonal panel common tests
                'Testosterone': 'HORMONAL','Estradiol': 'HORMONAL','E2': 'HORMONAL','Cortisol': 'HORMONAL','Prolactin': 'HORMONAL',
                'FSH': 'HORMONAL','LH': 'HORMONAL','DHEA': 'HORMONAL','DHEA-S': 'HORMONAL','Progesterone': 'HORMONAL',
                # Hematology special tests
                'ΓΛΥΚΟΖΥΛΙΩΜΕΝΗ HbA1c': 'HEMATOLOGY','Αμυλάση Ορού': 'HEMATOLOGY'
            }
        }
    def get_category_for_test(self, test_name: str) -> str:
        mappings = self.config_data.get('test_name_mappings', {})
        if test_name in mappings:
            return mappings[test_name]
        test_name_lower = test_name.lower()
        for key, category in mappings.items():
            if key.lower() in test_name_lower or test_name_lower in key.lower():
                return category
        return 'OTHER'
    def get_all_categories(self) -> Dict[str, str]:
        cats = self.config_data.get('test_categories')
        # Fallback to defaults if config file lacks test_categories or it's empty
        if not cats:
            return self._get_default_config().get('test_categories', {})
        return cats