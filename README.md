# DropSpot – Limited Stock & Waitlist Platform (Case Study)

> Project start time: 2025-11-08 00:05 (UTC+3)

This project is developed for Alpaco Full-Stack Developer Case.

## Description
Full-stack engineering assignment for Alpaco. Includes user auth, waitlist logic, claim window processing, admin CRUD, idempotent operations, and seed-based priority scoring.

## First Commit
- Repository initialized  
- Project skeleton created

### 🧮 Seed & Priority Score

Each project instance generates a unique **seed** value using:

remote_url | first_commit_epoch | start_time

This seed (first 12 hex chars of SHA256) determines coefficients A, B, C:

A = 7 + (int(seed[0:2],16) % 5)
B = 13 + (int(seed[2:4],16) % 7)
C = 3 + (int(seed[4:6],16) % 3)


Priority Score formula:

priority_score = base + (signup_latency_ms % A) + (account_age_days % B) - (rapid_actions % C)

This ensures each candidate’s instance has a deterministic yet personalized scoring pattern.
