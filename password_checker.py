"""
password_checker.py
--------------------
Checks whether a password has appeared in known public data breaches,
using the "Have I Been Pwned" Pwned Passwords API.

Pure Python standard library - no external dependencies required.

HOW IT WORKS (k-anonymity):
1. We hash the password locally with SHA-1 (never send the raw password anywhere)
2. We send ONLY the first 5 characters of that hash to the API
3. The API returns every hash suffix that starts with those 5 characters,
   plus how many times each one appeared in breaches
4. We check locally whether our full hash is in that returned list

This means the real password (and even the full hash) never leaves your machine.
"""

import hashlib
import urllib.request
import urllib.error


def check_password_pwned(password: str) -> int:
    """
    Returns the number of times this password has appeared in known breaches.
    Returns 0 if it hasn't been found.
    """
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    request = urllib.request.Request(url, headers={"User-Agent": "sentry-security-checker"})

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            text = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"HIBP API error: {exc}")

    for line in text.splitlines():
        line_suffix, count = line.split(":")
        if line_suffix == suffix:
            return int(count)

    return 0


if __name__ == "__main__":
    test_password = input("Enter a password to check: ")
    times_seen = check_password_pwned(test_password)

    if times_seen > 0:
        print(f"WARNING: This password has been seen {times_seen:,} times in known breaches.")
        print("You should NOT use this password anywhere.")
    else:
        print("Not found in known breaches (still use a strong, unique one!).")
