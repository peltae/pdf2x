import logging
from dotenv import load_dotenv
from llama_parse import LlamaParse
from pathlib import Path
import os
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_pdf(pdf_path: str, output_path: str = None, format: str = "markdown") -> None:
    """
    Convert a PDF file to the specified format using LlamaParse.
    
    Args:
        pdf_path (str): Path to the input PDF file
        output_path (str, optional): Path for the output file. If not provided,
                                   will use the same name as PDF with appropriate extension
        format (str, optional): Output format - one of "markdown", "text", or "json"
    
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
    
    # Validate format
    format = format.lower()
    if format not in ["markdown", "text", "json"]:
        raise ValueError(f"Unsupported format: {format}. Use 'markdown', 'text', or 'json'")
    
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
            result_type=format,
            verbose=True,            # Enable verbose logging
            premium_mode=True,       # Keep this for accuracy
            continuous_mode=True     # Keep this for proper text flow
        )
        
        # Process the PDF
        documents = parser.load_data(str(pdf_path))
        
        if not documents:
            raise ValueError("No content was extracted from the PDF")
        
        # Determine output extension based on format
        extensions = {
            "markdown": ".md",
            "text": ".txt",
            "json": ".json"
        }
        
        # Prepare output path
        if output_path:
            output_path = Path(output_path).resolve()
        else:
            output_path = pdf_path.with_suffix(extensions[format])
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check write permissions for output directory
        if not os.access(output_path.parent, os.W_OK):
            raise PermissionError(f"No write permission for directory: {output_path.parent}")
        
        # Write the content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(documents[0].text)
        
        logging.info(f"Successfully converted PDF to {format.upper()}: {output_path}")
            
    except Exception as e:
        logging.error(f"Failed to convert PDF: {str(e)}")
        raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Convert PDF to various formats using LlamaParse')
    parser.add_argument('pdf_path', help='Path to the PDF file to convert')
    parser.add_argument('--output', '-o', help='Path for the output file')
    parser.add_argument('--format', '-f', choices=['markdown', 'text', 'json'], 
                       default='markdown', help='Output format (default: markdown)')
    
    try:
        args = parser.parse_args()
        parse_pdf(args.pdf_path, args.output, args.format)
    except Exception as e:
        logging.error(f"Conversion failed: {str(e)}")
        sys.exit(1) 