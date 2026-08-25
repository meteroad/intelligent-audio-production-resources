#!/usr/bin/env python3
"""Resolve a concise publication venue from authoritative arXiv metadata."""

from __future__ import annotations

import re


ACCEPTANCE_MARKERS = re.compile(
    r"\b(?:accepted|to appear|forthcoming|published|camera[- ]ready|presented)\b",
    re.IGNORECASE,
)
NON_ACCEPTANCE_MARKERS = re.compile(
    r"\b(?:submitted|submission|under review|work in progress)\b",
    re.IGNORECASE,
)

ACRONYM_NAMES = {
    "ismir": "ISMIR",
    "icassp": "ICASSP",
    "dafx": "DAFx",
    "waspaa": "WASPAA",
    "eusipco": "EUSIPCO",
    "interspeech": "INTERSPEECH",
    "icml": "ICML",
    "neurips": "NeurIPS",
    "iclr": "ICLR",
    "aaai": "AAAI",
    "ijcai": "IJCAI",
    "mmsp": "MMSP",
    "mlsp": "MLSP",
    "smc": "SMC",
    "taslp": "IEEE/ACM TASLP",
}

ACRONYM_PATTERN = re.compile(
    r"\b(?P<name>ISMIR|ICASSP|DAFx|WASPAA|EUSIPCO|INTERSPEECH|ICML|NeurIPS|ICLR|AAAI|IJCAI|MMSP|MLSP|SMC|TASLP)"
    r"(?:\s*(?:conference|workshop))?\W*(?P<year>(?:20)?\d{2})?\b",
    re.IGNORECASE,
)

FULL_CONFERENCE_PATTERNS = (
    (re.compile(r"international conference on music information retrieval", re.IGNORECASE), "ISMIR"),
    (re.compile(r"international society for music information retrieval conference", re.IGNORECASE), "ISMIR"),
    (re.compile(r"international conference on acoustics,? speech,? and signal processing", re.IGNORECASE), "ICASSP"),
    (re.compile(r"international conference on digital audio effects", re.IGNORECASE), "DAFx"),
    (re.compile(r"workshop on applications of signal processing to audio and acoustics", re.IGNORECASE), "WASPAA"),
    (re.compile(r"european signal processing conference", re.IGNORECASE), "EUSIPCO"),
    (re.compile(r"international conference on machine learning", re.IGNORECASE), "ICML"),
    (re.compile(r"international conference on learning representations", re.IGNORECASE), "ICLR"),
    (re.compile(r"conference on neural information processing systems", re.IGNORECASE), "NeurIPS"),
    (re.compile(r"acm(?: international conference on)? multimedia", re.IGNORECASE), "ACM MM"),
)

JOURNAL_PATTERNS = (
    (re.compile(r"\bJAES\b|journal of the audio engineering society", re.IGNORECASE), "JAES"),
    (re.compile(r"journal of the acoustical society of america", re.IGNORECASE), "JASA"),
    (
        re.compile(r"(?:EURASIP )?journal on audio,? speech,? and music processing|J Audio Speech and Music Process", re.IGNORECASE),
        "EURASIP Journal on Audio, Speech, and Music Processing",
    ),
    (re.compile(r"IEEE/ACM transactions on audio,? speech,? and language processing", re.IGNORECASE), "IEEE/ACM TASLP"),
)

JOURNAL_VENUE_PREFIXES = (
    "JAES",
    "JASA",
    "EURASIP Journal",
    "IEEE/ACM TASLP",
)


def compact_text(value: str | None) -> str:
    return " ".join((value or "").split())


def normalized_year(value: str | None) -> str | None:
    if not value:
        return None
    year = int(value)
    if year < 100:
        year += 2000
    return str(year) if 2000 <= year <= 2099 else None


def year_in(text: str, preferred: str | None = None) -> str | None:
    year = normalized_year(preferred)
    if year:
        return year
    match = re.search(r"\b(20\d{2})\b", text)
    return match.group(1) if match else None


def with_year(name: str, year: str | None) -> str:
    return f"{name} {year}" if year else name


def known_venue(text: str) -> str | None:
    acronym = ACRONYM_PATTERN.search(text)
    if acronym:
        name = ACRONYM_NAMES[acronym.group("name").casefold()]
        return with_year(name, year_in(text, acronym.group("year")))

    for pattern, name in FULL_CONFERENCE_PATTERNS:
        if pattern.search(text):
            return with_year(name, year_in(text))

    aes = re.search(
        r"\bAES(?: International)?(?: Audio)? Convention\b|\bConvention of the Audio Engineering Society\b",
        text,
        re.IGNORECASE,
    )
    if aes:
        return with_year("AES Convention", year_in(text))

    for pattern, name in JOURNAL_PATTERNS:
        if pattern.search(text):
            return with_year(name, year_in(text))
    return None


def venue_from_doi(doi: str | None) -> str | None:
    value = compact_text(doi).casefold()
    if value.startswith("10.17743/jaes"):
        return "JAES"
    if value.startswith("10.1121/"):
        return "JASA"
    if value.startswith("10.1186/s13636"):
        return "EURASIP Journal on Audio, Speech, and Music Processing"
    return None


def semantic_scholar_venue(record: dict | None) -> tuple[str | None, str | None]:
    if not record:
        return None, None
    publication_venue = record.get("publicationVenue") or {}
    venue_name = compact_text(publication_venue.get("name") or record.get("venue"))
    if not venue_name or venue_name.casefold() in {"arxiv", "arxiv.org", "corr"}:
        return None, None

    external_ids = record.get("externalIds") or {}
    doi = compact_text(external_ids.get("DOI"))
    venue_type = compact_text(publication_venue.get("type")).casefold()
    year = normalized_year(str(record["year"])) if isinstance(record.get("year"), int) else None
    dblp = compact_text(external_ids.get("DBLP"))
    if venue_type == "conference":
        year = year_in(doi)
    if venue_type == "conference" and not year and dblp.startswith("conf/"):
        match = re.search(r"(\d{2})[a-z]?$", dblp, re.IGNORECASE)
        year = normalized_year(match.group(1)) if match else None

    canonical = known_venue(with_year(venue_name, year))
    return canonical or with_year(venue_name, year), "semanticScholar"


def semantic_scholar_doi(record: dict | None) -> str | None:
    if not record:
        return None
    return compact_text((record.get("externalIds") or {}).get("DOI")) or None


def resolve_publication_venue(
    journal_reference: str | None,
    comment: str | None,
    doi: str | None = None,
) -> tuple[str | None, str | None]:
    """Return ``(venue, evidence)`` without inferring acceptance from submission text."""

    reference = compact_text(journal_reference)
    if reference:
        return known_venue(reference) or reference, "journalReference"

    doi_venue = venue_from_doi(doi)
    if doi_venue:
        return doi_venue, "doi"

    comment_text = compact_text(comment)
    if comment_text:
        venue = known_venue(comment_text)
        explicitly_accepted = bool(ACCEPTANCE_MARKERS.search(comment_text))
        explicitly_unaccepted = bool(NON_ACCEPTANCE_MARKERS.search(comment_text))
        bare_conference_declaration = bool(venue) and not venue.startswith(JOURNAL_VENUE_PREFIXES)
        if venue and (explicitly_accepted or (not explicitly_unaccepted and bare_conference_declaration)):
            return venue, "comment"
    return None, None
