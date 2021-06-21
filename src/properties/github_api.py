from github import Github as PyGithub, GithubException


class GithubAPIHandler(PyGithub):
    def __init__(self, access_token: str) -> None:
        try:
            super().__init__(access_token)

        except GithubException as InitHandlerErr:
            print(f"Initialization Error: {InitHandlerErr}")

    def check_commit_constraint(self, commit_date: PyGithub.Commit) -> bool:

        # print
        pass

    def create_commit_payload(self):
        pass

    # def

    def __str__(self):
        pass

if __name__ == "__main__":
    raise SystemExit("You're about to run a Properties Module which is not allowed! Run the src/entrypoint.py instead!")