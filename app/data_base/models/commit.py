import httpx

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
    