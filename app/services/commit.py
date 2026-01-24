import httpx
from datetime import datetime

class CommitModel:

    def __init__(self, repo_owner: str, repo_name: str, commit_sha: str):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.commit_sha = commit_sha
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/commits/{self.commit_sha}"

    def get_commit_data(self):
        try:
            response = httpx.get(self.api_url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"An error occurred while fetching commit data: {e}")
            return None
            
    def get_commit_message(self):
        commit_data = self.get_commit_data()
        if commit_data:
            return commit_data.get("commit", {}).get("message", "No commit message found.")
        return "Failed to retrieve commit data."

    def get_author_info(self):
        commit_data = self.get_commit_data()    
        if commit_data:
            author = commit_data.get("commit", {}).get("author", {})
            return {
                "name": author.get("name", "Unknown"),
                "email": author.get("email", "Unknown"),
                "date": author.get("date", "Unknown")
            }
        return {"name": "Unknown", "email": "Unknown", "date": "Unknown"}

    def get_commit_stats(self):
        commit_data = self.get_commit_data()
        if commit_data:
            stats = commit_data.get("stats", {})
            return {
                "additions": stats.get("additions", 0),
                "deletions": stats.get("deletions", 0),
                "total": stats.get("total", 0)
            }
        return {"additions": 0, "deletions": 0, "total": 0}

    def get_time_between_commits(self):
        commit_data = self.get_commit_data()
        if not commit_data or not commit_data.get("parents"):
            return "Could not retrieve commit data or no parent commit found."

        current_commit_date_str = commit_data.get("commit", {}).get("author", {}).get("date")
        if not current_commit_date_str:
            return "Could not retrieve current commit's date."
        
        current_commit_date = datetime.fromisoformat(current_commit_date_str.replace("Z", "+00:00"))

        parent_sha = commit_data["parents"][0]["sha"]
        parent_commit = CommitModel(self.repo_owner, self.repo_name, parent_sha)
        parent_commit_data = parent_commit.get_commit_data()
        if not parent_commit_data:
            return "Could not retrieve parent commit's data."

        parent_commit_date_str = parent_commit_data.get("commit", {}).get("author", {}).get("date")
        if not parent_commit_date_str:
            return "Could not retrieve parent commit's date."

        parent_commit_date = datetime.fromisoformat(parent_commit_date_str.replace("Z", "+00:00"))

        time_difference = current_commit_date - parent_commit_date
        return time_difference

    def get_changed_files(self):
        """
        Returns a list of files changed in the commit.
        """
        commit_data = self.get_commit_data()
        if commit_data and "files" in commit_data:
            return [file.get("filename") for file in commit_data["files"]]
        return []

    def get_branch_for_commit(self):
        """
        Returns the branch name for the commit.
        Note: This uses a preview API and may not be stable.
        It might return multiple branches if the commit is on several.
        """
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/commits/{self.commit_sha}/branches-where-head"
        headers = {"Accept": "application/vnd.github.groot-preview+json"}
        try:
            response = httpx.get(url, headers=headers)
            response.raise_for_status()
            branches = response.json()
            if branches:
                return branches[0].get("name", "Unknown")
        except httpx.HTTPError as e:
            print(f"An error occurred while fetching branch data: {e}")
        return "Unknown"

    def get_tags_for_commit(self):
        """
        Returns a list of tags for the commit.
        Note: The GitHub API does not provide a direct way to get tags for a commit.
        This method is a placeholder and currently returns an empty list.
        A full implementation would require fetching all tags and finding the match.
        """
        return []
    




class AdminCommitmarkForUser:
    def __init__(self, repo_owner: str, repo_name: str, commit_sha: str, admin_user: str, mark: str, reason: str):
        self.commit_model = CommitModel(repo_owner, repo_name, commit_sha)
        self.admin_user = admin_user
        self.mark = mark
        self.reason = reason

    def record_mark(self):
        # Placeholder for recording the mark in a database or log
        print(f"Admin {self.admin_user} marked commit {self.commit_model.commit_sha} with {self.mark} for reason: {self.reason}")
        