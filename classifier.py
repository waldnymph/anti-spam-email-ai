
def classify_email(text):
    text = text.lower()

    if any(x in text for x in ["security", "login", "вход", "authentication", "2fa", "оповещение"]):
        return "important"

    if any(x in text for x in ["welcome", "newsletter", "digest", "unsubscribe", "подписка"]):
        return "newsletter"

    if any(x in text for x in ["sale", "discount", "скидк", "offer", "%", "акция"]):
        return "promo"

    if any(x in text for x in ["secret", "learn", "course", "магистрат", "training"]):
        return "informational"

    return "personal"