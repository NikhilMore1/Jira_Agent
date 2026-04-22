"""
jira_agent.py
─────────────
Simple Jira Agent – reads a Jira board and extracts stories for a person.

Usage:
    python jira_agent.py --board-url "https://org.atlassian.net/jira/software/projects/PROJ/boards/1" \
                         --assignee "Nikhil Sharadmore"
"""

import argparse
import os
import sys
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load .env from parent directory (project root)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "https://your-org.atlassian.net")
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


def fetch_stories(board_url: str, assignee: str) -> list:
    """Fetch all stories assigned to the given person."""
    project_key = extract_project_key(board_url)

    jql = (
        f'project = "{project_key}" '
        f'AND issuetype = Story '
        f'AND assignee = "{assignee}" '
        f'ORDER BY created DESC'
    )

    # Use API v2 instead of v3 (some Jira instances don't support v3)
    url = f"{JIRA_BASE_URL}/rest/api/2/search"
    params = {
        "jql": jql,
        "fields": "summary,description,status,priority,customfield_10016",
        "maxResults": 50,
    }

    try:
        print(f"🔗 Calling: {url}")
        print(f"📝 JQL: {jql}")
        response = requests.get(
            url,
            params=params,
            auth=(JIRA_EMAIL, JIRA_API_TOKEN),
            headers={"Accept": "application/json"},
            timeout=30,
            verify=True
        )
        print(f"📊 Status Code: {response.status_code}")
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error {response.status_code}: {e}")
        print(f"Response: {response.text[:500]}")
        return []
    except Exception as e:
        print(f"❌ Jira API Error: {e}")
        return []

    data = response.json()
    issues = data.get("issues", [])

    stories = []
    for issue in issues:
        story = {
            "key": issue["key"],
            "summary": issue["fields"].get("summary", ""),
            "description": issue["fields"].get("description", ""),
            "status": issue["fields"].get("status", {}).get("name", "Unknown"),
            "priority": issue["fields"].get("priority", {}).get("name", "Unknown"),
            "points": issue["fields"].get("customfield_10016", "?"),
        }
        stories.append(story)

    return stories


def print_stories(stories: list):
    """Pretty-print the stories."""
    if not stories:
        print("❌ No stories found.")
        return

    print(f"\n✅ Found {len(stories)} story/stories:\n")
    for story in stories:
        print("─" * 60)
        print(f"KEY      : {story['key']}")
        print(f"SUMMARY  : {story['summary']}")
        print(f"STATUS   : {story['status']}")
        print(f"PRIORITY : {story['priority']}")
        print(f"POINTS   : {story['points']}")
        print(f"DESCRIPTION:\n{story['description']}\n")


def main():
    parser = argparse.ArgumentParser(description="Jira Story Reader Agent")
    parser.add_argument(
        "--board-url",
        default=JIRA_BOARD_URL,
        help=f"Jira board URL (default from .env: {JIRA_BOARD_URL[:50]}...)"
    )
    parser.add_argument(
        "--assignee",
        default=JIRA_ASSIGNEE,
        help=f"Assignee name (default from .env: {JIRA_ASSIGNEE})"
    )
    args = parser.parse_args()

    # Check if we have values
    if not args.board_url or not args.assignee:
        print("❌ Error: Missing JIRA_BOARD_URL or JIRA_ASSIGNEE in .env file")
        print(f"   Current values:")
        print(f"   - Board URL: {args.board_url or 'NOT SET'}")
        print(f"   - Assignee: {args.assignee or 'NOT SET'}")
        sys.exit(1)

    if not JIRA_EMAIL or not JIRA_API_TOKEN:
        print("❌ Error: Missing JIRA_EMAIL or JIRA_API_TOKEN in .env file")
        sys.exit(1)

    print("\n🔍 Jira Agent: Fetching stories...\n")
    print(f"📋 Project: {args.board_url.split('projectKey=')[-1].split('&')[0]}")
    print(f"👤 Assignee: {args.assignee}\n")

    stories = fetch_stories(args.board_url, args.assignee)
    print_stories(stories)

    return stories


if __name__ == "__main__":
    main()

