#!/usr/bin/env python3
"""
mr_agent.py
───────────
GitHub Merge Request (Pull Request) Agent – creates PRs with proper formatting.

Usage:
    python mr_agent.py --title "Feature: Add Auth" \
                       --head "feature/auth" \
                       --base "develop" \
                       --description "Implements OAuth2 authentication" \
                       --labels "feature,auth" \
                       --assignees "reviewer1,reviewer2" \
                       --jira-issue "PROJ-123"
"""

import argparse
import os
import sys
import requests
import subprocess
from dotenv import load_dotenv
from pathlib import Path

try:
    from report_generator import ReportGenerator
    REPORT_GENERATOR_AVAILABLE = True
except ImportError:
    REPORT_GENERATOR_AVAILABLE = False

# Load .env from parent directory (project root)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

GITHUB_API_URL = os.getenv("GITHUB_API_URL", "https://api.github.com")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_OWNER = os.getenv("GITHUB_OWNER", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "")


def validate_branches(owner: str, repo: str, head: str, base: str) -> tuple:
    """Validate that both branches exist."""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Check head branch
    url_head = f"{GITHUB_API_URL}/repos/{owner}/{repo}/branches/{head}"
    try:
        r = requests.get(url_head, headers=headers, timeout=10)
        if r.status_code != 200:
            return False, f"❌ Head branch '{head}' not found"
    except Exception as e:
        return False, f"❌ Error checking head branch: {e}"

    # Check base branch
    url_base = f"{GITHUB_API_URL}/repos/{owner}/{repo}/branches/{base}"
    try:
        r = requests.get(url_base, headers=headers, timeout=10)
        if r.status_code != 200:
            return False, f"❌ Base branch '{base}' not found"
    except Exception as e:
        return False, f"❌ Error checking base branch: {e}"

    return True, "✅ Both branches exist"


