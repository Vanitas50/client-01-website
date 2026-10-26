"""Produktcheck für die Nordwerk-Website (unabhängig von der Factory).

Aufruf:
    python -m unittest test_website -v
oder
    python test_website.py
"""

import unittest
from html.parser import HTMLParser
from pathlib import Path

INDEX = Path(__file__).parent / "index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = ""
        self.title = ""
        self._in_title = False
        self.text_parts = []
        self.hrefs = []
        self.asset_refs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang", "")
        if tag == "title":
            self._in_title = True
        if tag == "a" and attrs.get("href"):
            self.hrefs.append(attrs["href"])
        if tag in ("img", "script", "link") and attrs.get("src"):
            self.asset_refs.append(attrs["src"])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        self.text_parts.append(data)


class NordwerkWebsiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")
        cls.parser = PageParser()
        cls.parser.feed(cls.html)
        cls.text = " ".join(t.strip() for t in cls.parser.text_parts if t.strip())

    def test_language_and_title(self):
        self.assertEqual(self.parser.lang, "de")
        self.assertIn("Nordwerk Industrie-Service", self.parser.title)

    def test_company_name_and_main_statement(self):
        self.assertIn("Nordwerk Industrie-Service", self.text)
        self.assertIn("Praktische Unterstützung für Ihren technischen Betrieb.", self.text)

    def test_one_service_present(self):
        self.assertIn("Wartungsplanung", self.text)
        self.assertIn(
            "Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten",
            self.text,
        )

    def test_contact_link_and_exercise_notice(self):
        self.assertIn("mailto:kontakt@nordwerk.example", self.parser.hrefs)
        self.assertIn("Fiktives Unternehmen – Lehrprojekt der HAW Hamburg", self.text)

    def test_no_external_assets(self):
        for ref in self.parser.asset_refs:
            self.assertFalse(ref.startswith("http://"), ref)
            self.assertFalse(ref.startswith("https://"), ref)
        self.assertNotIn("https://", self.html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
