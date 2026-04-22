"""
jira_agent_enhanced.py
─────────────────────
Enhanced Jira Agent - Tries multiple API endpoints for better compatibility
"""

import os
import sys
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load .env from parent directory (project root)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "https://jiraeu.epam.com")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "you@example.com")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "your-token")
JIRA_BOARD_URL = os.getenv("JIRA_BOARD_URL", "")
JIRA_ASSIGNEE = os.getenv("JIRA_ASSIGNEE", "")


def extract_project_key(board_url: str) -> str:
    """Extract project key from Jira board URL."""
    import re
    # Try standard format first: /projects/KEY/
    match = re.search(r"/projects/([A-Z0-9]+)/", board_url)
    if match:
        return match.group(1)

    # Try RapidBoard format: ?projectKey=KEY
    match = re.search(r"projectKey=([A-Z0-9]+)", board_url)
    if match:
        return match.group(1)

    raise ValueError(f"Cannot parse project key from: {board_url}")


def fetch_stories_v3(project_key: str, assignee: str) -> list:
    """Try API v3 endpoint."""
    jql = (
        f'project = "{project_key}" '
        f'AND issuetype = Story '
        f'AND assignee = "{assignee}" '
        f'ORDER BY created DESC'
    )

    url = f"{JIRA_BASE_URL}/rest/api/3/search"
    params = {
        "jql": jql,
        "fields": "summary,description,status,priority,customfield_10016",
        "maxResults": 50,
    }

    try:
        response = requests.get(
            url,
            params=params,
            auth=(JIRA_EMAIL, JIRA_API_TOKEN),
            headers={"Accept": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("issues", [])
        return None
    except:
        return None


def fetch_stories_v2(project_key: str, assignee: str) -> list:
    """Try API v2 endpoint (older Jira instances)."""
    jql = (
        f'project = "{project_key}" '
        f'AND issuetype = Story '
        f'AND assignee = "{assignee}" '
        f'ORDER BY created DESC'
    )

    url = f"{JIRA_BASE_URL}/rest/api/2/search"
    params = {
        "jql": jql,
        "fields": "summary,description,status,priority,customfield_10016",
        "maxResults": 50,
    }

    try:
        response = requests.get(
            url,
            params=params,
            auth=(JIRA_EMAIL, JIRA_API_TOKEN),
            headers={"Accept": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("issues", [])
        return None
    except:
        return None


def fetch_stories_jira_path(project_key: str, assignee: str) -> list:
    """Try with /jira in path."""
    jql = (
        f'project = "{project_key}" '
        f'AND issuetype = Story '
        f'AND assignee = "{assignee}" '
        f'ORDER BY created DESC'
    )

    url = f"{JIRA_BASE_URL}/jira/rest/api/3/search"
    params = {
        "jql": jql,
        "fields": "summary,description,status,priority,customfield_10016",
        "maxResults": 50,
    }

    try:
        response = requests.get(
            url,
            params=params,
            auth=(JIRA_EMAIL, JIRA_API_TOKEN),
            headers={"Accept": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("issues", [])
        return None
    except:
        return None


def parse_story(issue: dict) -> dict:
    """Parse a Jira issue into a story."""
    return {
        "key": issue.get("key", ""),
        "summary": issue.get("fields", {}).get("summary", ""),
        "description": issue.get("fields", {}).get("description", ""),
        "status": issue.get("fields", {}).get("status", {}).get("name", "Unknown"),
        "priority": issue.get("fields", {}).get("priority", {}).get("name", "Unknown"),
        "points": issue.get("fields", {}).get("customfield_10016", "?"),
    }


def fetch_stories(board_url: str, assignee: str) -> list:
    """Fetch stories, trying multiple API endpoints."""
    project_key = extract_project_key(board_url)

    print(f"\n🔄 Trying multiple API endpoints...\n")

    # Try API v3 first
    print("  1️⃣  Trying API v3 (/rest/api/3)...")
    issues = fetch_stories_v3(project_key, assignee)
    if issues is not None:
        print("     ✅ Success with API v3!")
        return [parse_story(issue) for issue in issues]

    # Try API v2
    print("  2️⃣  Trying API v2 (/rest/api/2)...")
    issues = fetch_stories_v2(project_key, assignee)
    if issues is not None:
        print("     ✅ Success with API v2!")
        return [parse_story(issue) for issue in issues]

    # Try with /jira path
    print("  3️⃣  Trying with /jira path (/jira/rest/api/3)...")
    issues = fetch_stories_jira_path(project_key, assignee)
    if issues is not None:
        print("     ✅ Success with /jira path!")
        return [parse_story(issue) for issue in issues]

    print("  ❌ All API endpoints failed")
    return []


def print_stories(stories: list):
    """Pretty-print the stories."""
    if not stories:
        print("\n❌ No stories found.\n")
        print("Possible reasons:")
        print("  1. API token might be expired")
        print("  2. Jira URL might be incorrect")
        print("  3. Project key might not exist")
        print("  4. No stories assigned to you")
        print("\nTo fix:")
        print("  • Go to https://jiraeu.epam.com")
        print("  • Generate a new API token")
        print("  • Update JIRA_API_TOKEN in .env file")
        print("  • Run: python agents/jira_agent.py\n")
        return

    print(f"\n✅ Found {len(stories)} story/stories:\n")
    for story in stories:
        print("─" * 70)
        print(f"KEY      : {story['key']}")
        print(f"SUMMARY  : {story['summary']}")
        print(f"STATUS   : {story['status']}")
        print(f"PRIORITY : {story['priority']}")
        print(f"POINTS   : {story['points']}")
        if story['description']:
            print(f"DESCRIPTION: {story['description']}\n")
        else:
            print()


def main():
    if not JIRA_BOARD_URL or not JIRA_ASSIGNEE:
        print("❌ Error: Missing JIRA_BOARD_URL or JIRA_ASSIGNEE in .env file")
        sys.exit(1)

    if not JIRA_EMAIL or not JIRA_API_TOKEN:
        print("❌ Error: Missing JIRA_EMAIL or JIRA_API_TOKEN in .env file")
        sys.exit(1)

    print("\n🔍 Jira Agent: Fetching stories (trying multiple endpoints)...\n")
    print(f"📋 Project: {extract_project_key(JIRA_BOARD_URL)}")
    print(f"👤 Assignee: {JIRA_ASSIGNEE}")

    stories = fetch_stories(JIRA_BOARD_URL, JIRA_ASSIGNEE)
    print_stories(stories)

    return stories


if __name__ == "__main__":
    main()

