import os
import requests
from github import Github

# Authenticate to GitHub
g = Github(os.getenv('GITHUB_TOKEN'))

# Get the repository
repo = g.get_repo("YOUR_GITHUB_USERNAME/YOUR_REPOSITORY")

# Fetch the latest submissions from Formspree (replace with your Formspree API endpoint)
response = requests.get("https://formspree.io/api/forms/YOUR_FORM_ID/submissions")
submissions = response.json()

# Process and update the repository with new submissions
for submission in submissions:
    header = submission['data']['header']
    description = submission['data']['description']
    pfd_image_url = submission['data']['pfd_image']

    # Download the image
    image_response = requests.get(pfd_image_url)
    image_path = f"submissions/{header.replace(' ', '_')}.jpg"
    with open(image_path, 'wb') as image_file:
        image_file.write(image_response.content)

    # Add the submission to the README file or any other documentation file
    with open("README.md", "a") as readme_file:
        readme_file.write(f"\n## {header}\n")
        readme_file.write(f"{description}\n")
        readme_file.write(f"![{header}]({image_path})\n")

# Commit and push the changes to the repository
repo.index.add(["README.md", "submissions/"])
repo.index.commit("Update submissions")
repo.remote().push()
