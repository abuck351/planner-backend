import websoc.settings as websoc


def parse_year_term(term_str: str):
    """
    See TERM_MAP in websoc.settings.py for how to format term_str
    """
    year, term = term_str.split("-")
    return f"{year}-{websoc.TERM_MAP[term]}"
