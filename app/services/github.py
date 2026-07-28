import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_org_invite(github_username: str, repo_name: str) -> bool:
    """
    Send an organization/repository invitation to a student via GitHub REST API.

    In production, this function executes an HTTP POST request to:
    POST /orgs/{settings.GITHUB_ORG_NAME}/invitations (or adding collaborator to repository)
    Headers:
        Authorization: Bearer <settings.GITHUB_TOKEN>
        Accept: application/vnd.github+json
    Body:
        {
            "invitee_id": <user_id_or_username>,
            "role": "direct_member"
        }
    """
    logger.info(
        f"[STUB] GitHub org invitation sent to user '{github_username}' "
        f"for repository '{repo_name}' in org '{settings.GITHUB_ORG_NAME}'"
    )
    # Stub returns True indicating successfully queued/sent invite
    return True
