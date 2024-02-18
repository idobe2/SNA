import csv
import requests

# Personal Access Token from GitHub
ACCESS_TOKEN = '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'

def get_user_bio(username):
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        bio = user_data.get('bio', 'No bio provided')
        return bio
    else:
        print(f"Failed to fetch bio for {username}")
        return None

def main():
    input_file = '../../csv/musae_git_target.csv'
    output_file = 'usernames_with_bio.csv'

    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['bio']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            username = row['name']
            bio = get_user_bio(username)
            if bio is not None:
                row['bio'] = bio
                writer.writerow(row)
                print(f"Fetched bio for {username}")
            else:
                row['bio'] = 'Bio not available'
                writer.writerow(row)
                print(f"Bio not available for {username}")

if __name__ == "__main__":
    main()
