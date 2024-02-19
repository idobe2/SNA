import csv
import requests
from collections import Counter

# Personal Access Token from GitHub
ACCESS_TOKEN = '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'


def get_user_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos_data = response.json()
        return [repo['languages_url'] for repo in repos_data]
    else:
        print(f"Failed to fetch repositories for {username}")
        return []


def get_most_common_language(languages):
    language_counter = Counter(languages)
    return language_counter.most_common(1)[0][0] if language_counter else 'No languages detected'


def main():
    input_file = '../../csv/usernames_with_bio.csv'
    output_file = 'usernames_with_language.csv'

    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
            open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['most_common_language']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if row['bio'] != 'Bio not available':
                username = row['name']
                repos_languages = []
                for repo_languages_url in get_user_repositories(username):
                    response = requests.get(repo_languages_url, headers={"Authorization": f"token {ACCESS_TOKEN}"})
                    if response.status_code == 200:
                        repo_languages_data = response.json()
                        repos_languages.extend(list(repo_languages_data.keys()))
                most_common_language = get_most_common_language(repos_languages)
                row['most_common_language'] = most_common_language
                writer.writerow(row)
                print(f"Fetched data for {username}: Most common language: {most_common_language}")
            else:
                print(f"Skipped! Bio not available for {row['name']}")


if __name__ == "__main__":
    main()