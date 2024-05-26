import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the uploaded CSV file
file_path = '../../csv/git_target_languages.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe to understand its structure and what kind of data it contains
data.head()

# Count the occurrences of each programming language
language_counts = data['most_common_language'].value_counts()

# Filter out entries where 'most_common_language' is "No languages detected" or similar
filtered_language_counts = data[data['most_common_language'].str.lower() != 'no languages detected'][
    'most_common_language'].value_counts()

# Plot only the top 10 languages (excluding "No languages detected") for better readability
top_languages_filtered = filtered_language_counts.head(10)

np.random.seed(0)  # For reproducibility
colors = np.random.rand(len(top_languages_filtered), 3)  # Generate as many colors as there are languages

# Plotting the distribution of the most common programming languages
plt.figure(figsize=(10, 6))
top_languages_filtered.plot(kind='bar', color=colors)
plt.title('Top 10 Most Common Programming Languages Among GitHub Users')
plt.xlabel('Programming Language')
plt.ylabel('Number of Users')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--')

plt.show()

# Adding a pie chart to visualize the same data
plt.figure(figsize=(10, 8))
top_languages_filtered.plot(kind='pie', colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Top 10 Most Common Programming Languages Among GitHub Users')
plt.ylabel('')  # Hide the y-label as it's unnecessary for a pie chart
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
