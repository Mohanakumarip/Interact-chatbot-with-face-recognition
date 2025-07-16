def detect_intent(text):
    text = text.lower()
    if any(word in text for word in ["weather", "temperature", "climate"]):
        return "weather"
    elif any(word in text for word in ["news", "headlines", "latest news"]):
        return "news"
    elif any(word in text for word in ["location", "distance", "route", "map"]):
        return "location"
    elif any(word in text for word in ["sports", "cricket", "match", "score", "live match"]):
        return "sports"
    elif any(word in text for word in ["exit", "quit", "bye", "stop"]):
        return "exit"
    else:
        return "unknown"