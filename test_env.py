#!/usr/bin/env python3
"""
test_env.py - Test if .env file is properly configured
Run this to verify your Jira configuration is working!
"""

import os
import sys
from pathlib import Path

# Load .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Loaded .env from: {env_path}\n")
except ImportError:
    print("❌ python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

# Check all required variables
required_vars = {
    "JIRA_BASE_URL": "Jira Base URL",
    "JIRA_EMAIL": "Jira Email",
    "JIRA_API_TOKEN": "Jira API Token",
    "JIRA_BOARD_URL": "Board URL",
    "JIRA_ASSIGNEE": "Assignee Name",
}

print("📋 Configuration Status:\n")
all_set = True

for var, description in required_vars.items():
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        if "TOKEN" in var or "API" in var:
            display_value = value[:10] + "..." if len(value) > 10 else value
        elif "EMAIL" in var:
            display_value = value[:15] + "..." if len(value) > 15 else value
        else:
            display_value = value[:50] + "..." if len(value) > 50 else value
        print(f"✅ {description:25} : {display_value}")
    else:
        print(f"❌ {description:25} : NOT SET")
        all_set = False

print("\n" + "─" * 60)

if all_set:
    print("\n✅ All configurations are set! You can run:")
    print("   python agents/jira_agent.py\n")
else:
    print("\n❌ Some configurations are missing. Please update .env file\n")
    sys.exit(1)

