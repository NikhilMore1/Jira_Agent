#!/usr/bin/env python3
"""
generate_pr_report.py
─────────────────────
Standalone utility to generate PDF reports for PR implementations.

Usage:
    python generate_pr_report.py \
      --title "Feature: JWT Auth" \
      --pr-number 42 \
      --user-story "PROJ-789" \
      --pr-url "https://github.com/owner/repo/pull/42" \
      --output "report.pdf"
"""

import argparse
import sys
from pathlib import Path

# Add agents directory to path
sys.path.insert(0, str(Path(__file__).parent / "agents"))

try:
    from report_generator import ReportGenerator
except ImportError:
    print("❌ Failed to import report_generator")
    print("Make sure you're running this from the correct directory")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate PDF reports for PR implementations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple report
  python generate_pr_report.py \
    --title "Feature: JWT Authentication" \
    --pr-number 42 \
    --user-story "EPMICMPSTP-789"

  # Complete report with details
  python generate_pr_report.py \
    --title "Feature: JWT Authentication" \
    --pr-number 42 \
    --user-story "EPMICMPSTP-789" \
    --pr-url "https://github.com/owner/repo/pull/42" \
    --git-commit "bbf6b3a" \
    --details "Added JWT provider,Implemented filter,Created token model" \
    --output "jwt_auth_report.pdf"
        """
    )

    parser.add_argument("--title", required=True, help="Feature title")
    parser.add_argument("--pr-number", type=int, required=True, help="PR number")
    parser.add_argument("--user-story", default="Not specified", help="Jira user story ID")
    parser.add_argument("--pr-url", default="", help="PR URL on GitHub")
    parser.add_argument("--git-commit", default="unknown", help="Git commit hash")
    parser.add_argument(
        "--details",
        default="",
        help="Implementation details (comma-separated)"
    )
    parser.add_argument(
        "--output",
        default="implementation_report.pdf",
        help="Output PDF file path"
    )

    args = parser.parse_args()

    print("\n🔄 Generating Implementation Report...\n")
    print(f"📋 Feature: {args.title}")
    print(f"📝 PR Number: #{args.pr_number}")
    print(f"🎯 User Story: {args.user_story}")
    print(f"💾 Output: {args.output}")
    print()

    # Parse implementation details
    implementation_details = []
    if args.details:
        implementation_details = [d.strip() for d in args.details.split(',')]
    else:
        # Default details
        implementation_details = [
            "Python implementation completed",
            "Comprehensive documentation created",
            "Configuration validation added",
            "Windows runners provided",
            "Error handling implemented",
            "Jira integration enabled",
            "Code pushed to GitHub"
        ]

    # Generate report
    generator = ReportGenerator()
    success = generator.generate_report(
        title=args.title,
        user_story=args.user_story,
        pr_url=args.pr_url or f"https://github.com/[owner]/[repo]/pull/{args.pr_number}",
        pr_number=args.pr_number,
        implementation_details=implementation_details,
        git_commit=args.git_commit,
        output_file=args.output
    )

    if success:
        print(f"\n✅ Report generated successfully!")
        print(f"📄 File: {args.output}")

        # Try to get file size
        try:
            import os
            size = os.path.getsize(args.output) / 1024
            print(f"📊 Size: {size:.2f} KB")
        except:
            pass
    else:
        print("\n❌ Failed to generate report")
        sys.exit(1)


if __name__ == "__main__":
    main()

