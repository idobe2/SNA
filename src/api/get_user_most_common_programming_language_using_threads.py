import csv
import threading

import requests
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

# Personal Access Token from GitHub
ACCESS_TOKEN = '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'

start_time = time.time()

def get_user_repositories(username):
    """
    Fetches the repositories of a given user from the GitHub API.

    Args:
        username (str): The GitHub username.

    Returns:
        list: List of URLs to the languages of the user's repositories.
    """
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    # print(f"Fetching repositories for {username}...")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos_data = response.json()
        return [repo['languages_url'] for repo in repos_data]
    else:
        print(f"Failed to fetch repositories for {username}")
        return []


def get_most_common_language(languages):
    """
    Finds the most common programming language from a list of languages.

    Args:
        languages (list): List of programming languages.

    Returns:
        str: The most common programming language.
    """
    language_counter = Counter(languages)
    return language_counter.most_common(1)[0][0] if language_counter else 'No languages detected'


def process_user(row, request_counter):
    """
    Processes a user from the input CSV file.

    Args:
        row (dict): A dictionary containing user data.
        request_counter (Counter): Counter object to track the number of requests.

    Returns:
        dict or None: Processed user data with the most common language added, or None if user processing was skipped.
    """
    if row['bio'] != 'Bio not available':
        username = row['name']
        uid = row['id']
        repos_languages = []
        for repo_languages_url in get_user_repositories(username):
            response = requests.get(repo_languages_url, headers={"Authorization": f"token {ACCESS_TOKEN}"})
            request_counter['total_requests'] += 1
            if response.status_code == 200:
                repo_languages_data = response.json()
                repos_languages.extend(list(repo_languages_data.keys()))
                # Introduce a delay to stay within rate limit
                time.sleep(0.5)  # Adjust this delay as needed
            else:
                print(f"Failed to fetch repositories for {uid}: {username}")
        most_common_language = get_most_common_language(repos_languages)
        row['most_common_language'] = most_common_language
        print(f"Fetched data for {uid}: {username}: Most common language: {most_common_language}")
        return row
    else:
        print(f"Skipped! Bio not available for {row['id']}: {row['name']}")
        return None


def print_progress_message():
    """
    Prints a progress message every 10 seconds.
    """
    interval = 30
    while True:
        uptime = time.time() - start_time
        print(f"Running... req/hour: {int(request_counter['total_requests']/(uptime/60/60))} Total: {request_counter['total_requests']}")
        time.sleep(interval)


def main():
    input_file = '../../csv/sce3.csv'
    output_file = 'usernames_with_language.csv'
    global request_counter
    request_counter = Counter()

    progress_thread = threading.Thread(target=print_progress_message, daemon=True)
    progress_thread.start()

    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
            open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['most_common_language']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        with ThreadPoolExecutor(max_workers=4) as executor:
            results = executor.map(lambda x: process_user(x, request_counter), reader)
            for result in results:
                if result:
                    writer.writerow(result)


if __name__ == "__main__":
    main()
