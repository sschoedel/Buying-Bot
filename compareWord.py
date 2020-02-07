# Lets you copmpare a word to a list of words within a given accuracy (within one keyboard char adjacent to each in the string)
# and returns whether or not the word exists in that list


possibleCharReplacements = {}

def findNear(r, c):
	origChar = keyboardChars[r][c]
	near = []
	if c > 0:
		near.append(keyboardChars[r][c-1])
	if c < 9:
		near.append(keyboardChars[r][c+1])
	if r > 0:
		near.append(keyboardChars[r-1][c])
	if r < 3:
		near.append(keyboardChars[r+1][c])
	if c > 0 and r > 0:
		near.append(keyboardChars[r-1][c-1])
	if c > 0 and r < 3:
		near.append(keyboardChars[r+1][c-1])
	if c < 9 and r > 0:
		near.append(keyboardChars[r-1][c+1])
	if c < 9 and r < 3:
		near.append(keyboardChars[r+1][c+1])
	return near

possibleCharReplacements = {'q' : ['w','a','1','2'], 'w' : ['2','1','3','q','e','d','s','a'], 'e' : ['2','3','4','w','r','s','f','d']}
keyboardChars = ["1234567890","qwertyuiop","asdfghjkl;","zxcvbnm,./"]
keyboardChars = [list(keyboardChars[n]) for n in range(len(keyboardChars))]
# allChars = split('1234567890qwertyuiopasdfghjkl;zxcvbnm,./')
for r in range(len(keyboardChars)): # rows
	for c in range(len(keyboardChars[0])): # then columns
		possibleCharReplacements.update({keyboardChars[r][c] : findNear(r,c)})

def genPossReplacements(discWord):
	possWordReplacements = []
	for i,c in enumerate(discWord):
		if c in possibleCharReplacements:
			for replacementC in possibleCharReplacements[c]:
				tempWord = list(discWord)
				tempWord[i] = replacementC
				possWordReplacements.append("".join(tempWord))
	# return [replacements.lower() for replacements in possWordReplacements]
	return possWordReplacements
def compare(word, discoveredWords):
	# Generate all words to within one letter of the original for all words in discoveredWords
	# Ex: given word: paper   acceptable words: aper, pper, paer, papr, pape, qaper, pbper
	# Would be better to generate list of acceptable words by choosing only letters around a specific letter
	# string = 'ABC'
	# string = string.lower()
	# > 'abc'
	result = False
	for discWord in discoveredWords:
		print(f'word.lower(): {word.lower()}, replacements: {genPossReplacements(discWord)}')
		print("HI")
		if word.lower() in genPossReplacements(discWord):
			result = True
			break
	return result