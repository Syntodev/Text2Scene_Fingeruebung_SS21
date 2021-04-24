import spacy
import get_input as gi

#print("it works")
#spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion. I'm curious to see if this is a good idea.")
for token in doc:
    print(token.text, token.pos_, token.dep_)
document = gi.get_input_data()

#print("nice")