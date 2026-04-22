#!/usr/bin/env python3
"""Test Jira API connectivity"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()
JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
PROJECT_KEY = "EPMICMPSTP"

print(f'🔧 Testing Jira API Connectivity')
print(f'Base URL: {JIRA_BASE_URL}')
print(f'Email: {JIRA_EMAIL}')
print('─' * 60)

# Test 1: Basic auth test with /myself
print('\n1️⃣  Testing /myself endpoint...')
try:
    r = requests.get(
        f'{JIRA_BASE_URL}/rest/api/3/myself',
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        timeout=10
    )
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        user_data = r.json()
        print(f'   ✅ User: {user_data.get("displayName")}')
    else:
        print(f'   ❌ Error: {r.text[:300]}')
except Exception as e:
    print(f'   ❌ Connection failed: {e}')

# Test 2: Get project
print(f'\n2️⃣  Testing /project/{PROJECT_KEY} endpoint...')
try:
    r = requests.get(
        f'{JIRA_BASE_URL}/rest/api/3/project/{PROJECT_KEY}',
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        timeout=10
    )
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        project_data = r.json()
        print(f'   ✅ Project: {project_data.get("name")}')
    else:
        print(f'   ❌ Error: {r.text[:300]}')
except Exception as e:
    print(f'   ❌ Connection failed: {e}')

# Test 3: Search with simple JQL
print(f'\n3️⃣  Testing /search endpoint with simple query...')
try:
    jql = f'project = {PROJECT_KEY}'
    r = requests.get(
        f'{JIRA_BASE_URL}/rest/api/3/search',
        params={'jql': jql, 'maxResults': 5},
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        timeout=10
    )
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        print(f'   ✅ Found {data.get("total")} issues')
        for issue in data.get('issues', [])[:3]:
            print(f'      - {issue["key"]}: {issue["fields"]["summary"]}')
    else:
        print(f'   ❌ Error: {r.text[:300]}')
except Exception as e:
    print(f'   ❌ Connection failed: {e}')

# Test 4: Search for assignee
print(f'\n4️⃣  Testing /search endpoint with assignee filter...')
try:
    jql = f'project = {PROJECT_KEY} AND assignee = "Nikhil Sharad More"'
    r = requests.get(
        f'{JIRA_BASE_URL}/rest/api/3/search',
        params={'jql': jql, 'maxResults': 50},
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        timeout=10
    )
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        print(f'   ✅ Found {data.get("total")} issues for Nikhil Sharad More')
        for issue in data.get('issues', []):
            status = issue['fields']['status']['name']
            print(f'      - {issue["key"]}: {issue["fields"]["summary"]} [{status}]')
    else:
        print(f'   ❌ Error: {r.text[:300]}')
except Exception as e:
    print(f'   ❌ Connection failed: {e}')

print('\n✅ Test complete!')

