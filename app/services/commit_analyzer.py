
from commit import CommitModel
from skill_scorer import ScoreSkillsForProject

from datetime import timedelta

class CommitAnalyzer:
    def __init__(self, repo_owner: str, repo_name: str, commit_sha: str):
        self.commit_model = CommitModel(repo_owner, repo_name, commit_sha)

    def analyze_commit(self):
        commit_message = self.commit_model.get_commit_message()
        author_info = self.commit_model.get_author_info()
        commit_stats = self.commit_model.get_commit_stats()

        analysis = {
            "commit_message": commit_message,
            "author_info": author_info,
            "commit_stats": commit_stats
        }
        return analysis
        
    def given_summary(self):
        analysis = self.analyze_commit()
        summary = (
            f"Commit Message: {analysis['commit_message']}\n"
            f"Author: {analysis['author_info']['name']} <{analysis['author_info']['email']}>\n"
            f"Date: {analysis['author_info']['date']}\n"
            f"Stats: +{analysis['commit_stats']['additions']} -{analysis['commit_stats']['deletions']} (Total: {analysis['commit_stats']['total']})"
        )
        return summary

    def grade_commit(self):
        analysis = self.analyze_commit()
        commit_message = analysis['commit_message']
        stats = analysis['commit_stats']
        #check the commits and give a grade based on some simple criteria
        grade = "C"
        if len(commit_message) > 50 and stats['additions'] > 10:
            grade = "A"
        elif len(commit_message) > 30 and stats['additions'] > 5:
            grade = "B"
        return grade

    def is_significant_commit(self):
        analysis = self.analyze_commit()
        stats = analysis['commit_stats']
        # A commit is considered significant if it has more than 20 additions or deletions
        return stats['additions'] > 20 or stats['deletions'] > 20

    def get_detailed_report(self):
        analysis = self.analyze_commit()
        report = (
            f"Detailed Commit Report:\n"
            f"-----------------------\n"
            f"Commit Message:\n{analysis['commit_message']}\n\n"
            f"Author Information:\n"
            f"Name: {analysis['author_info']['name']}\n"
            f"Email: {analysis['author_info']['email']}\n"
            f"Date: {analysis['author_info']['date']}\n\n"
            f"Commit Statistics:\n"
            f"Additions: {analysis['commit_stats']['additions']}\n"
            f"Deletions: {analysis['commit_stats']['deletions']}\n"
            f"Total Changes: {analysis['commit_stats']['total']}\n"
        )
        return report

    def get_commit_summary_dict(self):
        analysis = self.analyze_commit()
        summary_dict = {
            "commit_message": analysis['commit_message'],
            "author_name": analysis['author_info']['name'],
            "author_email": analysis['author_info']['email'],
            "author_date": analysis['author_info']['date'],
            "additions": analysis['commit_stats']['additions'],
            "deletions": analysis['commit_stats']['deletions'],
            "total_changes": analysis['commit_stats']['total']
        }
        return summary_dict

    def get_time_between_commits_days(self):
        time_difference = self.commit_model.get_time_between_commits()
        if isinstance(time_difference, timedelta):
            return time_difference.days
        return -1 # Return -1 or some other indicator of an error/inability to calculate

    def is_merge_commit(self):
        commit_message = self.commit_model.get_commit_message()
        return commit_message.startswith("Merge") or "merge" in commit_message.lower()

    def get_changed_files(self):
        return self.commit_model.get_changed_files()

    def get_commit_tags(self):
        return self.commit_model.get_tags_for_commit()

    def get_commit_branch(self):
        return self.commit_model.get_branch_for_commit()

class SkillMarketValueAnalyzer:
    def __init__(self, repo_owner: str, repo_name: str, commit_sha: str):
        self.skill_scorer = ScoreSkillsForProject(repo_owner, repo_name, commit_sha)

    def analyze_skill_market_value(self):
        return self.skill_scorer.get_skill_market_value()
    







#example usage:

