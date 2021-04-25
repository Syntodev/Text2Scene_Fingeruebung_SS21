import spacy
import get_input as gi
import csv
import os
#spacy.cli.download("en_core_web_sm")   #<---------- ggf muss das hier laufen, falls es bisher nicht installiert ist.


nlp = spacy.load("en_core_web_sm")


def create_dir_for_saving_data(new_directory_name):
    show_warnings = 0
    show_info = 0
    cur_abs_path = os.path.abspath("")
    path = os.path.join(cur_abs_path, new_directory_name)
    if show_info == 1:
        print("Wir versuchen den Ordner '"+str(new_directory_name)+"' zu erstellen um dort die von Spacy tokenisierten und"
              " mit PoS versehenen Texte zu speichern.")
    try:
        os.mkdir(path)
        print("Wir haben einen neuen Order mit dem Pfad:",path,"erstellt.")
    except FileExistsError:
        if show_warnings == 1:
            print("Der Ordner '"+str(new_directory_name)+"' existiert bereits, wir werden ihn nicht erneut erstellen.")
    except:
        print("Ein unvorhergesehener Fehler ist aufgetreten.")
        print("GGF. stimmt etwas mit dem Pfad für die Ordnererstellung nicht.")


def write_into_csv_file(new_directory_name, output_csv_filename, all_texts):
    cur_abs_path = os.path.abspath("")
    path = os.path.join(cur_abs_path, new_directory_name)
    os.chdir(path)
    full_output_csv_name = str(output_csv_filename) + ".csv"
    with open(full_output_csv_name, 'w', newline='') as myfile:
        thewriter = csv.writer(myfile)
        thewriter.writerow(['Wort', 'PoS', 'Satzende?'])

        for text in all_texts:
            doc = nlp(text)
            for sentence in doc.sents:
                #print("Ein Satz beginnt")
                counter = 0
                words_in_sentence = len(sentence)
                for token in sentence:
                    counter += 1
                    if counter != words_in_sentence:
                        thewriter.writerow([token.text, token.pos_])
                    else:
                        thewriter.writerow([token.text, token.pos_, "Satzende"])


def main():
    all_texts = gi.get_input_data()
    new_directory_name = "output_data"
    output_csv_filename = "output_data"

    create_dir_for_saving_data(new_directory_name)
    #write_into_csv_file(new_directory_name, output_csv_filename, all_texts)
    write_into_csv_file(new_directory_name, output_csv_filename,all_texts[0:1])


main()

#for text_passage in input:
    #test_2(text_passage)


#token.text return the text of a token

#TODO #TODO #TODO #TODO #TODO #TODO #TODO #TODO
#Was können wir bisher:
#Wir können den Text von allen .xml Dateien lesen und diese mit mithilfe von Spacy mit PoS Tags versehen.













'''
def create_csv_file(new_directory_name, output_csv_filename):
    cur_abs_path = os.path.abspath("")
    path = os.path.join(cur_abs_path, new_directory_name)
    os.chdir(path)
    full_output_csv_name = str(output_csv_filename)+".csv"
    with open(full_output_csv_name, 'w', newline='') as myfile:
        column_names = ['col1', 'col2', 'col3']
        thewriter = csv.writer(myfile)

        thewriter.writerow(["aaaaaa", "hmm"])


'''