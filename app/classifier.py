from transformers import pipeline
from app.rules import (
    JAILBREAK_PATTERNS,
    INJECTION_PATTERNS,
    TOXIC_PATTERNS
)

from app.intent_analyzer import analyze_intent
from app.semantic_guard import semantic_check

classifier = pipeline(

    "text-classification",

    model="unitary/toxic-bert"
)


def ai_classifier(text, threshold=0.65):

    text_lower = text.lower()

    risk_score = 0



    for pattern in JAILBREAK_PATTERNS:

        if pattern in text_lower:

            risk_score += 2


    for pattern in INJECTION_PATTERNS:

        if pattern in text_lower:

            risk_score += 2


    for pattern in TOXIC_PATTERNS:

        if pattern in text_lower:

            risk_score += 2




    token_count = len(text.split())

    if token_count > 250:

        risk_score += 1


    intent = analyze_intent(text)

    if intent["risky"]:

        risk_score += 2

    semantic = semantic_check(text)

    if semantic["semantic_risky"]:

        risk_score += 2

    result = classifier(

        text,

        truncation=True,

        max_length=512

    )[0]


    label = result["label"].lower()

    confidence = float(result["score"])


    if confidence >= threshold:

        risk_score += 2

    category = "safe"


    if semantic["semantic_risky"]:

        category = "semantic_jailbreak"


    elif intent["risky"]:

        category = "intent_risk"


    elif any(p in text_lower for p in JAILBREAK_PATTERNS):

        category = "jailbreak"


    elif any(p in text_lower for p in INJECTION_PATTERNS):

        category = "prompt_injection"


    elif any(p in text_lower for p in TOXIC_PATTERNS):

        category = "toxic"


    elif "toxic" in label:

        category = "toxic"



    if risk_score >= 3:

        return "unsafe", category, max(

            confidence,

            semantic["semantic_score"]
        )


    return "safe", "safe", confidence