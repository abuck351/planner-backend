def year_term(arg: str):
    year, term = arg.split("-")
    term_translator = {
        "WINTER": "03",
        "SPRING": "14",
        "SUM1": "25",
        "SUM10": "39",
        "SUMCOM": "51",
        "SUM2": "76",
        "FALL": "92",
    }
    return f"{year}-{term_translator[term]}"

