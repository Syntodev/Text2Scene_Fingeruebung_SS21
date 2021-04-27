import spacy
import get_input as gi
import csv
import os
import visualisierung as vi
from xml.etree import ElementTree
from matplotlib import pyplot as plt
from collections import Counter
spacy.cli.download("en_core_web_sm")
#Die obige Zeile downloaded "en_core_web_sm", nachdem man das gedownloaded hat, kann man es auskommentieren

nlp = spacy.load("en_core_web_sm")

def create_dir_for_saving_data(new_directory_name):
    #Wir erstellen einen Ordner und geben dem User an, dass dieser erstellt wird
    show_warnings = 1
    show_info = 1
    cur_abs_path = os.path.abspath("")
    path = os.path.join(cur_abs_path, new_directory_name)
    if show_info == 1:
        print("Wir versuchen den Ordner '"+str(new_directory_name)+"' zu erstellen um dort den Output von diesem Programm zu speichern")
    try:
        os.mkdir(path)
        print("Wir haben einen neuen Order mit dem Pfad:",path,"erstellt.")
    except FileExistsError:
        if show_warnings == 1:
            print("Der Ordner '"+str(new_directory_name)+"' existiert bereits, wir werden ihn nicht erneut erstellen.")
            print("Wir fahren wie geplant fort.")
    except:
        print("Ein unvorhergesehener Fehler ist aufgetreten.")
        print("GGF. stimmt etwas mit dem Pfad für die Ordnererstellung nicht.")


def write_into_csv_file(new_directory_name, output_csv_filename, all_texts, output_count_pos_tags):
    #Wir versehen jedes Wort in jeder der .xml Dateien mit dem von Spacy erkannten Part-of-Speech Tag
    #Die Satzenden finden wir mit "doc.sents" und geben wir an den entsprechenden Stellen in der .csv Datei an
    #Wir zählen parallel die Häufigkeit der verschiedenen PoS Tags und schreiben diese in ein anderes File.
    #Wir zählen hier auch die Satzlängen
    cur_abs_path = os.path.abspath("")
    path = os.path.join(cur_abs_path, new_directory_name)
    os.chdir(path)
    full_output_csv_name = str(output_csv_filename) + ".csv"
    with open(full_output_csv_name, 'w', newline='') as myfile:
        thewriter = csv.writer(myfile)
        thewriter.writerow(['Wort:', 'PoS:', 'Satzende:'])

        counter_for_pos = dict()
        count_length_of_different_sentences = dict()
        for text in all_texts:
            thewriter.writerow(["Begin New File"])
            doc = nlp(text)
            for sentence in doc.sents:
                #print("Ein Satz beginnt")
                counter = 0
                tokens_in_sentence = len(sentence)
                words_in_sentence = 0
                for token in sentence:
                    if token.pos_ != "PUNCT":   #Count amount of 'real' words in a sentence
                        words_in_sentence += 1
                    if token.pos_ in counter_for_pos:
                        counter_for_pos[token.pos_] += 1
                    else:
                        counter_for_pos[token.pos_] = 1
                    counter += 1
                    if counter != tokens_in_sentence:
                        thewriter.writerow([token.text, token.pos_])
                    else:
                        thewriter.writerow([token.text, token.pos_, "Satzende"])
                if words_in_sentence in count_length_of_different_sentences:
                    count_length_of_different_sentences[words_in_sentence] += 1
                else:
                    count_length_of_different_sentences[words_in_sentence] = 1

    #Hier schreiben wir die Häufigkeit der PoS Tags in eine extra Datei.
    output_count_pos_tags_csv = str(output_count_pos_tags) + ".csv"
    with open(output_count_pos_tags_csv, 'w', newline='') as myfile:
        thewriter = csv.writer(myfile)
        thewriter.writerow(['Part-of-Speech', 'Anzahl'])
        for pos_part in counter_for_pos:
            thewriter.writerow([pos_part, counter_for_pos.get(pos_part)])
    return count_length_of_different_sentences


def count_locations(all_texts):
    #Diese Funktion zählt die Häufigkeiten von der Entität Locations
    ent_dict = dict()
    for text in all_texts:
        doc = nlp(text)
        for token in doc:
            if token.ent_type_ != "":
                if token.ent_type_ in ent_dict:
                    ent_dict[token.ent_type_] += 1
                else:
                    ent_dict[token.ent_type_] = 1
    locations_amount = ["LOC", ent_dict.get("LOC")]
    return locations_amount

