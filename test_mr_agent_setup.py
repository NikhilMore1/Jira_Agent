#!/usr/bin/env python3
"""
test_mr_agent_setup.py
──────────────────────
Test script to validate MR Agent configuration
"""

import os
import sys
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_OWNER = os.getenv("GITHUB_OWNER", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "")
GITHUB_API_URL = os.getenv("GITHUB_API_URL", "https://api.github.com")

print("\n" + "═" * 70)
print("🔀 MR Agent Setup Validator")
print("═" * 70)

# Test 1: Check environment variables
print("\n1️⃣  Checking Environment Variables...")
print("─" * 70)

checks = {
    "GITHUB_TOKEN": bool(GITHUB_TOKEN),
    "GITHUB_OWNER": bool(GITHUB_OWNER),
    "GITHUB_REPO": bool(GITHUB_REPO),
}

for var, status in checks.items():
    emoji = "✅" if status else "❌"
    value = os.getenv(var, "")
    masked = (value[:10] + "...") if value and var == "GITHUB_TOKEN" else value
    print(f"   {emoji} {var:<20} : {masked or 'NOT SET'}")

missing = [k for k, v in checks.items() if not v]
if missing:
    print(f"\n   ⚠️  Missing: {', '.join(missing)}")
    print(f"   Add them to .env file")

# Test 2: Validate GitHub Token
if GITHUB_TOKEN:
    print("\n2️⃣  Validating GitHub Token...")
    print("─" * 70)

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        r = requests.get(f"{GITHUB_API_URL}/user", headers=headers, timeout=10)

        if r.status_code == 200:
            user_data = r.json()
            print(f"   ✅ Token is valid")
            print(f"   👤 User: {user_data.get('login')}")
            print(f"   📧 Email: {user_data.get('email', 'Not set')}")
            print(f"   📍 Location: {user_data.get('location', 'Not set')}")
        else:
            print(f"   ❌ Token validation failed (Status: {r.status_code})")
            print(f"   Error: {r.text[:200]}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
else:
    print("\n2️⃣  Skipping Token Validation (token not set)")

# Test 3: Check Repository Access
if GITHUB_TOKEN and GITHUB_OWNER and GITHUB_REPO:
    print("\n3️⃣  Checking Repository Access...")
    print("─" * 70)

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        r = requests.get(
            f"{GITHUB_API_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}",
            headers=headers,
            timeout=10
        )

        if r.status_code == 200:
            repo_data = r.json()
            print(f"   ✅ Repository accessible")
            print(f"   📦 Name: {repo_data.get('full_name')}")
            print(f"   📝 Description: {repo_data.get('description', 'None')}")
            print(f"   ⭐ Stars: {repo_data.get('stargazers_count')}")
            print(f"   🌿 Default Branch: {repo_data.get('default_branch')}")
        else:
            print(f"   ❌ Repository not accessible (Status: {r.status_code})")
            print(f"   Check GITHUB_OWNER and GITHUB_REPO")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
else:
    print("\n3️⃣  Skipping Repository Check (owner/repo not set)")

# Test 4: Check Branch Listing
if GITHUB_TOKEN and GITHUB_OWNER and GITHUB_REPO:
    print("\n4️⃣  Checking Available Branches...")
    print("─" * 70)

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        r = requests.get(
            f"{GITHUB_API_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/branches",
            headers=headers,
            timeout=10,
            params={"per_page": 10}
        )

        if r.status_code == 200:
            branches = r.json()
            print(f"   ✅ Found {len(branches)} branches")
            for branch in branches[:5]:
                print(f"      🌿 {branch['name']}")
            if len(branches) > 5:
                print(f"      ... and {len(branches) - 5} more")
        else:
            print(f"   ❌ Could not list branches (Status: {r.status_code})")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
else:
    print("\n4️⃣  Skipping Branch Check (token/owner/repo not set)")

# Test 5: Check Token Scopes
if GITHUB_TOKEN:
    print("\n5️⃣  Checking Token Scopes...")
    print("─" * 70)

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        r = requests.get(f"{GITHUB_API_URL}/user", headers=headers, timeout=10)

        if r.status_code == 200:
            scopes = r.headers.get("X-OAuth-Scopes", "").split(", ")
            required_scopes = ["repo"]
            print(f"   Current Scopes: {', '.join(scopes) if scopes[0] else 'No scopes'}")

            if not scopes or not scopes[0]:
                print(f"   ⚠️  Warning: Token has no scopes (might be public access only)")

            for scope in required_scopes:
                status = "✅" if scope in scopes else "❌"
                print(f"   {status} {scope}")
        else:
            print(f"   ⚠️  Could not check scopes")
    except Exception as e:
        print(f"   ⚠️  Could not check scopes: {e}")
else:
    print("\n5️⃣  Skipping Scope Check (token not set)")

# Test 6: Test PR Creation (Dry Run)
if GITHUB_TOKEN and GITHUB_OWNER and GITHUB_REPO:
    print("\n6️⃣  Test PR Creation (Validation Only)...")
    print("─" * 70)

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get default branch
    try:
        r = requests.get(
            f"{GITHUB_API_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}",
            headers=headers,
            timeout=10
        )
        default_branch = r.json().get("default_branch", "main")

        # Check if develop branch exists
        r = requests.get(
            f"{GITHUB_API_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/branches/develop",
            headers=headers,
            timeout=10
        )

        if r.status_code == 200:
            print(f"   ✅ 'develop' branch exists")
            print(f"   ℹ️  Ready to create PRs targeting 'develop'")
        else:
            print(f"   ℹ️  'develop' branch not found")
            print(f"   ℹ️  Default branch is '{default_branch}'")
            print(f"   💡 You can target '{default_branch}' instead")
    except Exception as e:
        print(f"   ⚠️  Could not validate branches: {e}")
else:
    print("\n6️⃣  Skipping PR Creation Test (config not complete)")

# Final Summary
print("\n" + "═" * 70)
print("📋 Summary")
print("═" * 70)

config_complete = all([GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO])

if config_complete:
    print("✅ Configuration is complete!")
    print("\nYou can now create PRs with:")
    print(f"   python agents/mr_agent.py --title \"...\" --head \"...\" --base \"...\"")
    print("\nFor more examples, see: MR_AGENT_QUICKSTART.md")
else:
    print("❌ Configuration is incomplete")
    print("\nNext steps:")
    print("   1. Get GitHub Personal Access Token (https://github.com/settings/tokens)")
    print("   2. Add to .env file:")
    print("      GITHUB_TOKEN=ghp_xxxxx")
    print("      GITHUB_OWNER=your_username")
    print("      GITHUB_REPO=your_repo")
    print("   3. Run this test again to verify")

print("═" * 70 + "\n")

