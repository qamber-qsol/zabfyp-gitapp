import requests
from github import Github, GithubException
from app.config import settings

class GitHubService:
    def __init__(self):
        self.client = Github(settings.GITHUB_TOKEN)
        self.org_name = settings.GITHUB_ORG_NAME
        self.org = self.client.get_organization(self.org_name)

    def get_or_create_parent_team(self):
        """Fetches the CS-FYP-2026 parent team, or creates it if missing."""
        parent_name = "CS-FYP-2026"
        slug = "cs-fyp-2026"
        try:
            return self.org.get_team_by_slug(slug)
        except GithubException:
            # Create it if it doesn't exist
            return self.org.create_team(name=parent_name, privacy="closed")

    def provision_group(self, repo_name: str, team_name: str, student_emails: list[str]):
        """
        1. Creates private repository
        2. Creates child team nested under CS-FYP-2026
        3. Grants team 'push' (write) permissions to repo
        4. Invites students via @szabist.pk email
        """
        results = {"repo_created": False, "team_created": False, "invites_sent": 0, "errors": []}

        # 1. Create Repository
        try:
            repo = self.org.create_repo(name=repo_name, private=True, auto_init=True)
            results["repo_created"] = True
        except GithubException as e:
            if e.status == 422: # Repo already exists
                repo = self.org.get_repo(repo_name)
                results["repo_created"] = True
            else:
                results["errors"].append(f"Repo error: {str(e)}")
                return results

        # 2. Create Nested Team
        parent_team = self.get_or_create_parent_team()
        try:
            team = self.org.create_team(
                name=team_name, 
                privacy="closed",
                parent_team_id=parent_team.id # Nests it exactly like CS-FYP-2025
            )
            results["team_created"] = True
        except GithubException as e:
            if e.status == 422: # Team already exists
                teams = self.org.get_teams()
                team = next((t for t in teams if t.name == team_name), None)
                results["team_created"] = True
            else:
                results["errors"].append(f"Team error: {str(e)}")
                return results

        # 3. Link Team to Repository with Write (Push) Access
        if team and repo:
            team.set_repo_permission(repo, "push")

        # 4. Invite Students via Email
        headers = {
            "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        
        for email in student_emails:
            invite_url = f"https://api.github.com/orgs/{self.org_name}/invitations"
            payload = {
                "email": email,
                "role": "direct_member",
                "team_ids": [team.id] if team else []
            }
            res = requests.post(invite_url, json=payload, headers=headers)
            if res.status_code in [201, 422]: 
                results["invites_sent"] += 1
            else:
                results["errors"].append(f"Invite failed for {email}: {res.text}")

        return results

github_service = GitHubService()