import spacy
import get_input as gi
#spacy.cli.download("en_core_web_sm")   #<---------- ggf muss das hier laufen, falls es bisher nicht installiert ist.

nlp = spacy.load("en_core_web_sm")


input = gi.get_input_data()



def test_2(text):
    doc = nlp(text)

    for token in doc:
        print(token.text, token.pos_)
    #for ent in doc.ents:
        #print(ent.text, ent.label_)
        #print(ent.text, ent.label_)

    #print(doc.text)
    print(spacy.explain("GPE"))


test_2(input[0])


#for text_passage in input:
    #test_2(text_passage)


#token.text return the text of a token

#TODO #TODO #TODO #TODO #TODO #TODO #TODO #TODO
#Was können wir bisher:
#Wir können den Text von allen .xml Dateien lesen und diese mit mithilfe von Spacy mit PoS Tags versehen.