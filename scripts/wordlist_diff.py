# Load two wordlists and output the words in the second list that are not contained in,
# or have a different score from, the first list.
#
# Larry Snyder
# 4/4/23

import csv


##############################
#
# THIS IS THE ONLY PORTION YOU NEED TO EDIT...
#
# Put paths to your wordlists here. 
# wordlist1 is the original wordlist (i.e., the one before you made changes).
# wordlist2 is the wordlist with your changes.
wordlist1_path = "Wordlists/spreadthewordlist.dict"
wordlist2_path = "Wordlists/spreadthewordlist-myedits.dict"
#
# Put path to your desired output file here. (The file will be overwritten if it
# already exists.)
output_path = "Wordlists/diff.dict"
#
##############################


def read_wordlist(wordlist_path, min_score=None):
	"""Read a wordlist file and return a dict in which the keys are words and
	the values are scores.

	If min_score is set, only returns words with at least that score.
	"""

	# Initialize data.
	words = set()
	scores = {}

	# Read and process wordlist file. 
	with open(wordlist_path) as f:
		lines = f.readlines()
		for line in lines:
			parts = line.strip().upper().split(';')
			word = parts[0]
			score = int(parts[1])
			if word not in words:
				words.add(word)
				scores[word] = score 
	
	# Remove words with score < min_score.
	word_dict = {w: scores[w] for w in words if scores[w] > (min_score or -1)}

	return word_dict


# Load both wordlists.
wordlist1 = read_wordlist(wordlist1_path)
print(f"{wordlist1_path} contains {len(wordlist1)} entries")
wordlist2 = read_wordlist(wordlist2_path)
print(f"{wordlist2_path} contains {len(wordlist2)} entries")

# Initialize outputs.
diff_list = []
num_rescored = 0
num_new = 0
max_len = max([len(w) for w in wordlist2])

# Determine differences.
for w in wordlist2:
	if w not in wordlist1:
		diff_list.append((w, wordlist2[w]))
		print(f"word {w:{max_len}} not in {wordlist1_path}")
		num_new += 1
	elif wordlist1[w] != wordlist2[w]:
		diff_list.append((w, wordlist2[w]))
		print(f"word {w:{max_len}} scored {wordlist2[w]:3d} in {wordlist2_path} but {wordlist1[w]:3d} in {wordlist1_path}")
		num_rescored += 1

print(f"{num_rescored} rescored words found, {num_new} new words found")

# Write to output file.
with open(output_path, 'w') as out:
	csv_out = csv.writer(out, delimiter=";")
	csv_out.writerows(diff_list)
	
print(f"wrote results to {output_path}")

