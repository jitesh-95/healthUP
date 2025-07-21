def parse_suggestions(suggestions):
    if isinstance(suggestions, str):
        return [s.strip("-• ").strip() for s in suggestions.strip().split("\n") if s.strip()]
    elif isinstance(suggestions, list):
        return [s.strip("-• ").strip() for s in suggestions if isinstance(s, str) and s.strip()]
    return []
