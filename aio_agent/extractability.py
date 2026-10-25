import re
from pathlib import Path
from html.parser import HTMLParser

class ExtractabilityAuditor:
    """Audits HTML pages for single H1 tag and concise 35-70 word direct answer blocks."""

    def __init__(self, min_words: int = 35, max_words: int = 70):
        self.min_words = min_words
        self.max_words = max_words

    def audit_content(self, html_text: str) -> dict:
        # Check H1 tags
        h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', html_text, re.IGNORECASE | re.DOTALL)
        h1_count = len(h1_matches)
        h1_text = re.sub(r'<[^>]+>', '', h1_matches[0]).strip() if h1_count > 0 else ""

        # Extract quick answer paragraph
        # First look for class="quick-answer" or class="direct-answer"
        qa_match = re.search(r'<p[^>]*class=["\'][^"\']*(?:quick-answer|direct-answer)[^"\']*["\'][^>]*>(.*?)</p>', html_text, re.IGNORECASE | re.DOTALL)
        if not qa_match:
            # Fallback: look for the first paragraph directly following </h1>
            qa_match = re.search(r'</h1>\s*(?:<div[^>]*>)?\s*<p[^>]*>(.*?)</p>', html_text, re.IGNORECASE | re.DOTALL)
        
        answer_text = ""
        word_count = 0
        is_valid_answer = False

        if qa_match:
            answer_text = re.sub(r'<[^>]+>', '', qa_match.group(1)).strip()
            # remove whitespace normalization
            words = answer_text.split()
            word_count = len(words)
            is_valid_answer = self.min_words <= word_count <= self.max_words

        passed = (h1_count == 1) and is_valid_answer
        return {
            "h1_count": h1_count,
            "h1_text": h1_text,
            "has_single_h1": (h1_count == 1),
            "quick_answer_text": answer_text,
            "word_count": word_count,
            "is_valid_length": is_valid_answer,
            "passed": passed,
        }

    def audit_file(self, file_path: str | Path) -> dict:
        path = Path(file_path)
        if not path.is_file():
            return {"file": str(file_path), "error": "File not found", "passed": False}
        html_text = path.read_text(encoding="utf-8")
        result = self.audit_content(html_text)
        result["file"] = str(file_path)
        return result
