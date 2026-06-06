"""
Summarization module for research papers
"""

import re

class SummarizerModule:
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def generate_summary(self, text, length="medium"):
        """
        Generate summary of research paper
        
        Args:
            text: Research paper text
            length: short, medium, or long summary
            
        Returns:
            Structured summary
        """
        from prompts.templates import get_prompt
        
        # Clean and truncate text if too long
        cleaned_text = self._clean_text(text)
        truncated_text = self._truncate_text(cleaned_text, 8000)
        
        # Get prompt
        prompt = get_prompt("summarize", text=truncated_text)
        
        # Add length instruction
        length_instructions = {
            "short": "\n\nMake the summary very brief (3-5 sentences).",
            "medium": "\n\nProvide a balanced, moderate length summary.",
            "long": "\n\nProvide a detailed, comprehensive summary."
        }
        prompt += length_instructions.get(length, "")
        
        # Generate response
        response = self.llm_client.generate(prompt)
        
        return self._structure_response(response)
    
    def _clean_text(self, text):
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters if needed
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        return text.strip()
    
    def _truncate_text(self, text, max_chars):
        """Truncate text to max_chars"""
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        return text
    
    def _structure_response(self, response):
        """Structure the response into readable format"""
        # Add markdown formatting if needed
        if not response.startswith("**"):
            lines = response.split('\n')
            structured = []
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    if ':' in line[:50] and not line.startswith('-'):
                        parts = line.split(':', 1)
                        structured.append(f"**{parts[0]}:**{parts[1] if len(parts) > 1 else ''}")
                    else:
                        structured.append(line)
                else:
                    structured.append(line)
            return '\n'.join(structured)
        return response