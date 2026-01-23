#skill_scorer_for_commits_based_on_analysis
from app.services.commit_analyzer import CommitAnalyzer
skills_type ={
    "a": "Excellent",
    "b": "Good",
    "c": "Average",
    "d": "Poor"

}
    
class SkillScorer:
    def __init__(self, repo_owner: str, repo_name: str, commit_sha: str):
        self.analyzer = CommitAnalyzer(repo_owner, repo_name, commit_sha)

    def score_skills(self):
        grade = self.analyzer.grade_commit()
        significant = self.analyzer.is_significant_commit()

        skill_score = {
            "grade": grade,
            "is_significant": significant
        }
        return skill_score
    def get_skill_report(self):
        score = self.score_skills()
        report = (
            f"Skill Scoring Report:\n"
            f"---------------------\n"
            f"Commit Grade: {score['grade']}\n"
            f"Significant Commit: {'Yes' if score['is_significant'] else 'No'}"
        )
        return report
    def get_skill_summary(self):
        score = self.score_skills()
        summary = {
            "commit_grade": score['grade'],
            "significant_commit": score['is_significant']
        }
        return summary
    def detailed_skill_analysis(self):
        analysis = self.analyzer.analyze_commit()
        detailed_analysis = {
            "commit_message": analysis['commit_message'],
            "author_info": analysis['author_info'],
            "commit_stats": analysis['commit_stats'],
            "changed_files": self.analyzer.get_changed_files(),
            "skill_score": self.score_skills()

        }
        return detailed_analysis
class GiveJob_position:
    def __init__(self, repo_owner: str, repo_name: str, commit_sha: str):
        self.analyzer = CommitAnalyzer(repo_owner, repo_name, commit_sha) 
    def suggest_position(self):
        grade = self.analyzer.grade_commit()
        position = "Junior Developer"
        if grade == "A":
            position = "Senior Developer"
        elif grade == "B":
            position = "Mid-level Developer"
        return position
    def get_position_report(self):
        position = self.suggest_position()
        report = (
            f"Job Position Suggestion Report:\n"
            f"-------------------------------\n"
            f"Suggested Position: {position}"
        )
        return report
    def get_position_summary(self):
        position = self.suggest_position()
        summary = {
            "suggested_position": position
        }
        return summary
    def detailed_position_analysis(self):
        analysis = self.analyzer.analyze_commit()
        detailed_analysis = {
            "commit_message": analysis['commit_message'],
            "author_info": analysis['author_info'],
            "commit_stats": analysis['commit_stats'],
            "changed_files": self.analyzer.get_changed_files(),
            "suggested_position": self.suggest_position()

        }
        return detailed_analysis
    