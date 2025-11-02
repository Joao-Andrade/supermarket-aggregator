from ..base_collector import BaseCollector
import ..utils.requests as req

class ContinenteCollector(BaseCollector):
    
    def fetch(self, query: str) -> str:
        req.request_page(self.base_url+"")
