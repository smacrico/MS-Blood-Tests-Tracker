# ms-blood-test-tracker Main Application

import argparse
import logging
import sys
from pathlib import Path

from src.pdf_reader import PDFReader
from src.database_handler import DatabaseHandler
from src.data_parser import DataParser
from src.config import Config

def setup_logging():
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def process_pdfs(pdf_dir: Path, db_handler, logger):
    pdf_reader = PDFReader()
    data_parser = DataParser()
    # Search for PDFs recursively in all subdirectories, excluding 'scanned' folder
    all_pdfs = list(pdf_dir.glob("**/*.pdf")) + list(pdf_dir.glob("**/*.PDF"))
    pdf_files = [p for p in all_pdfs if 'scanned' not in str(p)]
    if not pdf_files:
        logger.warning(f"No PDF files found in {pdf_dir}")
        return
    logger.info(f"Found {len(pdf_files)} PDF file(s) to process")
    total_tests = 0
    total_results = 0
    for pdf_file in pdf_files:
        try:
            page_count = pdf_reader.get_page_count(pdf_file)
            logger.info(f"Processing: {pdf_file.name} (pages: {page_count})")
            pdf_text = pdf_reader.extract_text(pdf_file)
            # Process BOTH tables and text to capture all test formats
            all_results = []
            parsed_data = None
            
            # Step 1: Extract from tables (CBC tests on Page 1)
            try:
                tables = pdf_reader.extract_tables(pdf_file)
                if tables:
                    logger.info(f"Table extraction found {len(tables)} table(s) across {page_count} page(s) for {pdf_file.name}")
                    table_data = data_parser.parse_blood_test_from_tables(tables, pdf_text, pdf_file.name)
                    if table_data and table_data.get('results'):
                        all_results.extend(table_data['results'])
                        parsed_data = table_data
                        logger.info(f"Extracted {len(table_data['results'])} results from tables")
            except Exception as table_err:
                logger.debug(f"Table extraction failed for {pdf_file.name}: {table_err}")
            
            # Step 2: Extract from text (biochemical tests on Page 2)
            try:
                text_results = data_parser.parse_blood_test_from_text(pdf_text, pdf_file.name)
                if text_results and text_results.get('results'):
                    all_results.extend(text_results['results'])
                    if not parsed_data:
                        parsed_data = text_results
                    else:
                        parsed_data['results'] = all_results
                    logger.info(f"Extracted {len(text_results['results'])} additional results from text")
            except Exception as text_err:
                logger.debug(f"Text extraction failed for {pdf_file.name}: {text_err}")
            
            # Fallback to legacy text parser if nothing found
            if not all_results:
                logger.info(f"No structured data extracted; attempting legacy text parser")
                parsed_data = data_parser.parse_blood_test(pdf_text, pdf_file.name)
                if parsed_data:
                    all_results = parsed_data.get('results', [])
            
            if parsed_data and all_results:
                parsed_data['results'] = all_results
                db_handler.insert_test_results(parsed_data)
                total_tests += 1
                total_results += len(all_results)
                logger.info(f"Processed: {pdf_file.name} ({len(all_results)} total results extracted; pages parsed: {page_count})")
            else:
                logger.warning(f"No data extracted from: {pdf_file.name} (pages: {page_count})")
        except Exception as e:
            logger.error(f"Error processing {pdf_file.name}: {str(e)}", exc_info=True)
    logger.info(f"\nProcessing complete!")
    logger.info(f"Total tests processed: {total_tests}")
    logger.info(f"Total results stored: {total_results}")

def query_results(db_handler, args, logger):
    filters = {}
    if args.patient:
        filters['patient_name'] = args.patient
    if args.start_date:
        filters['start_date'] = args.start_date
    if args.end_date:
        filters['end_date'] = args.end_date
    if args.category:
        filters['category'] = args.category
    results = db_handler.query_results(filters)
    if results:
        logger.info(f"\nFound {len(results)} test result(s):")
        for result in results:
            print(f"\n{'-'*60}")
            print(f"Date: {result['test_date']}")
            print(f"Patient: {result['patient_name']}")
            print(f"Category: {result['category_name']}")
            print(f"Test: {result['test_name']}")
            print(f"Result: {result['result_value']} {result['unit']}")
            print(f"Reference: {result['reference_range']}")
            print(f"Status: {result['flag']}")
        
        # Save query results to database
        try:
            saved_count = db_handler.save_query_results(results, filters)
            logger.info(f"\nSaved {saved_count} query results to database table 'query_results'")
        except Exception as e:
            logger.error(f"Error saving query results to database: {str(e)}")
    else:
        logger.info("No results found matching the criteria")

def export_results(db_handler, output_file, logger):
    try:
        db_handler.export_to_csv(output_file)
        logger.info(f"Results exported to: {output_file}")
    except Exception as e:
        logger.error(f"Error exporting results: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description="MS Blood Test Tracker - Process and manage blood test results"
    )
    parser.add_argument('--pdf-dir', type=str, default='data/pdfs')
    parser.add_argument('--query', action='store_true')
    parser.add_argument('--patient', type=str)
    parser.add_argument('--start-date', type=str)
    parser.add_argument('--end-date', type=str)
    parser.add_argument('--category', type=str)
    parser.add_argument('--export', type=str)
    args = parser.parse_args()
    logger = setup_logging()
    logger.info("=== MS Blood Test Tracker Started ===")
    config = Config()
    db_handler = DatabaseHandler(config.database_path)
    db_handler.initialize_database()
    try:
        if args.query:
            query_results(db_handler, args, logger)
        elif args.export:
            export_results(db_handler, args.export, logger)
        else:
            pdf_dir = Path(args.pdf_dir)
            if not pdf_dir.exists():
                logger.error(f"PDF directory not found: {pdf_dir}")
                pdf_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {pdf_dir}")
                logger.info("Please add PDF files to this directory and run again")
                return
            process_pdfs(pdf_dir, db_handler, logger)
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    finally:
        db_handler.close()
        logger.info("=== MS Blood Test Tracker Finished ===")

if __name__ == "__main__":
    main()