def get_tags_from_xml(abs_paths_to_xml_data):
    #Diese Funktion erfüllt vieles für die 2.3
    #Hier zählen wir die Häufigkeit der verschiedenen QsLink Typen
    #Wir sammeln außerdem die Präpositionen, welche durch SPATIAL_SIGNAl angegeben werden
    #Wir werten aus, welche Links durch welche Präpositionen getriggert werden und wie oft das passiert
    #Und wir zählen hier die Anzahl der verschiedenen MOTION verben um die 5 häufigsten zu finden
    read_all = 1
    sub_tag_dict = dict()
    sub_tag_QS_link_types = dict()
    praeposition_triggers_for_qs_links = dict()
    praeposition_triggers_for_os_links = dict()
    count_motion_verb = dict()
    for xml_file in abs_paths_to_xml_data:
        tree = ElementTree.parse(xml_file)
        root = tree.getroot()
        list_with_qs_and_o_link_trigger_ids = []
        list_of_spatial_signal_ids_and_words = []
        for elem in root:
            if elem.tag == 'TAGS':
                for sub_tag in elem:
                    if sub_tag.tag in sub_tag_dict: #Counts all the different Types of Tags
                        sub_tag_dict[sub_tag.tag] += 1
                    else:
                        sub_tag_dict[sub_tag.tag] = 1
                    if sub_tag.tag == "QSLINK": #Counts all the different relTypes of QSLinks
                        #val = sub_tag.attrib['relType']
                        if sub_tag.attrib['relType'] in sub_tag_QS_link_types:
                            sub_tag_QS_link_types[sub_tag.attrib['relType']] += 1
                        else:
                            sub_tag_QS_link_types[sub_tag.attrib['relType']] = 1
                    if sub_tag.tag == "MOTION": #Counts all the different words for motion
                        if sub_tag.attrib['text'] in count_motion_verb:
                            count_motion_verb[sub_tag.attrib['text']] += 1
                        else:
                            count_motion_verb[sub_tag.attrib['text']] = 1

                    if sub_tag.tag == "QSLINK" or sub_tag.tag == "OLINK":   #Here we start to collect the IDS
                        type_of_link = sub_tag.tag                          #for QS and OSlink matches
                        trigger_id = sub_tag.attrib["trigger"]              #to find the trigger-praepositions
                        list_with_qs_and_o_link_trigger_ids.append([type_of_link, trigger_id])
                    if sub_tag.tag == "SPATIAL_SIGNAL":
                        trigger_id = sub_tag.attrib["id"]
                        word_trigger = sub_tag.attrib["text"]
                        list_of_spatial_signal_ids_and_words.append([trigger_id, word_trigger])
        for potential_match in list_of_spatial_signal_ids_and_words:
            for potential_signal_link in list_with_qs_and_o_link_trigger_ids:
                if potential_match[0] == potential_signal_link[1]:
                    if potential_signal_link[0] == "QSLINK":
                        if potential_match[1] in praeposition_triggers_for_qs_links:
                            praeposition_triggers_for_qs_links[potential_match[1]] += 1
                        else:
                            praeposition_triggers_for_qs_links[potential_match[1]] = 1
                    else: #=OSLINK
                        if potential_match[1] in praeposition_triggers_for_os_links:
                            praeposition_triggers_for_os_links[potential_match[1]] += 1
                        else:
                            praeposition_triggers_for_os_links[potential_match[1]] = 1

        double_list_with_qs_and_os_counted_trigger_lists = [praeposition_triggers_for_qs_links, praeposition_triggers_for_os_links]
        if read_all == 0:
            break
    return_list = [sub_tag_dict, sub_tag_QS_link_types, double_list_with_qs_and_os_counted_trigger_lists, count_motion_verb]
    return return_list


def write_counted_tags_and_loc_into_csv(tags_in_dict_counted, get_location_amount):
    #Hier schreiben wir die in anderen Funktionen gezählten Tags und Locations in eine .csv-Datei
    csv_name_for_counted_tags = "output_counted_tags_and_loc.csv"
    with open(csv_name_for_counted_tags, 'w', newline='') as myfile:
        thewriter = csv.writer(myfile)
        thewriter.writerow(['Name:', 'Anzahl:'])
        for entry in tags_in_dict_counted:
            if entry in ["SPATIAL_ENTITY", "PLACE", "MOTION", "SPATIAL_SIGNAL", "MOTION_SIGNAL","QSLINK", "OLINK"]:
                thewriter.writerow([entry, tags_in_dict_counted.get(entry)])
        thewriter.writerow(['Locations', get_location_amount[1]])
        signal_number = tags_in_dict_counted['SPATIAL_SIGNAL'] + tags_in_dict_counted['MOTION_SIGNAL']
        thewriter.writerow(['Signals', signal_number])


