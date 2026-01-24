from commit import CommitModel
class ScoreSkillsForProject:
    def __init__(self, repo_owner, repo_name, commit_sha):
        self.commit_model = CommitModel(repo_owner, repo_name, commit_sha)

    def score_skills(self):
        commit_message = self.commit_model.get_commit_message()
        author_info = self.commit_model.get_author_info()
        commit_stats = self.commit_model.get_commit_stats()

        skill_score = 0

        # Simple scoring logic based on commit message length and stats
        if len(commit_message) > 50:
            skill_score += 5
        elif len(commit_message) > 30:
            skill_score += 3
        else:
            skill_score += 1

        skill_score += commit_stats['additions'] // 10
        skill_score += commit_stats['deletions'] // 10

        return {
            "author": author_info['name'],
            "skill_score": skill_score
        }
    def get_skill_market_value(self):
        skill_data = self.score_skills()
        base_value = 1000  # Base market value
        market_value = base_value + (skill_data['skill_score'] * 100)
        return {
            "author": skill_data['author'],
            "market_value": market_value
        }
