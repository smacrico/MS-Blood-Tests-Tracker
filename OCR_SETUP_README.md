# OCR Setup Instructions and Status

## Current Situation

You have 4 PDF files in `data/pdfs/` that are **scanned/image-based PDFs**:
- results_2018-2019.pdf
- results_2021.pdf  
- results_2022-2023.pdf
- results_24062019-.pdf

These PDFs contain images of blood test results, not extractable text, so they require **OCR (Optical Character Recognition)** to read.

## Options to Extract These PDFs

### Option 1: Complete Tesseract OCR Setup (Recommended for Local Processing)

The OCR libraries are installed, but Tesseract OCR engine needs proper configuration:

1. **Download Greek Language Data**:
   - Visit: https://github.com/tesseract-ocr/tessdata
   - Download `ell.traineddata` (Greek) and `eng.traineddata` (English)
   - Place in: `C:\Program Files\Tesseract-OCR\tessdata\`

2. **Install Poppler** (for PDF to image conversion):
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases/
   - Extract and add to PATH

3. **Run the OCR script**: `python test_ocr.py`

### Option 2: Use Online OCR Services

Convert PDFs to text using online tools:
- Adobe Acrobat Online (supports Greek)
- Google Drive (upload PDF, open with Google Docs)
- OnlineOCR.net  

Then place the extracted text in a format the parser can read.

### Option 3: Azure Computer Vision API (Cloud OCR)

If you have Azure subscription, we can integrate Azure Computer Vision OCR which has excellent Greek language support.

### Option 4: Re-save PDFs with Text Layer

If you have access to the original source:
- Re-scan with OCR enabled
- Or use Adobe Acrobat to add text layer
- Then the regular extraction will work

## Current Extraction Status

✅ **Working**: 32 text-based PDFs in subdirectories  
   - Total: 2,164 blood test records
   - Unique tests: 83 types

❌ **Needs OCR**: 4 scanned PDFs in main folder
   - Cannot be processed without OCR setup

## Recommendation

For now, I suggest:
1. Move the 4 scanned PDFs to a separate folder (e.g., `data/pdfs/scanned/`)
2. Continue working with the 32 successfully extracted PDFs
3. Set up OCR later when needed, OR
4. Use online OCR to convert the scanned PDFs to searchable PDFs

Would you like me to help with any of these options?
