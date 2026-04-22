#!/usr/bin/env python3
"""Test different Jira API endpoints and versions"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()
JIRA_BASE_URL = os.getenv('JIRA_BASE_URL', '').rstrip('/')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')

print(f'🔍 Testing various Jira API endpoints')
print(f'Base URL: {JIRA_BASE_URL}')
print('─' * 60)

# Test different API paths
endpoints = [
    '/rest/api/3/myself',
    '/rest/api/2/myself',
    '/rest/api/latest/myself',
    '/api/3/myself',
    '/jira/rest/api/3/myself',
    '/secure/rest/api/3/myself',
]

auth = (JIRA_EMAIL, JIRA_API_TOKEN)

for endpoint in endpoints:
    url = JIRA_BASE_URL + endpoint
    try:
        r = requests.get(url, auth=auth, timeout=5)
        print(f'✅ {endpoint:<40} : {r.status_code}')
        if r.status_code == 200:
            print(f'   SUCCESS!')
            data = r.json()
            print(f'   User: {data.get("displayName")}')
    except Exception as e:
        print(f'❌ {endpoint:<40} : {str(e)[:40]}')

print('\n' + '─' * 60)
print('ℹ️  Most likely issue: API URL path is incorrect')
print('💡 Please verify the Jira instance URL in your .env file')

