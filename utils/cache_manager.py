"""
Cache manager for storing and retrieving analysis results
"""

import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any


class CacheManager:
    """Manage caching of analysis results"""
    
    def __init__(self, cache_dir: str = ".cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.ttl = timedelta(hours=ttl_hours)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_key(self, text: str, task: str, params: Dict = None) -> str:
        """Generate cache key from input"""
        content = f"{text[:1000]}_{task}_{json.dumps(params or {}, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, text: str, task: str, params: Dict = None) -> Optional[str]:
        """Get cached result if available and not expired"""
        key = self._get_key(text, task, params)
        cache_file = self.cache_dir / f"{key}.json"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                data = json.load(f)
            
            cache_time = datetime.fromisoformat(data['timestamp'])
            if datetime.now() - cache_time < self.ttl:
                return data['result']
        
        return None
    
    def set(self, text: str, task: str, result: str, params: Dict = None):
        """Store result in cache"""
        key = self._get_key(text, task, params)
        cache_file = self.cache_dir / f"{key}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'result': result,
            'text_preview': text[:200]
        }
        
        with open(cache_file, 'w') as f:
            json.dump(data, f)
    
    def clear(self):
        """Clear all cache files"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        files = list(self.cache_dir.glob("*.json"))
        return {
            'total_cached': len(files),
            'cache_size_mb': sum(f.stat().st_size for f in files) / (1024 * 1024)
        }