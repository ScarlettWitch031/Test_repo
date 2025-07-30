import json
import os
import requests

# Load the findings from the JSON file
with open('findings.json', 'r') as f:
    findings = json.load(f)

# GitLab environment variables
project_id = os.environ["CI_PROJECT_ID"]
merge_request_iid = os.environ["CI_MERGE_REQUEST_IID"]
gitlab_token = os.environ["GITLAB_TOKEN"]  # You must set this variable in GitLab

# GitLab API endpoint
api_base_url = os.environ.get("CI_API_V4_URL", "https://gitlab.com/api/v4")

headers = {
    "PRIVATE-TOKEN": gitlab_token,
    "Content-Type": "application/json",
}

# Post one discussion per finding
for finding in findings.get("results", []):
    body = f"""
**Semgrep finding**

- **Rule ID:** {finding['check_id']}
- **File:** {finding['path']}
- **Line:** {finding['start']['line']}
- **Message:** {finding['extra']['message']}
- **Impact:** {finding['extra']['metadata'].get('impact', 'N/A')}
- **Confidence:** {finding['extra']['metadata'].get('confidence', 'N/A')}
- **Rule Link:** https://semgrep.dev/r/{finding['check_id']}
"""

    payload = {
        "body": body,
        "position": {
            "position_type": "text",
            "new_path": finding["path"],
            "new_line": finding["start"]["line"],
            "base_sha": os.environ["CI_COMMIT_BEFORE_SHA"],
            "head_sha": os.environ["CI_COMMIT_SHA"],
            "start_sha": os.environ["CI_COMMIT_BEFORE_SHA"]
        }
    }

    url = f"{api_base_url}/projects/{project_id}/merge_requests/{merge_request_iid}/discussions"
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 201:
        raise Exception(f"Failed to post comment: {response.status_code} {response.text}")


print("checl")
