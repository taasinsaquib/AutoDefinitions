from lxml import html
import requests
import json

class DictionaryScrape:
	
	# Currently scraping dictionary.com
	url = 'https://www.dictionary.com/browse/'
	urlParameters = { 's' : 'ts'}

	# XML paths to access the data we want
	_XmlPartOfSpeech 		= '//*[@id="base-pw"]/div/main/section/section/div[1]/section[2]/h3/span[1]/span/text()'
	_XmlWordInfoContainer	= '//*[@id="base-pw"]/div/main/section/section/div[1]/section[2]/div/div'
	_XmlWordInfo 			= '//*[@id="base-pw"]/div/main/section/section/div[1]/section[2]/div/div[$]/span'

	"""Print out information in object returned from self.getWordInfo
	[in]  wordJSON as a stringified JSON object
	[out] string
	"""
	def printWordInfo(self, wordJSON):

		wordString = ''

		word = json.loads(wordJSON)

		wordString += word['word'] + ' - '
		wordString += word['partOfSpeech'] + '\n'

		for definition in word['definitions']:
			wordString += '\t* ' + definition['definition'] + '\n'
			wordString += '\t\tex. ' + definition['usage'] + '\n'

		wordString += '\n'

		return wordString

	"""Get parts of speech, definitions, and usage for a word
	[in]  word as a string
	[out] stringified JSON object
	"""
	def getWordInfo(self, word):

		# store data to populate JSON object
		partofSpeech = ''
		definitions = []

		page = requests.get(self.url + word, self.urlParameters)
		tree = html.fromstring(page.content)
		
		# *********** Part of speech ***********
		partOfSpeechElements = tree.xpath(self._XmlPartOfSpeech)

		try:
			partofSpeech = partOfSpeechElements[0]
		except:
			raise Exception("No part of speech found for: " + word + '\n')

		# *********** Definitions and usage examples ***********
		definitionsElements = tree.xpath(self._XmlWordInfoContainer)

		for i in range(0, len(definitionsElements)):

			# XML index starts from 1
			wordXpath = self._XmlWordInfo.replace('$', str(i + 1))
			defin = tree.xpath(wordXpath)	

			# parts of the definition could be stored in a child anchor tag, collect those here
			# HTML tag broken up in interesting way when multiple anchor tags exist, text could be lost in these cases
			tags = ''
			usage = ''
			
			# Assume there is always 1 Element returned here in defin, so access defin[0]
			try:
				for i, child in enumerate(defin[0].getchildren()):
					# last child is usage
					if (i == len(defin[0].getchildren()) - 1):
						usage = child.text
					else:
						tags += child.text.strip()
						tags += ' '

				definitionData = {
					'definition': defin[0].text + tags,
					'usage': usage
				}

				definitions.append(definitionData)

			except:
				raise Exception("No definition found for: " + word + '\n')

		# *********** Create return object ***********
		wordInfo = {
			"word": word,
			"partOfSpeech": partofSpeech,
			"definitions": definitions
		}

		return json.dumps(wordInfo)