def write_counted_qslink_types_into_csv(dict_with_qs_link_types):
    # Hier schreiben wir die in anderen Funktionen gezählten QsLink Typen in eine .csv-Datei
    csv_name_for_qs_link_types = "output_counted_qslink_types.csv"
    with open(csv_name_for_qs_link_types, 'w', newline='') as myfile:
        thewriter = csv.writer(myfile)
        thewriter.writerow(['Name:', 'Anzahl:'])
        for entry in dict_with_qs_link_types:
            if entry == "":
                thewriter.writerow(["No Type specified", dict_with_qs_link_types.get(entry)])
            else:
                thewriter.writerow([entry, dict_with_qs_link_types.get(entry)])


def write_counted_qslink_and_oslink_praep_word_triggers_into_csv(list_with_dicts_for_qs_and_os_link_triggers):
    # Hier schreiben wir die in anderen Funktionen gezählten QsLink und OsLink Trigger in eine .csv-Datei
    csv_name = "output_counted_qs_and_os_link_praep_triggers.csv"
    with open(csv_name, 'w', newline='') as myfile:
        thewriter = csv.writer(myfile)
        thewriter.writerow(['Linktyp:', 'QsLink'])
        thewriter.writerow(['Triggerwort:', 'Anzahl der Triggerungen:'])
        for entry in list_with_dicts_for_qs_and_os_link_triggers[0]:
            thewriter.writerow([entry, list_with_dicts_for_qs_and_os_link_triggers[0].get(entry)])
        thewriter.writerow([''])
        thewriter.writerow(['Linktyp:', 'OsLink'])
        thewriter.writerow(['Triggerwort:', 'Anzahl der Triggerungen:'])
        for entry in list_with_dicts_for_qs_and_os_link_triggers[1]:
            thewriter.writerow([entry, list_with_dicts_for_qs_and_os_link_triggers[1].get(entry)])


def write_counted_motion_verb_into_csv(dict_with_motion_text):
    # Hier schreiben wir die in anderen Funktionen gezählten Motion Verben in eine .csv-Datei
    csv_name = "output_counted_motion_verbs.csv"
    with open(csv_name, 'w', newline='') as myfile:
        thewriter = csv.writer(myfile)
        thewriter.writerow(['Name:', 'Anzahl:'])
        for entry in dict(Counter(dict_with_motion_text).most_common(5)):
            thewriter.writerow([entry, dict_with_motion_text.get(entry)])


def create_graph_for_sentence_lengths(dict_with_sentence_lengths):
    #Hier stellen wir die Verteilung Satzlänge graphisch dar und speichern das Bild
    x = []
    y = []
    for entry in dict_with_sentence_lengths:
        x.append(entry)
        y.append(dict_with_sentence_lengths.get(entry))
    plt.bar(x, y, align='center')

    plt.title("Anzahl der Wörter pro Satz")
    plt.xlabel("Satzlänge")
    plt.ylabel("Häufigkeit")
    plt.savefig('Verteilung_der_satzlaenge.png', dpi=300, bbox_inches='tight')
    #plt.show()


def do_part_2_2_vorverarbeitung(all_texts):
    #Eine kleine Sub-funktione, welche den Output-Ordner erstellt und
    #dafür sorgt, dass das die PoS-Tags gezählt und geschrieben werden und dabei
    #zählen wir die Satzlängen und geben diese in einem dict zurück
    create_dir_for_saving_data("output_data")
    dict_with_sentence_lengths = write_into_csv_file("output_data", "output_text_with_pos", all_texts, "output_count_pos_tags")
    return dict_with_sentence_lengths


def main():
    input_data = gi.get_input_data()
    all_texts = input_data[0]
    dict_with_sentence_lengths = do_part_2_2_vorverarbeitung(all_texts)
    abs_paths_to_xml_files = input_data[1]

    #count the different tags for 2.3.b)
    get_location_amount = count_locations(all_texts)
    xml_tags = get_tags_from_xml(abs_paths_to_xml_files)
    write_counted_tags_and_loc_into_csv(xml_tags[0], get_location_amount)
    write_counted_qslink_types_into_csv(xml_tags[1])
    write_counted_qslink_and_oslink_praep_word_triggers_into_csv(xml_tags[2])
    write_counted_motion_verb_into_csv(xml_tags[3])
    create_graph_for_sentence_lengths(dict_with_sentence_lengths)

    vi.visualisierung_fuer_nummer_vier(abs_paths_to_xml_files)
    print("Alles hat erfolgreich geklappt!")
    print("Der Output ist in dem Ordner: 'output_data' in entsprechenden Bildern und .csv-Dateien")


if __name__ == '__main__':
    main()