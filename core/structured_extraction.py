import os
try:
    import langextract as lx
    LANGEXTRACT_AVAILABLE = True
except ImportError:
    LANGEXTRACT_AVAILABLE = False

class StructuredExtractor:
    """
    Wrapper for LangExtract to perform structured information extraction 
    using LLMs as per the official documentation.
    """
    def __init__(self, model_id="gemini-2.5-flash"):
        self.model_id = model_id
        if not LANGEXTRACT_AVAILABLE:
            print("Warning: langextract library is not installed.")

    def extract(self, text_or_doc, prompt_description, examples):
        """
        Extracts structured data from text or documents.
        
        Args:
            text_or_doc (str): Input text or URL/path to document.
            prompt_description (str): Description of what to extract.
            examples (list): List of lx.data.ExampleData objects.
        """
        if not LANGEXTRACT_AVAILABLE:
            return {"error": "langextract library is missing."}
        
        try:
            result = lx.extract(
                text_or_documents=text_or_doc,
                prompt_description=prompt_description,
                examples=examples,
                model_id=self.model_id
            )
            return result
        except Exception as e:
            return {"error": f"Extraction failed: {str(e)}"}