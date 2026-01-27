
from commit import CommitModel
from skill_scorer import ScoreSkillsForProject
from commit import AdminCommitmarkForUser

from datetime import timedelta

class CommitAnalyzer:
    def __init__(self, repo_owner: str, repo_name: str, commit_sha: str):
       
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.commit_sha = commit_sha
        self.commit_model = CommitModel(repo_owner, repo_name, commit_sha)

    def analyze_commit(self):
        """
        Analyzes a specific commit in a GitHub repository and returns a dictionary containing information about the commit.
        """
        commit_message = self.commit_model.get_commit_message()
        author_info = self.commit_model.get_author_info()
        commit_stats = self.commit_model.get_commit_stats()

        analysis = {
            "commit_message": commit_message,
            "author_info": author_info,
            "commit_stats": commit_stats
        }
        return analysis

    def get_summary(self):
        analysis = self.analyze_commit()
        summary = (
            f"Commit Message: {analysis['commit_message']}\n"
            f"Author: {analysis['author_info']['name']} <{analysis['author_info']['email']}>\n"
            f"Date: {analysis['author_info']['date']}\n"
            f"Stats: +{analysis['commit_stats']['additions']} -{analysis['commit_stats']['deletions']} (Total: {analysis['commit_stats']['total']})"
        )
        return summary
class SkillMarketValueAnalyzer:
    def __init__(self, repo_owner: str, repo_name: str, commit_sha: str):
        self.skill_scorer = ScoreSkillsForProject(repo_owner, repo_name, commit_sha)

    def analyze_skill_market_value(self):
        return self.skill_scorer.get_skill_market_value()







analyzer = CommitAnalyzer("megaladonntm-arch", "ShadowSkills", "d0e7d528d11e5270da48ad837031a69381049b34")

report = analyzer.get_detailed_report()
print(report)
summary_dict = analyzer.get_commit_summary_dict()
print(summary_dict)
time_difference_days = analyzer.get_time_between_commits_days()
print(f"Time between commits: {time_difference_days} days")
is_merge = analyzer.is_merge_commit()
print(f"Is merge commit: {is_merge}")

changed_files = analyzer.get_changed_files()
print(f"Changed files: {changed_files}")
commit_tags = analyzer.get_commit_tags()
print(f"Commit tags: {commit_tags}")
 



commit_branch = analyzer.get_commit_branch()
print(f"Commit branch: {commit_branch}")
skill_analyzer = SkillMarketValueAnalyzer("megaladonntm-arch", "ShadowSkills", "d0e7d528d11e5270da48ad837031a69381049b34")
skill_market_value = skill_analyzer.analyze_skill_market_value()
print(f"Skill Market Value: {skill_market_value}")
summary = analyzer.given_summary()
print(summary)
grade = analyzer.grade_commit()
print(grade)
