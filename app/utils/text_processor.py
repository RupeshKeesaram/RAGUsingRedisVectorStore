import re
from langchain_community.document_loaders import PyPDFLoader
from typing import List

class TextProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans the input text by:
        - Removing special characters that are not relevant to English text.
        - Replacing consecutive periods, commas, exclamation marks, or question marks with a single one.
        - Collapsing multiple spaces into a single space.
        - Removing leading and trailing whitespace.
        """
        text = re.sub(r"[^\w\s\.\,\?\!\-']", "", text)
        
        text = re.sub(r"(\.{2,})", ".", text)  
        text = re.sub(r"(\,{2,})", ",", text)  
        text = re.sub(r"(\!{2,})", "!", text)  
        text = re.sub(r"(\?{2,})", "?", text)  
        
        text = re.sub(r"\s+", " ", text)
        
        return text.strip()

text_processor = TextProcessor() 