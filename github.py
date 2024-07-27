import requests
import os
import git

class GitHubRepository:
    def __init__(self, github_username, github_token, repo_name, repo_description, repo_visibility):
        self.github_username = github_username
        self.github_token = github_token
        self.repo_name = repo_name
        self.repo_description = repo_description
        self.repo_visibility = repo_visibility
        self.repo_url = f'https://github.com/{github_username}/{repo_name}.git'

    def create_repo(self):
        url = f'https://api.github.com/user/{self.github_username}/repos'
        headers = {
            'Authorization': f'token {self.github_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'name': self.repo_name,
            'description': self.repo_description,
            'visibility': self.repo_visibility
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            print(f'Repository created successfully: {self.repo_name}')
        else:
            print(f'Error creating repository: {response.text}')

    def clone_repo(self):
        os.system(f'git clone {self.repo_url}')

    def add_file(self, filename, contents):
        repo = git.Repo(self.repo_url)
        with open(filename, 'w') as f:
            f.write(contents)
        repo.git.add(filename)
        repo.git.commit(m=f'Added {filename}')

    def push_changes(self):
        repo = git.Repo(self.repo_url)
        repo.git.push()

# Example usage:
github_username = 'your-github-username'
github_token = 'your-github-personal-access-token'
repo_name = 'my-new-repo'
repo_description = 'This is my new repository'
repo_visibility = 'public'

repo = GitHubRepository(github_username, github_token, repo_name, repo_description, repo_visibility)
repo.create_repo()
repo.clone_repo()

# Add a new file
repo.add_file('example.txt', 'Hello, world!')

# Commit and push changes
repo.push_changes()