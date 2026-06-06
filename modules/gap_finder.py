"""
Research gap identification module
"""

class GapFinderModule:
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def identify_gaps(self, texts, is_multi_doc=False):
        """
        Identify research gaps from paper(s)
        
        Args:
            texts: Single text string or list of texts
            is_multi_doc: Whether analyzing multiple documents
            
        Returns:
            Gap analysis
        """
        from prompts.templates import get_prompt
        
        if is_multi_doc and isinstance(texts, list):
            # Multi-document gap analysis
            formatted_texts = []
            for i, text in enumerate(texts, 1):
                cleaned = self._clean_text(text)[:3000]
                formatted_texts.append(f"Paper {i}:\n{cleaned}\n")
            
            combined_texts = "\n---\n".join(formatted_texts)
            prompt = get_prompt("gap_multi", texts=combined_texts)
        else:
            # Single document gap analysis
            if isinstance(texts, list):
                texts = texts[0]
            cleaned_text = self._clean_text(texts)[:6000]
            prompt = get_prompt("gap_single", text=cleaned_text)
        
        response = self.llm_client.generate(prompt)
        return response
    
    def _clean_text(self, text):
        import re
        text = re.sub(r'\s+', ' ', text)
        return text.strip()