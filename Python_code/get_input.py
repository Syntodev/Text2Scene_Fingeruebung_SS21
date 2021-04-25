#This file gets you the input for further processing.
#If you want to change the input or something this is the correct place to change that.

"""
For file-reading we need:
Folder Path
File Name
Extension
"""
import os
from xml.etree import ElementTree


#print(type(cur_abs_path))

def get_text_from_xml(abs_paths_to_xml_data):
    all_text = []

    for xml_document in abs_paths_to_xml_data:
        dom = ElementTree.parse(xml_document)
        current_text = dom.findall('TEXT')
        all_text.append(current_text[0].text)

    return all_text

def get_tags_from_xml(abs_paths_to_xml_data):

    sub_tag_tags = set("")
    read_all = 1
    print(abs_paths_to_xml_data)
    for xml_file in abs_paths_to_xml_data:
        tree = ElementTree.parse(xml_file)
        root = tree.getroot()
        for elem in root:
            if elem.tag == 'TAGS':
                for sub_tag in elem:
                    #print(sub_tag.tag)
                    sub_tag_tags.add(sub_tag.tag)
                #print(elem.tag)
            #for subelem in elem:
                #print("HERE IT COMES")
                #print(subelem,":")
                #print(subelem.attrib)
        if read_all == 0:
            break
    print(sub_tag_tags)
    '''

    all_tags = []

    for xml_document in abs_paths_to_xml_data:
        dom = ElementTree.parse(xml_document)
        current_text = dom.findall('PLACE')
        all_tags.append(current_text[0].text)
    '''
    all_tags = []
    return all_tags

def get_abs_path_to_xml_files():
    cur_abs_path = os.path.abspath("")
    abs_path_to_xml_files = []
    for (root, dirs, files) in os.walk(cur_abs_path+"/training/Traning", topdown=True):
        for name in files:
            if os.path.abspath(os.path.join(root, name))[-4:] == ".xml":
                abs_path_to_xml_files.append(os.path.abspath(os.path.join(root, name)))

    #print(abs_path_to_xml_files)
    return abs_path_to_xml_files

def get_input_data():
    abs_paths_to_xml_files = get_abs_path_to_xml_files()
    all_text_in_lists = get_text_from_xml(abs_paths_to_xml_files)
    all_tags_in_lists = get_tags_from_xml(abs_paths_to_xml_files)
    return all_text_in_lists

#print(get_input_data())
if __name__ == '__main__':
    get_input_data()
#ret = get_input_data()
#for line in ret:
    #print(line)