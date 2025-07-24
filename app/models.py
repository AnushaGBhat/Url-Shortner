from datetime import datetime
url_store = {}

class ShortURL:
    def __init__(self, original_url, short_code):
        self.original_url = original_url
        self.short_code = short_code
        self.created_at = datetime.utcnow()
        self.clicks = 0

    def to_dict(self):
        return {
            "original_url": self.original_url,
            "short_code": self.short_code,
            "created_at": self.created_at.isoformat(),
            "clicks": self.clicks
        }
