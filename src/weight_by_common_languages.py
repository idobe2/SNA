import pandas as pd

# Read the CSV file
df = pd.read_csv("../csv/usernames_with_language.csv")


# Define a function to assign weight based on programming language
def assign_weight(language):
    common_languages = [
        "Python", "JavaScript", "Java", "HTML", "CSS", "C++", "C#", "C",
        "TypeScript", "Shell", "Ruby", "PHP", "Perl", "Objective-C", "PowerShell",
        "Go"
    ]
    moderate_languages = [
        "Swift", "R", "MATLAB", "Makefile", "Jupyter Notebook", "Julia", "Haskell",
        "GDScript", "Elixir", "Dart", "Cuda", "Crystal", "CMake", "Clojure",
        "Batchfile"
    ]
    uncommon_languages = [
        "Vim Script", "Nginx", "Markdown", "Emacs Lisp", "Dockerfile", "AutoHotkey"
    ]

    if language in common_languages:
        return 4
    elif language in moderate_languages:
        return 3
    elif language in uncommon_languages:
        return 2
    elif language == "No languages detected":
        return 0
    else:
        return 1


# Apply the function to each row to create the weight column
df['weight'] = df['most_common_language'].apply(assign_weight)

# Write the updated DataFrame to a new CSV file
df.to_csv("usernames_with_weight.csv", index=False)