def check_existing_pr(owner: str, repo: str, head: str, base: str) -> tuple:
    """Check if a PR already exists from head to base."""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
    params = {
        "state": "open",
        "head": f"{owner}:{head}",
        "base": base
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        data = r.json()
        if data and len(data) > 0:
            return True, f"⚠️ PR already exists: {data[0]['html_url']}"
        return False, "✅ No existing PR"
    except Exception as e:
        return False, f"⚠️ Could not check existing PRs: {e}"


def create_pr(owner: str, repo: str, title: str, body: str, head: str,
              base: str, draft: bool = False) -> dict:
    """Create a new pull request."""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = {
        "title": title,
        "body": body,
        "head": head,
        "base": base,
        "draft": draft
    }

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.HTTPError as e:
        error_msg = e.response.text if hasattr(e, 'response') else str(e)
        return {"success": False, "error": f"HTTP Error {response.status_code}: {error_msg[:300]}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def add_labels(owner: str, repo: str, pr_number: int, labels: list) -> bool:
    """Add labels to a pull request."""
    if not labels:
        return True

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues/{pr_number}/labels"

    try:
        response = requests.post(
            url,
            json={"labels": labels},
            headers=headers,
            timeout=10
        )
        return response.status_code in [200, 201]
    except:
        return False


def add_assignees(owner: str, repo: str, pr_number: int, assignees: list) -> bool:
    """Add assignees to a pull request."""
    if not assignees:
        return True

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues/{pr_number}/assignees"

    try:
        response = requests.post(
            url,
            json={"assignees": assignees},
            headers=headers,
            timeout=10
        )
        return response.status_code in [200, 201]
    except:
        return False


def request_reviewers(owner: str, repo: str, pr_number: int, reviewers: list) -> bool:
    """Request reviewers for a pull request."""
    if not reviewers:
        return True

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}/requested_reviewers"

    try:
        response = requests.post(
            url,
            json={"reviewers": reviewers},
            headers=headers,
            timeout=10
        )
        return response.status_code in [200, 201]
    except:
        return False


def print_pr_confirmation(pr_data: dict, labels: list = None, assignees: list = None, reviewers: list = None):
    """Pretty-print PR confirmation."""
    print("\n" + "═" * 70)
    print("✅ PULL REQUEST CREATED SUCCESSFULLY!")
    print("═" * 70)

    pr_number = pr_data.get("number")
    title = pr_data.get("title")
    html_url = pr_data.get("html_url")
    state = pr_data.get("state")
    draft = pr_data.get("draft", False)
    head = pr_data.get("head", {}).get("ref")
    base = pr_data.get("base", {}).get("ref")
    created_at = pr_data.get("created_at")

    print(f"\n📋 PR #{pr_number}: {title}")
    print(f"{'─' * 70}")
    print(f"🔗 URL: {html_url}")
    print(f"📊 Status: {state.upper()}" + (" (DRAFT)" if draft else ""))
    print(f"🌿 Branch: {head} → {base}")
    print(f"⏰ Created: {created_at}")

    if labels:
        print(f"🏷️  Labels: {', '.join(labels)}")

    if assignees:
        print(f"👤 Assignees: {', '.join(assignees)}")

    if reviewers:
        print(f"👥 Reviewers: {', '.join(reviewers)}")

    body = pr_data.get("body", "")
    if body:
        print(f"\n📝 Description:")
        print(f"{'─' * 70}")
        lines = body.split('\n')[:10]  # Show first 10 lines
        for line in lines:
            print(f"   {line}")
        if len(body.split('\n')) > 10:
            print(f"   ... ({len(body.split(chr(10)))} lines total)")

    print("\n" + "═" * 70)
    print("💡 Next Steps:")
    print("   1. Add description and acceptance criteria")
    print("   2. Link to related Jira issue")
    print("   3. Wait for CI/CD to pass")
    print("   4. Request reviewers for code review")
    print("   5. Merge once approved")
    print("═" * 70 + "\n")


def build_pr_description(description: str, jira_issue: str = None, changes: list = None) -> str:
    """Build a formatted PR description."""
    body = f"{description}\n"

    if jira_issue:
        body += f"\n## Related Issue\nCloses #{jira_issue}\n"

    if changes:
        body += "\n## Changes Made\n"
        for change in changes:
            body += f"- {change}\n"

    body += "\n## Testing\n"
    body += "- [ ] Tested locally\n"
    body += "- [ ] Tests pass\n"
    body += "- [ ] No console errors\n"

    body += "\n## Checklist\n"
    body += "- [ ] Code follows style guidelines\n"
    body += "- [ ] No breaking changes\n"
    body += "- [ ] Documentation updated\n"
    body += "- [ ] Tests added/updated\n"

    return body


def main():
    parser = argparse.ArgumentParser(description="GitHub MR Agent - Create Pull Requests")
    parser.add_argument("--title", required=True, help="PR title")
    parser.add_argument("--head", required=True, help="Source branch (e.g., feature/auth)")
    parser.add_argument("--base", required=True, help="Target branch (e.g., develop)")
    parser.add_argument("--description", default="", help="PR description")
    parser.add_argument("--labels", default="", help="Labels (comma-separated)")
    parser.add_argument("--assignees", default="", help="Assignees (comma-separated)")
    parser.add_argument("--reviewers", default="", help="Reviewers (comma-separated)")
    parser.add_argument("--jira-issue", default="", help="Related Jira issue (e.g., PROJ-123)")
    parser.add_argument("--changes", default="", help="Changes made (comma-separated)")
    parser.add_argument("--draft", action="store_true", help="Create as draft PR")
    parser.add_argument("--owner", default=GITHUB_OWNER, help="GitHub owner/org")
    parser.add_argument("--repo", default=GITHUB_REPO, help="GitHub repository")
    parser.add_argument("--generate-report", action="store_true", help="Generate PDF report")
    parser.add_argument("--report-file", default="mr_implementation_report.pdf", help="Report output file")

    args = parser.parse_args()

    # Validate required config
    if not GITHUB_TOKEN:
        print("❌ Error: GITHUB_TOKEN not set in .env")
        sys.exit(1)

    owner = args.owner or GITHUB_OWNER
    repo = args.repo or GITHUB_REPO

    if not owner or not repo:
        print("❌ Error: GITHUB_OWNER and GITHUB_REPO must be set")
        sys.exit(1)

    print("\n🔀 GitHub MR Agent: Creating Pull Request...\n")
    print(f"📦 Repository: {owner}/{repo}")
    print(f"🎯 Title: {args.title}")
    print(f"🌿 Branch: {args.head} → {args.base}\n")

    # Parse labels, assignees, reviewers
    labels = [l.strip() for l in args.labels.split(',') if l.strip()]
    assignees = [a.strip() for a in args.assignees.split(',') if a.strip()]
    reviewers = [r.strip() for r in args.reviewers.split(',') if r.strip()]
    changes = [c.strip() for c in args.changes.split(',') if c.strip()]

    # Validate branches
    print("🔍 Validating branches...")
    valid, msg = validate_branches(owner, repo, args.head, args.base)
    if not valid:
        print(msg)
        sys.exit(1)
    print(msg)

    # Check for existing PR
    print("🔍 Checking for existing PRs...")
    exists, msg = check_existing_pr(owner, repo, args.head, args.base)
    if exists:
        print(msg)
        sys.exit(1)
    print(msg)

    # Build PR description
    body = build_pr_description(args.description, args.jira_issue, changes)

    # Create PR
    print("📤 Creating PR...\n")
    result = create_pr(owner, repo, args.title, body, args.head, args.base, args.draft)

    if not result["success"]:
        print(f"❌ Failed to create PR: {result['error']}")
        sys.exit(1)

    pr_data = result["data"]
    pr_number = pr_data.get("number")

    # Add metadata
    print("⚙️  Adding metadata...")
    add_labels(owner, repo, pr_number, labels)
    add_assignees(owner, repo, pr_number, assignees)
    request_reviewers(owner, repo, pr_number, reviewers)

    # Print confirmation
    print_pr_confirmation(pr_data, labels, assignees, reviewers)

    # Generate report if requested
    if args.generate_report and REPORT_GENERATOR_AVAILABLE:
        print("\n📄 Generating Implementation Report...")
        try:
            # Get git commit hash
            git_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()[:8]
        except:
            git_commit = "unknown"

        implementation_details = [
            f"Created PR: {args.title}",
            f"Source Branch: {args.head}",
            f"Target Branch: {args.base}",
            f"Linked Jira Issue: {args.jira_issue}" if args.jira_issue else "No Jira issue linked",
            f"Labels: {', '.join(labels)}" if labels else "No labels added",
            f"Reviewers: {', '.join(reviewers)}" if reviewers else "No reviewers assigned",
            "Implementation complete and ready for review"
        ]

        if args.changes:
            implementation_details.extend([c.strip() for c in args.changes.split(',')])

        generator = ReportGenerator()
        report_success = generator.generate_report(
            title=args.title,
            user_story=args.jira_issue or "Not specified",
            pr_url=pr_data.get('html_url', ''),
            pr_number=pr_number,
            implementation_details=implementation_details,
            git_commit=git_commit,
            output_file=args.report_file
        )

        if report_success:
            print(f"\n✅ Report saved as: {args.report_file}")
        else:
            print("\n⚠️  Report generation failed (reportlab may not be installed)")
            print("   Install with: pip install reportlab")
    elif args.generate_report and not REPORT_GENERATOR_AVAILABLE:
        print("\n⚠️  Report generation requested but reportlab not available")
        print("   Install with: pip install reportlab")

    return pr_data


if __name__ == "__main__":
    main()




