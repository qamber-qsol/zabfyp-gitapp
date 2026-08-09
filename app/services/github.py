import logging
import requests
from app.core.config import settings

logger = logging.getLogger(__name__)

async def send_org_invite(github_username: str, repo_name: str) -> str:
    """
    Sends a real GitHub organization invitation using the student's email address.
    """
    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    url = f"https://api.github.com/orgs/{settings.GITHUB_ORG_NAME}/invitations"
    
    # Use the email directly if it looks like an email, otherwise format it or use it safely
    payload = {
        "role": "direct_member"
    }
    
    if "@" in github_username:
        payload["email"] = github_username
    else:
        # Fallback: if they passed a username, append their szabist domain or handle via email lookup
        payload["email"] = f"{github_username}@szabist.pk" 

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        logger.info(f"Successfully sent new GitHub invite to {payload.get('email')}")
        return "created"
    elif response.status_code == 422:
        logger.info(f"Invite already pending for {payload.get('email')}")
        return "exists"
    else:
        logger.error(f"GitHub API Error status {response.status_code}: {response.text}")
        return "error"