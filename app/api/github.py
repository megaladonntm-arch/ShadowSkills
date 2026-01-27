from fastapi import APIRouter, HTTPException
from app.services.commit_analyzer import CommitAnalyzer

router = APIRouter()

@router.get("/repo/{repo_owner}/{repo_name}/commit/{commit_sha}/analyze")
def analyze_commit_endpoint(repo_owner: str, repo_name: str, commit_sha: str):
    try:
        analyzer = CommitAnalyzer(repo_owner=repo_owner, repo_name=repo_name, commit_sha=commit_sha)
        analysis = analyzer.analyze_commit()
        # A simple check to see if we got any meaningful data back.
        # The underlying model prints errors but returns empty/default values.
        if analysis.get("commit_message") == "Failed to retrieve commit data.":
             raise HTTPException(status_code=404, detail="Commit not found or failed to retrieve data from GitHub API.")
        return analysis
    except Exception as e:
        # Catch any other unexpected errors during analysis.
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
