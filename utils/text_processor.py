"""
Text processing utilities
"""

import re
from typing import List, Dict

class TextProcessor:
    
    @staticmethod
    def extract_abstract(text: str) -> str:
        """Extract abstract from research paper text"""
        # Try to find abstract section
        patterns = [
            r'abstract[:\s]+(.*?)(?=\n\s*\n|\n(?:introduction|1\.|i\.))',
            r'ABSTRACT[:\s]+(.*?)(?=\n\s*\n|\n(?:INTRODUCTION|1\.|I\.))',
            r'<abstract>(.*?)</abstract>',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                abstract = match.group(1).strip()
                if len(abstract) > 100:
                    return abstract
        
        # Return first 500 characters as fallback
        return text[:500] + "..."
    
    @staticmethod
    def extract_title(text: str) -> str:
        """Extract title from research paper text"""
        # First line is often the title
        lines = text.strip().split('\n')
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) < 200 and not line.startswith(('Abstract', 'ABSTRACT')):
                return line
        return "Untitled"
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 3000) -> List[str]:
        """Split text into chunks"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            current_length += len(word) + 1
            if current_length > chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    @staticmethod
    def process_user_query(query: str) -> Dict:
        """Process and classify user query"""
        query_lower = query.lower()
        
        # Task classification
        if any(word in query_lower for word in ['summarize', 'summary', 'brief']):
            return {'task': 'summarize', 'confidence': 'high'}
        elif any(word in query_lower for word in ['extract', 'key information', 'details']):
            return {'task': 'extract', 'confidence': 'high'}
        elif any(word in query_lower for word in ['compare', 'comparison', 'versus', 'vs']):
            return {'task': 'compare', 'confidence': 'high'}
        elif any(word in query_lower for word in ['gap', 'future direction', 'missing', 'identify']):
            return {'task': 'gap', 'confidence': 'high'}
        elif any(word in query_lower for word in ['question', 'what is', 'explain', 'how does']):
            return {'task': 'qa', 'confidence': 'medium'}
        else:
            return {'task': 'summarize', 'confidence': 'low'}