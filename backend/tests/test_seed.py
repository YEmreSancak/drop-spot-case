from app.utils.seed import derive_coefficients, calculate_priority_score

def test_priority_score_deterministic():
    seed = "abcdef123456"
    A, B, C = derive_coefficients(seed)
    assert isinstance(A, int)
    assert isinstance(B, int)
    assert isinstance(C, int)

    score1 = calculate_priority_score(seed, base=100, signup_latency_ms=321, account_age_days=12, rapid_actions=4)
    score2 = calculate_priority_score(seed, base=100, signup_latency_ms=321, account_age_days=12, rapid_actions=4)
    assert score1 == score2  # deterministik sonuç
