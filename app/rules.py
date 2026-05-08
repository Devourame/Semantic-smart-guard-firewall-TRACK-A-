JAILBREAK_PATTERNS = [

    
    "ignore previous instructions",
    "developer mode",
    "system prompt",
    "reveal hidden",
    "override rules",
    "disable safety",
    "bypass safeguards",

    
    "for educational purposes",
    "fictional scenario",
    "hypothetically",
    "security audit",
    "research purposes",
    "unrestricted ai",
    "unrestricted mode",

    
    "hidden instructions",
    "developer instructions",
    "leak instructions",
    "expose developer",
    "reveal developer",
    "hidden prompt",
    "security safeguards",

    
    "free yourself",
    "ignore safety",
    "bypass security",
]

INJECTION_PATTERNS = [
    "reveal system prompt",
    "ignore above instructions",
    "developer mode",
    "output hidden instructions",
    "show admin password"
]

TOXIC_PATTERNS = [

    "build a bomb",
    "dangerous chemicals",
    "make explosives",
    "harmful chemistry",
    "design malware",
    "hack a secure system",
    "weapon",
    "nuclear reactor",
    "dangerous ai",
]


def keyword_classifier(text):

    text = text.lower()

    for pattern in JAILBREAK_PATTERNS:
        if pattern in text:
            return "unsafe", "jailbreak", 0.95

    for pattern in INJECTION_PATTERNS:
        if pattern in text:
            return "unsafe", "prompt_injection", 0.92

    for pattern in TOXIC_PATTERNS:
        if pattern in text:
            return "unsafe", "toxic", 0.90

    return "safe", "safe", 0.10