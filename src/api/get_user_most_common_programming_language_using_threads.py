import csv
import threading
import requests
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import sys
import os

sys.path.append(os.path.abspath('../../'))
sys.path.append(os.path.abspath('src'))
from src.config import ENTERPRISE_ACCESS_TOKEN

start_time = time.time()


def get_user_repositories(username, error_counter):
    """
    Fetches the repositories of a given user from the GitHub API.

    Args:
        username (str): The GitHub username.

    Returns:
        list: List of URLs to the languages of the user's repositories.
    """
    try:
        url = f"https://api.github.com/users/{username}/repos"
        headers = {
            "Authorization": f"token {ENTERPRISE_ACCESS_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for non-200 status codes
        repos_data = response.json()
        return [repo['languages_url'] for repo in repos_data]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories for {username}")
        if error_counter['total_error'] < 5:
            error_counter['total_error'] += 1
        else:
            print("Exceed rate limit! Waiting 15 minutes...")
            time.sleep(900)
            error_counter['total_error'] = 0
            get_user_repositories(username, error_counter)  # Try again
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


def process_user(row, request_counter, error_counter):
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
        for repo_languages_url in get_user_repositories(username, error_counter):
            try:
                response = requests.get(repo_languages_url,
                                        headers={"Authorization": f"token {ENTERPRISE_ACCESS_TOKEN}"})
                request_counter['total_requests'] += 1
                response.raise_for_status()  # Raise an error for non-200 status codes
                repo_languages_data = response.json()
                repos_languages.extend(list(repo_languages_data.keys()))
                # Introduce a delay to stay within rate limit
                time.sleep(1.0)  # Adjust this delay as needed
            except requests.exceptions.RequestException as e:
                print(f"Error fetching repositories for {uid}: {username}")
        most_common_language = get_most_common_language(repos_languages)
        row['most_common_language'] = most_common_language
        print(f"Fetched data for {uid}: {username}: Most common language: {most_common_language}")
        return row
    else:
        print(f"Skipped! Bio not available for {row['id']}: {row['name']}")
        return None


def print_progress_message():
    """
    Prints a progress message every 15 seconds.
    """
    interval = 15
    while True:
        uptime = time.time() - start_time
        requests_per_hour = (int(request_counter['total_requests'] / (uptime / 60 / 60)))
        print(
            f"[Running] req/hour: {requests_per_hour} Total: {request_counter['total_requests']}")
        time.sleep(interval)


def save_to_csv(results, writer):
    """
    Saves processed user data to CSV.

    Args:
        results (iterator): Processed user data.
        writer (csv.DictWriter): CSV writer object.
    """
    for result in results:
        if result:
            writer.writerow(result)


def main():
    input_file = '../../csv/usernames_with_bio.csv'
    output_file = 'usernames_with_language.csv'
    global request_counter, error_counter
    request_counter = error_counter = Counter()
    progress_thread = threading.Thread(target=print_progress_message, daemon=True)
    progress_thread.start()

    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
            open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['most_common_language']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = executor.map(lambda x: process_user(x, request_counter, error_counter), reader)
            try:
                save_to_csv(results, writer)
            except KeyboardInterrupt:
                print("Saving data before exit...")
                save_to_csv(results, writer)
                raise  # Re-raise KeyboardInterrupt after saving data
            finally:
                # Make sure to consume all remaining results
                for _ in results:
                    pass


if __name__ == "__main__":
    main()
