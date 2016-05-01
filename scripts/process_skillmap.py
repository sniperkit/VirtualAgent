import json
import os
import string

import numpy as np
import pandas as pd

# define constants

PRINTABLE = set(string.printable)
PATH_TO_DATA = os.getcwd()[:-7] + 'data/'

# Load skill-map.json

with open(PATH_TO_DATA + 'skill-map.json') as data_file:
	data = json.load(data_file)

# Generate parent and child lists

keys = data.keys()
parent_list = []
child_list = []

for key in data.keys():

	# Don't include non-english entries

	english = True

	for chr in key:

		if chr not in PRINTABLE:

			english = False
			break

	if not english:

		continue

	parent_list.append(key)

	children = []

	for child in data[key]:
		children.append(child.encode('utf-8'))


	child_list.append(children)


# get children into their own lists, along with related terms and parents

extracted_children = []
parents = []
related_terms = []
index = 0

for entry in child_list:

	for skill in entry:
		related = entry
		related.remove(skill) 
		extracted_children.append(skill)
		related_terms.append(related)
		parents.append(parent_list[index])


	index += 1

# Generate dataframe skill_rel

skill_rel = pd.DataFrame({"keywords": pd.Series(extracted_children),
						  "parents": pd.Series(parents),
						  })


# Hand crafted sorting

# Move all rows with SQL to Databases
SQL_parents_index = np.ndarray.tolist(skill_rel[~skill_rel['parents'].str.contains("^((?!SQL).)*$")].index.values)
skill_rel['parents'].ix[SQL_parents_index] = 'Databases'

# Move all rows with database to Databases
database_parents_index = np.ndarray.tolist(skill_rel[~skill_rel['parents'].str.contains("^((?!database).)*$")].index.values)
skill_rel['parents'].ix[database_parents_index] = 'Databases'

# Move all rows with Database to Databases
Database_parents_index = np.ndarray.tolist(skill_rel[~skill_rel['parents'].str.contains("^((?!Database).)*$")].index.values)
skill_rel['parents'].ix[Database_parents_index] = 'Databases'

# Move Backend Development to Backend
backend_parents_index = np.ndarray.tolist(skill_rel[~skill_rel['parents'].str.contains("^((?!Backend).)*$")].index.values)
skill_rel['parents'].ix[backend_parents_index] = 'Backend'

# Move Backend Development to Backend
backend_parents_index = np.ndarray.tolist(skill_rel[~skill_rel['parents'].str.contains("^((?!Back End).)*$")].index.values)
skill_rel['parents'].ix[backend_parents_index] = 'Backend'

# Move Backend Development to Backend
backend_parents_index = np.ndarray.tolist(skill_rel[~skill_rel['parents'].str.contains("^((?!Back-end).)*$")].index.values)
skill_rel['parents'].ix[backend_parents_index] = 'Backend'

# Move Frontend Development to Frontend
frontend_parents_index = np.ndarray.tolist(skill_rel[~skill_rel['parents'].str.contains("^((?!Front).)*$")].index.values)
skill_rel['parents'].ix[frontend_parents_index] = 'Frontend'

# Move Languages to Programming
Languages_parents_index = np.ndarray.tolist(skill_rel[~skill_rel['parents'].str.contains("^((?!Languages).)*$")].index.values)
skill_rel['parents'].ix[Languages_parents_index] = 'Programming'

# Move Software to Development
Software_parents_index = np.ndarray.tolist(skill_rel[~skill_rel['parents'].str.contains("^((?!Software).)*$")].index.values)
skill_rel['parents'].ix[Software_parents_index] = 'Development'

# Move DevOps to Development
DevOps_parents_index = np.ndarray.tolist(skill_rel[~skill_rel['parents'].str.contains("^((?!DevOps).)*$")].index.values)
skill_rel['parents'].ix[DevOps_parents_index] = 'Development'

# Move HTML to Web Development
HTML_parents_index = np.ndarray.tolist(skill_rel[~skill_rel['parents'].str.contains("^((?!HTML).)*$")].index.values)
skill_rel['parents'].ix[HTML_parents_index] = 'Web Development'

# Drop update later

skill_rel = skill_rel[(skill_rel.keywords != 'update later')]
skill_rel = skill_rel[(skill_rel.keywords != '')]

# create associtated score col

# skill_rel['score'] = 0.0 

# print skill_rel['keywords'].value_counts()
# print skill_rel['parents'].value_counts()

# print skill_rel

# export unique wordlist

# pd.Series(skill_rel["keywords"].unique()).to_json(PATH_TO_DATA + "unique_keywords.json",orient='records')

# This gives us the normalized relation to a particular category

# def calculation(value):

# 	return float(value)

# for par in skill_rel['parents'].unique():
# 	#print "currently on" + par
# 	normed_values = skill_rel[(skill_rel['parents'] == par)]['keywords'].value_counts() / sum(skill_rel[(skill_rel['parents'] == par)]['keywords'].value_counts())
# 	#print normed_values

# 	for key in skill_rel[(skill_rel['parents'] == par)]['keywords'].value_counts().keys():
# 		#print "currently working on " + key
# 		skill_rel[(skill_rel['parents'] == par) & (skill_rel.keywords == key)]['score'] = 1
# 		print type(normed_values[key]) 
# 		print skill_rel[(skill_rel['parents'] == par) & (skill_rel.keywords == key)]['score']
# 		#print normed_values[key]
# 		#print skill_rel[(skill_rel.parents == par) & (skill_rel.keywords == key)]['score']

# print skill_rel['score'].unique()


# skill_rel[(skill_rel.parents == 'Web Development')]['keywords'].value_counts() / sum(skill_rel[(skill_rel.parents == 'Web Development')]['keywords'].value_counts())

# skill_rel
# print skill_rel[(skill_rel.parents == 'Databases')]['keywords'].value_counts()
# print skill_rel[(skill_rel.parents == 'Backend')]['keywords'].value_counts()
# print skill_rel[(skill_rel.parents == 'Frontend')]['keywords'].value_counts()

# print skill_rel[(skill_rel.parents == 'Web Development')]['keywords'].unique
# print skill_rel[(skill_rel.parents == 'Databases')]['keywords'].unique()
# print skill_rel[(skill_rel.parents == 'Backend')]['keywords'].unique()
# print skill_rel[(skill_rel.parents == 'Frontend')]['keywords'].unique()



# print skill_rel


def get_popular_tag(keyword):

	return skill_rel[(skill_rel.keywords == keyword)]['parents'].value_counts().idxmax()



def get_parents_top_keys(parent):

	return skill_rel[(skill_rel.parents == parent)]['keywords'].value_counts().index[0:5].values

related_terms = []

for key in skill_rel['keywords']:
	related_terms.append(get_parents_top_keys(get_popular_tag(key)))

skill_rel['related_terms'] = related_terms

skill_rel = skill_rel.drop('parents', 1)
skill_rel.drop_duplicates(['keywords'], take_last=True)
PATH_TO_DATA = os.getcwd()[:-7] + 'data/'

skill_rel.to_json(PATH_TO_DATA + 'relations.json', orient='records')


