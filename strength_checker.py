"""
strength_checker.py
--------------------
Scores password strength independently of breach data.

A password can be "not found in any breach" and still be weak
(e.g. a brand-new predictable pattern nobody has leaked yet).
This module checks HOW HARD a password would be to guess or crack,
based on length, character variety, and common weak patterns.
"""

import re
import math

# A small list of common weak patterns / substitutions attackers try first.
# (Not exhaustive - real tools use huge wordlists, but this covers the
# most common student/beginner mistakes for demo purposes.)
COMMON_PATTERNS = [
    r"123456", r"password", r"qwerty", r"letmein", r"admin",
    r"welcome", r"iloveyou", r"abc123", r"111111", r"000000",
]

KEYBOARD_WALKS = ["qwerty", "asdf", "zxcv", "12345", "09876"]


def _has_common_pattern(password: str) -> bool:
    lowered = password.lower()
    return any(pattern in lowered for pattern in COMMON_PATTERNS + KEYBOARD_WALKS)


def _character_pool_size(password: str) -> int:
    """Estimate how large the character set is, for entropy calculation."""
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"[0-9]", password):
        pool += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        pool += 32  # rough estimate for symbols
    return pool or 1


def estimate_crack_time_seconds(password: str) -> float:
    """
    Very rough entropy-based estimate:
    entropy_bits = length * log2(pool_size)
    guesses = 2^entropy_bits
    Assume an attacker can try 10 billion guesses/sec (offline GPU attack).
    """
    pool = _character_pool_size(password)
    entropy_bits = len(password) * math.log2(pool)
    guesses = 2 ** entropy_bits
    guesses_per_second = 10_000_000_000  # 10 billion/sec, realistic for offline hash cracking
    return guesses / guesses_per_second


def format_duration(seconds: float) -> str:
    """Turn a big number of seconds into a human-readable string."""
    if seconds < 1:
        return "instantly"
    intervals = [
        ("years", 60 * 60 * 24 * 365),
        ("days", 60 * 60 * 24),
        ("hours", 60 * 60),
        ("minutes", 60),
        ("seconds", 1),
    ]
    for name, count in intervals:
        value = seconds / count
        if value >= 1:
            if value > 1_000_000:
                return f"over {value:,.0f} {name} (essentially uncrackable with today's tech)"
            return f"about {value:,.1f} {name}"
    return "instantly"


def score_password_strength(password: str) -> dict:
    """
    Returns a dict with: score (0-100), rating, crack_time, and reasons.
    """
    reasons = []
    score = 0

    length = len(password)
    if length >= 16:
        score += 40
    elif length >= 12:
        score += 30
    elif length >= 8:
        score += 15
        reasons.append("Password is on the shorter side (8-11 chars) - longer is stronger.")
    else:
        reasons.append("Password is very short (<8 chars) - easy to brute-force.")

    pool = _character_pool_size(password)
    if pool >= 90:
        score += 30
    elif pool >= 62:
        score += 20
        reasons.append("Consider adding symbols for more character variety.")
    else:
        score += 5
        reasons.append("Uses a small character set (e.g. only lowercase) - easy to guess.")

    if _has_common_pattern(password):
        score -= 30
        reasons.append("Contains a common word or keyboard pattern attackers try first.")

    if re.fullmatch(r"[A-Za-z]+\d+", password) or re.fullmatch(r"[A-Za-z]+\d+[^A-Za-z0-9]?", password):
        reasons.append("Follows a predictable 'word + numbers' pattern.")
        score -= 10

    score = max(0, min(100, score))

    if score >= 80:
        rating = "Strong"
    elif score >= 50:
        rating = "Moderate"
    elif score >= 25:
        rating = "Weak"
    else:
        rating = "Very Weak"

    crack_seconds = estimate_crack_time_seconds(password)

    return {
        "score": score,
        "rating": rating,
        "estimated_crack_time": format_duration(crack_seconds),
        "reasons": reasons or ["No major weaknesses detected in structure."],
    }


if __name__ == "__main__":
    test_password = input("Enter a password to score: ")
    result = score_password_strength(test_password)

    print(f"\nStrength: {result['rating']} ({result['score']}/100)")
    print(f"Estimated time to crack (offline attack): {result['estimated_crack_time']}")
    print("Notes:")
    for reason in result["reasons"]:
        print(f"  - {reason}")
