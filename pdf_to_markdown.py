import logging
from dotenv import load_dotenv
from llama_parse import LlamaParse
from pathlib import Path
import os
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_pdf_to_markdown(pdf_path: str, output_path: str = None) -> None:
    """
    Convert a PDF file to Markdown format using LlamaParse.
    
    Args:
        pdf_path (str): Path to the input PDF file
        output_path (str, optional): Path for the output Markdown file. If not provided,
                                   will use the same name as PDF with .md extension
    
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        ValueError: If the input file is not a PDF or if LLAMA_CLOUD_API_KEY is not set
        PermissionError: If there are file permission issues
    """
    # Load environment variables from the same directory as the script
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)
    
    # Check for API key
    api_key = os.getenv('LLAMA_CLOUD_API_KEY')
    if not api_key:
        raise ValueError("LLAMA_CLOUD_API_KEY environment variable is not set")
    
    # Validate input file is a PDF
    pdf_path = Path(pdf_path).resolve()
    if not pdf_path.suffix.lower() == '.pdf':
        raise ValueError(f"Input file must be a PDF: {pdf_path}")
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    if not pdf_path.is_file():
        raise ValueError(f"Path exists but is not a file: {pdf_path}")
    
    # Check read permissions
    if not os.access(pdf_path, os.R_OK):
        raise PermissionError(f"No read permission for file: {pdf_path}")
    
    logging.info(f"Processing PDF file: {pdf_path}")
    
    try:
        # Initialize LlamaParse with API key
        parser = LlamaParse(
            api_key=api_key,
            result_type="markdown",
            verbose=True,            # Enable verbose logging
            premium_mode=True,       # Keep this for accuracy
            continuous_mode=True     # Keep this for proper text flow
        )
        
        # Process the PDF
        documents = parser.load_data(str(pdf_path))
        
        if not documents:
            raise ValueError("No content was extracted from the PDF")
        
        # Prepare output path
        output_path = Path(output_path).resolve() if output_path else pdf_path.with_suffix('.md')
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check write permissions for output directory
        if not os.access(output_path.parent, os.W_OK):
            raise PermissionError(f"No write permission for directory: {output_path.parent}")
        
        # Write the markdown content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(documents[0].text)
        
        logging.info(f"Successfully converted PDF to Markdown: {output_path}")
            
    except Exception as e:
        logging.error(f"Failed to convert PDF: {str(e)}")
        raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Convert PDF to Markdown using LlamaParse')
    parser.add_argument('pdf_path', help='Path to the PDF file to convert')
    parser.add_argument('--output', '-o', help='Path for the output markdown file')
    
    try:
        args = parser.parse_args()
        parse_pdf_to_markdown(args.pdf_path, args.output)
    except Exception as e:
        logging.error(f"Conversion failed: {str(e)}")
        sys.exit(1)
