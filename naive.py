import json
	
	
	
def tokenize(string):
		string=string.replace("."," ")
		string=string.replace("'"," ")
		string=string.replace('"'," ")
		string=string.replace(":"," ")
		string=string.replace(","," ")
		string=string.replace('\\', ' ')
		string=string.replace("\n"," ")
		string=string.replace("."," ")
		#apagar espaços repetidos para fazer o parsing corretamente
		aux_str=string
		string=string.replace("  "," ")
		while string!=aux_str:
			aux_str=string
			string=string.replace("  "," ")
			
		
		return string.split(" ")

# -*- coding: utf-8 -*-


class naive_bayes_classifier:
		
		def __init__(self):		
			self.training_data = []
			# capture unique stemmed words in the training corpus
			self.corpus_words = {}
			self.class_words = {}
			self.classes=[]
			self.load_variables()#assim que inicia já carrega o arquivo que tem os valores das variáveis, bem legal!
		
		#____________________________________________________________________________________________________________________________________________________
		def save_variables(self):
			try:
				data={'corpus_words':self.corpus_words,"class_words":self.class_words,"classes":self.classes,"training_data":self.training_data}
				#print (json.dumps(data, sort_keys=True, indent=4 ,ensure_ascii=False))
				with open('classification.json', 'w') as f:
				  json.dump(data, f, ensure_ascii=False)
			except:
				pass	  
		
		#____________________________________________________________________________________________________________________________________________________
		def load_variables(self):
			try:
				fp = open("classification.json", "r")
				data = json.load(fp)
				fp.close()
				self.training_data=data['training_data']
				self.corpus_words = data['corpus_words']
				self.class_words = data['class_words']
				self.classes=data['classes']
			except:
				pass	
		
		#____________________________________________________________________________________________________________________________________________________
		
		def reset_training(self):
			#reseta as variáveis de dados para não haver erro de contagem, é extremamente necessário
			self.training_data = []
			self.corpus_words = {}
			self.class_words = {}
			self.classes=[]
			#TEM QUE TER UMA FUNÇÃO PARA APAGAR O ARQUIVO DE CLASSIFICAÇÃO
						
		def training_classifier(self,file_name):#testando com nome repetido dentro da função<<<<<<<<<<<
					
			fp = open(file_name, "r")
			obj = json.load(fp)
			fp.close()
			for e in obj['training']:
				if e!=None:
					#print(e)
					self.training_data.append(e)
			self.classes = list(set([a['class'] for a in self.training_data]))
			for c in self.classes:
			    # prepare a list of words within each class
			    self.class_words[c] = []
			
			# loop through each sentence in our training data
			for data in self.training_data:
			    # tokenize each sentence into words
			    for word in tokenize(data['sentence']):
			        # ignore a some things
			        
			        if word not in ["?", "'s"]:
			            # stem and lowercase each word
			            word = word.lower()#tinha uma funçao de stemm aqui, eu a removi pois era do pacote nltk
			            # have we not seen this word already?
			            if word not in self.corpus_words:
			                self.corpus_words[word] = 1
			            else:
			                self.corpus_words[word] += 1
			
			            # add the word to our words in class list
			            self.class_words[data['class']].extend([word])
		
			
			#____________________________________________________________________________________________________________________________________________________
			# we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
			#print ("Corpus words and counts: %s \n" % corpus_words)
			# also we have all words in each class
			#print ("Class words: %s" % class_words)
			self.save_variables()# já salva arquivo assim que termina a nova classificação
			return	
		
		
		
		#____________________________________________________________________________________________________________________________________________________	
		#print(training_data)
		#print(training_classifier('classificador.json'))
		#training_data.append(training_classifier('classificador.json'))
		#print(training_data)
		#training_classifier('classificador.json')
		
		
		#print ("%s sentences of training data" % len(training_data))
		#print(training_data)
		
		#____________________________________________________________________________________________________________________________________________________
		
		# turn a list into a set (of unique items) and then a list again (this removes duplicates)
		
		
		
		# calculate a score for a given class taking into account word commonality
		def calculate_class_score_commonality(self,sentence, class_name, show_details=True):
		    score = 0
		    # tokenize each word in our new sentence
		    for word in tokenize(sentence):
		        # check to see if the stem of the word is in any of our classes
		        if word in self.class_words[class_name]:
		            # treat each word with relative weight
		            score += (1 / self.corpus_words[word])
		
		            if show_details:
		               print ("   match: %s (%s)" % ( word , 1 / self.corpus_words[word]))
		    return score
		
		
		
		
		#____________________________________________________________________________________________________________________________________________________
		# now we can find the class with the highest score
		#for c in class_words.keys():
		#   print ("Class: %s  Score: %s \n" % (c, calculate_class_score(sentence, c)) )
		
		# return the class with highest score for sentence
		def classify(self,sentence):
			sentence=sentence.lower()
			high_class = None
			high_score = 0
			# loop through our classes
			for c in self.class_words.keys():
			# calculate score of sentence for each class
				score = self.calculate_class_score_commonality(sentence, c, show_details=False)
				# keep track of highest score
				if score > high_score:
					high_class = c
					high_score = score
			
			return high_class, high_score
		#____________________________________________________________________________________________________________________________________________________
		
		

#criar o banco de dados para as variáveis corpus_word, class_words e classes, em um arquivo json,
#pois assim não será necessário treinar o classificador toda vez que o programa ser executado.
#Isso ajuda muito quando o banco de dados é grande.


#COMBINAR O CLASSIFICADOR COM DISTANCIA DE LEVENSHTEIN PARA SER MENOS ESTRITO AO TEXTO, E TOLERAR ERROS DE PORTUGUES
