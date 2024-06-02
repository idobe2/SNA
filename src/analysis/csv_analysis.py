import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the uploaded CSV file
file_path = '../../csv/git_target_languages.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe to understand its structure and what kind of data it contains
data.head()

# Filter out entries where 'most_common_language' is "No languages detected" or similar
filtered_data = data[data['most_common_language'].str.lower() != 'no languages detected']

# Get the top 10 languages
top_languages = filtered_data['most_common_language'].value_counts().head(10).index

# Filter the dataframe to include only the top 10 languages
filtered_data = filtered_data[filtered_data['most_common_language'].isin(top_languages)]

# Create a pivot table to count the occurrences of each programming language split by ml_target
pivot_table = filtered_data.pivot_table(index='most_common_language', columns='ml_target', aggfunc='size', fill_value=0)

# Sort the pivot table by the total count
pivot_table = pivot_table.loc[top_languages]

# Plotting the distribution of the most common programming languages split by ml_target
plt.figure(figsize=(12, 8))
pivot_table.plot(kind='bar', stacked=True, color=['#1f77b4', '#ff7f0e'])
plt.title('Top 10 Most Common Programming Languages')
plt.xlabel('Programming Language')
plt.ylabel('Number of Users')
plt.xticks(rotation=45)
plt.legend(title='Developer type')
plt.grid(axis='y', linestyle='--')

plt.show()

# Adding a pie chart to visualize the split for each language
fig, axes = plt.subplots(2, 5, figsize=(20, 10))
axes = axes.flatten()
colors = ['#1f77b4', '#ff7f0e']

for i, language in enumerate(top_languages):
    language_data = pivot_table.loc[language]
    axes[i].pie(language_data, labels=language_data.index, colors=colors, autopct='%1.1f%%', startangle=140)
    axes[i].set_title(language)

plt.suptitle('Distribution of Top 10 Most Common Programming Languages Split by ML Target')
plt.tight_layout(rect=[0, 0, 1, 0.96])

plt.show()
