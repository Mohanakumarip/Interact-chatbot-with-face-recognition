def detect_intent(prompt):
    prompt = prompt.lower()
    if "weather" in prompt:
        return "weather"
    elif "news" in prompt:
        return "news"
    elif "score" in prompt or "cricket" in prompt:
        return "sports"
    elif "distance" in prompt:
        return "location"
    elif "total employees" in prompt or "employee count" in prompt:
        return "employee_count"
    elif "department" in prompt:
        return "department"
    elif "birthdays in" in prompt:
        return "birthdays"
    elif "upcoming birthday" in prompt:
        return "upcoming_birthdays"
    return "unknown"
