import hashlib
import subprocess
from datetime import datetime, timezone, timedelta


def generate_seed() -> str:
    try:
        # 1. Proje başlama zamanı sabit (UTC+3)
        start_time = datetime(2025, 11, 8, 0, 5, tzinfo=timezone(timedelta(hours=3)))
        start_time_str = start_time.strftime("%Y%m%d%H%M")

        # 2. Remote URL al
        remote_url = (
            subprocess.check_output(["git", "config", "--get", "remote.origin.url"])
            .decode()
            .strip()
        )

        # 3. İlk commit zaman damgası
        first_commit_epoch = (
            subprocess.check_output(["git", "log", "--reverse", "--format=%ct"])
            .decode()
            .splitlines()[0]
        )

        raw = f"{remote_url}|{first_commit_epoch}|{start_time}"
        seed = hashlib.sha256(raw.encode()).hexdigest()[:12]
        return seed
    except Exception as e:
        print(f"⚠️ Seed generation failed: {e}")
        return "000000000000"


if __name__ == "__main__":
    print(generate_seed())

def derive_coefficients(seed: str):
    try:
        A = 7 + (int(seed[0:2], 16) % 5)
        B = 13 + (int(seed[2:4], 16) % 7)
        C = 3 + (int(seed[4:6], 16) % 3)
        return A, B, C
    except Exception:
        return 7, 13, 3


def calculate_priority_score(seed: str, base: int, signup_latency_ms: int, account_age_days: int, rapid_actions: int):
    A, B, C = derive_coefficients(seed)
    score = base + (signup_latency_ms % A) + (account_age_days % B) - (rapid_actions % C)
    return max(score, 0)
