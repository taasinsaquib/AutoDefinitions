import json
import os
import io

from dictionary_scrape import DictionaryScrape

def main():
	# get list of words from file
	repoLocation = ''	# TODO: put path of repository here before running
	filepath     = os.path.join(repoLocation, 'Words', 'vocab_list.txt')

	scrape = DictionaryScrape()

	# open output file to write to
	fileOut = io.open('definitions.txt','w+', encoding='utf8')

	with open(filepath) as f:
		content = f.readlines()

		for line in content:
			try:
				word = scrape.getWordInfo(line.rstrip())
				wordInfoDump = scrape.printWordInfo(word)
			except Exception as e:
				fileOut.write(str(e).decode('utf-8'))

			fileOut.write(wordInfoDump)
			print(wordInfoDump)

	fileOut.close()

if __name__== "__main__":
	main()