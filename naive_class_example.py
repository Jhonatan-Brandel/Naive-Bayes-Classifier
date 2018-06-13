# -*- coding: utf-8 -*-
import json
import naive

# code you want to evaluate
naive=naive.naive_bayes_classifier()

#print(naive.corpus_words) #show corpora content


naive.reset_training() #reset training database

naive.training_classifier('intents/classificador.json') # certify for training once, else it will increase words frequency on traning database
#naive.training_classifier('intents/matemática.json')

print(naive.classify('obrigado'))
#print(naive.classify('muito obrigado por usar este programa'))



