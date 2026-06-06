"""
Comparison module for multiple research papers
"""

class ComparerModule:
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def compare_papers(self, papers_texts):
        """
        Compare multiple research papers
        
        Args:
            papers_texts: List of paper texts
            
        Returns:
            Comparison analysis
        """
        from prompts.templates import get_prompt
        
        if len(papers_texts) < 2:
            return "Need at least 2 papers for comparison."
        
        if len(papers_texts) > 5:
            papers_texts = papers_texts[:5]
        
        # Format papers for prompt
        formatted_papers = []
        for i, text in enumerate(papers_texts, 1):
            cleaned = self._clean_text(text)[:4000]
            formatted_papers.append(f"Paper {i}:\n{cleaned}\n")
        
        prompt = get_prompt("compare", paper1=formatted_papers[0], paper2=formatted_papers[1])
        
        response = self.llm_client.generate(prompt)
        
        return response
    
    def _clean_text(self, text):
        import re
        text = re.sub(r'\s+', ' ', text)
        return text.strip()