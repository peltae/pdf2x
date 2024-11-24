# pdf2x

Convert PDF documents to Markdown, Text, or JSON using LlamaParse API.

## Setup

1. Get your API key from [LlamaParse](https://cloud.llamaindex.ai/)
2. Install dependencies: `pip install -r requirements.txt`
3. Rename `.env.example` to `.env` and add your API key

## Usage

Basic conversion (defaults to markdown):
```bash
python pdf2x.py input.pdf
```

Specify format (markdown, text, or json):
```bash
python pdf2x.py input.pdf --format text
```

Custom output path:
```bash
python pdf2x.py input.pdf -o output.md --format markdown
```

## License

MIT License - see [LICENSE](LICENSE) file