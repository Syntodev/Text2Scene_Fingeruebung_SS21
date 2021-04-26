import spacy
import get_input as gi
import csv
import os
import pydot
import visualisierung as vi
from xml.etree import ElementTree
from matplotlib import pyplot as plt
from collections import Counter
import copy


def create_picture(name, places, locations, spatial_entities, nonmotionevents, paths):
    name_of_drawing = "Visualisierung für: "+str(name)
    graph = pydot.Dot('my_graph', graph_type='graph', bgcolor='white', label=name_of_drawing)
        # Add nodes
    #cwd = os.getcwd()
    #print(cwd)
    for i in places:
        my_node = pydot.Node(i, label=i, fillcolor = 'blue', style="filled")  #fontcolor = 'red'
        graph.add_node(my_node)
    for j in locations:
        my_node = pydot.Node(j, label=j, fillcolor='green', style="filled")  # fontcolor = 'red'
        graph.add_node(my_node)

    for pos_edge in places:
        for pos_match in locations:
            if pos_edge[0] == pos_match[0]:
                my_edge = pydot.Edge(pos_edge, pos_match, color='red', penwidth=3, label="QLink")
                graph.add_edge(my_edge)
        # Or, without using an intermediate variable:
    graph.add_node(pydot.Node('b', shape='circle'))
    my_edge = pydot.Edge("Pizzeria", "italy", color='red', penwidth=3, label="QLink")
    graph.add_edge(my_edge)
        # Add edges
    my_edge = pydot.Edge('a', 'b', color='blue', penwidth=3)
    graph.add_edge(my_edge)
        # Or, without using an intermediate variable:
    graph.add_edge(pydot.Edge('b', 'c', color='blue'))



    output_graphviz_svg = graph.create_svg()
    name_of_finished_drawing_file_png = name_of_drawing+".png"
    graph.write_png(name_of_finished_drawing_file_png)

def extract_required_information_for_visualization(xml_file):
    graph = pydot.Dot('my_graph', graph_type='graph', bgcolor='white', label="test_drawing")
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    test = []
    counter = 0

    #Here we gather the IDs for the Metalinked Tags
    metalinked_ids = []
    for elem in root:
        if elem.tag == 'TAGS':
            for sub_tag in elem:
                if sub_tag.tag == "METALINK":
                    if sub_tag.attrib['fromID'] == '' or sub_tag.attrib['toID'] == '':
                        continue
                    else:
                        id_connection = [sub_tag.attrib['fromID'], sub_tag.attrib['toID']]
                        metalinked_ids.append(id_connection)
    print("große Liste:",metalinked_ids)
    connected_nodes_metalinks_list = []
    for edge in metalinked_ids:
        hit_left_node = 0
        hit_right_node = 0
        for connected_node in connected_nodes_metalinks_list:
            if edge[0] in connected_node and edge[1] in connected_node: #Diese Verbindung ist bereits bekannt.
                break
        for connected_node in connected_nodes_metalinks_list:
            if edge[0] in connected_node:   #Der linke Knoten ist bekannt
                hit_left_node = 1
        for connected_node in connected_nodes_metalinks_list:
            if edge[1] in connected_node:   #Der Rechte knoten ist bekannt
                hit_right_node = 1
        if hit_left_node and hit_right_node:    #2 Gruppen mergen
            for connected_node in connected_nodes_metalinks_list:
                if edge[0] in connected_node:
                    copy_vertex_comp_0 = copy.deepcopy((connected_node))
                if edge[1] in connected_node:
                    copy_vertex_comp_1 = copy.deepcopy((connected_node))
            connected_nodes_metalinks_list.remove(copy_vertex_comp_0)
            connected_nodes_metalinks_list.remove(copy_vertex_comp_1)
            merged_list = copy_vertex_comp_0 + copy_vertex_comp_1
            connected_nodes_metalinks_list.append(merged_list)
        elif hit_left_node:
            for connected_node in connected_nodes_metalinks_list:
                if edge[0] in connected_node:
                    connected_node.append(edge[1])
        elif hit_right_node:
            for connected_node in connected_nodes_metalinks_list:
                if edge[1] in connected_node:
                    connected_node.append(edge[0])
        else:
            connected_nodes_metalinks_list.append(edge)
    #Now we got the IDs of the Tags that are getting merged by Metalinks
    #The IDs are in the list: connected_nodes_metalinks_list


    for elem in root:
        if elem.tag == 'TAGS':
            for sub_tag in elem:
                if sub_tag.tag == "PLACE":
                    if sub_tag.attrib['text'] == '':
                        continue
                    #my_node = pydot.Node(sub_tag.attrib['id'], label=sub_tag.attrib['text'], fillcolor='blue', style="filled")
                    my_node = pydot.Node(sub_tag.attrib['text'], label=sub_tag.attrib['text'], fillcolor='blue', style="filled")
                    graph.add_node(my_node)
                elif sub_tag.tag == "LOCATION": #place + path??
                    pass
                elif sub_tag.tag == "SPATIAL_ENTITY":
                    if sub_tag.attrib['text'] == '':
                        continue
                    my_node = pydot.Node(sub_tag.attrib['text'], label=sub_tag.attrib['text'], fillcolor='red',
                                         style="filled")  # fontcolor = 'red'
                    graph.add_node(my_node)
                elif sub_tag.tag == "NONMOTION_EVENT":
                    if sub_tag.attrib['text'] == '':
                        continue
                    my_node = pydot.Node(sub_tag.attrib['text'], label=sub_tag.attrib['text'], fillcolor='orange',
                                         style="filled")  # fontcolor = 'red'
                    graph.add_node(my_node)
                elif sub_tag.tag == "PATH":
                    if sub_tag.attrib['text'] == '':
                        continue
                    counter += 1
                    if sub_tag.attrib['text'] != "edge":    #Das Visualisierungsprogramm gibt einen Error, wenn ein Knoten "edge" heißt,
                                                            #deswegen benenne wir den Knoten um in "edge'"
                        my_node = pydot.Node(sub_tag.attrib['text'], label=sub_tag.attrib['text'], fillcolor='green',
                                             style="filled")  # fontcolor = 'red'
                        graph.add_node(my_node)
                    else:
                        my_node = pydot.Node("edge'", label="edge'", fillcolor='green',
                                             style="filled")  # fontcolor = 'red'
                        graph.add_node(my_node)

            for sub_tag in elem:
                if sub_tag.tag == "QSLINK":
                    if sub_tag.attrib['fromText'] == '' or sub_tag.attrib['toText'] == '':
                        continue
                    if sub_tag.attrib['fromText'] == 'edge' and sub_tag.attrib['toText'] == 'edge':
                        my_edge = pydot.Edge("edge'", "edge'", color='red',
                                             penwidth=3, label=sub_tag.attrib['relType'])
                        continue
                    if sub_tag.attrib['fromText'] == 'edge':
                        my_edge = pydot.Edge("edge'", sub_tag.attrib['toText'], color='red',
                                             penwidth=3, label=sub_tag.attrib['relType'])
                        continue
                    if sub_tag.attrib['toText'] == 'edge':
                        my_edge = pydot.Edge(sub_tag.attrib['fromText'], "edge'", color='red',
                                             penwidth=3, label=sub_tag.attrib['relType'])
                        continue
                    #my_edge = pydot.Edge(sub_tag.attrib['fromID'], sub_tag.attrib['toID'], color='red', penwidth=3, label=sub_tag.attrib['relType'])
                    my_edge = pydot.Edge(sub_tag.attrib['fromText'], sub_tag.attrib['toText'], color='red', penwidth=3, label=sub_tag.attrib['relType'])
                    graph.add_edge(my_edge)
                elif sub_tag.tag == "OLINK":
                    if sub_tag.attrib['fromText'] == '' or sub_tag.attrib['toText'] == '':
                        continue
                    if sub_tag.attrib['fromText'] == 'edge' and sub_tag.attrib['toText'] == 'edge':
                        my_edge = pydot.Edge("edge'", "edge'", color='blue',
                                             penwidth=3, label=sub_tag.attrib['relType'])
                        continue
                    if sub_tag.attrib['fromText'] == 'edge':
                        my_edge = pydot.Edge("edge'", sub_tag.attrib['toText'], color='blue',
                                             penwidth=3, label=sub_tag.attrib['relType'])
                        continue
                    if sub_tag.attrib['toText'] == 'edge':
                        my_edge = pydot.Edge(sub_tag.attrib['fromText'], "edge'", color='blue',
                                             penwidth=3, label=sub_tag.attrib['relType'])
                        continue
                    #my_edge = pydot.Edge(sub_tag.attrib['fromID'], sub_tag.attrib['toID'], color='blue', penwidth=3, label=sub_tag.attrib['relType'])
                    my_edge = pydot.Edge(sub_tag.attrib['fromText'], sub_tag.attrib['toText'], color='blue', penwidth=3, label=sub_tag.attrib['relType'])
                    graph.add_edge(my_edge)
                elif sub_tag.tag == "METALINK":
                    pass
    graph.write_png("testdrawing.png")
    places_locations_spatial_entities_nonmotionevents_paths = []
    return places_locations_spatial_entities_nonmotionevents_paths

def visualisierung_fuer_nummber_vier(abs_paths_to_xml_files):
    files_to_visualize = []
    for file in abs_paths_to_xml_files:
        if file[-12:] == "Bicycles.xml" or file[-34:] == "Highlights_of_the_Prado_Museum.xml":
            files_to_visualize.append(file)
    for file in files_to_visualize:
        if file[-12:] == "Bicycles.xml":
            name = "Bicycles.xml"
            continue
        else:
            name = "Highlights_of_the_Prado_Museum.xml"
        visualize_this = extract_required_information_for_visualization(file)
        Place = ["Pizzeria","Wash Saloon"]
        Location = ["italy", "Spain"]
        spatial_entity = ["ok"]
        nonmotionevent = ["sitting"]
        path = ["over there"]
        create_picture(name, Place, Location, spatial_entity, nonmotionevent, path)
