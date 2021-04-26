import pydot
from xml.etree import ElementTree
import copy

def create_picture(xml_file, name):
    graph = pydot.Dot('my_graph', graph_type='graph', bgcolor='white', label=name)
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()

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
    list_of_multilinked_ids = []
    for list in connected_nodes_metalinks_list:
        list_of_multilinked_ids = list_of_multilinked_ids + list


    nodes_in_graph_dict = dict()
    #merge_nodes weil die mit Metalinks  versehen wurden
    for connected_nodes in connected_nodes_metalinks_list:
        for i in range(len(connected_nodes)):
            if i == 1:  #we start at 1 to get a label with text
                continue
            nodes_in_graph_dict[connected_nodes[i]] = connected_nodes[1]

    nodes_in_graph_dict_copy = copy.deepcopy(nodes_in_graph_dict)

    call_nodes = 'id'
    for elem in root:
        if elem.tag == 'TAGS':
            for sub_tag in elem:
                if not(sub_tag.tag in ["PLACE", "SPATIAL_ENTITY", "NONMOTION_EVENT", "PATH"]):
                    continue
                if sub_tag.attrib['id'] in nodes_in_graph_dict:
                    pass
                else:
                    fill_col = "pink"
                    if sub_tag.tag == "PLACE":
                        my_node = pydot.Node(sub_tag.attrib[call_nodes], label=sub_tag.attrib['text'], fillcolor='blue', style="filled")
                    elif sub_tag.tag == "SPATIAL_ENTITY":
                        my_node = pydot.Node(sub_tag.attrib[call_nodes], label=sub_tag.attrib['text'], fillcolor='red',
                                             style="filled")
                    elif sub_tag.tag == "NONMOTION_EVENT":
                        my_node = pydot.Node(sub_tag.attrib[call_nodes], label=sub_tag.attrib['text'], fillcolor='orange',
                                             style="filled")
                    elif sub_tag.tag == "PATH":
                        if sub_tag.attrib['text'] != "edge":    # Das Visualisierungsprogramm gibt einen Error, wenn ein Knoten "edge" heißt,
                                                                # deswegen benenne wir den Knoten um in "edge'"
                            my_node = pydot.Node(sub_tag.attrib[call_nodes], label=sub_tag.attrib['text'],
                                                 fillcolor='green',
                                                 style="filled")  # fontcolor = 'red'
                            graph.add_node(my_node)
                        else:
                            my_node = pydot.Node(sub_tag.attrib[call_nodes], label="edge'", fillcolor='green',
                                                 style="filled")
                    else:
                        my_node = pydot.Node("what", label="what", fillcolor=fill_col,
                                             style="filled")
                    nodes_in_graph_dict[sub_tag.attrib['id']] = "sth"
                    graph.add_node(my_node)

            for sub_tag in elem:
                if sub_tag.tag == "QSLINK":
                    if name == "Bicycles_visualisierung.png":
                        if sub_tag.attrib['fromID'] == "m5" or \
                                sub_tag.attrib['fromID'] == "m7" or \
                                sub_tag.attrib['fromID'] == "m8" or \
                                sub_tag.attrib['fromID'] == "m43" or \
                                sub_tag.attrib['fromID'] == "m2":
                            continue
                    from_id = sub_tag.attrib['fromID']
                    to_id = sub_tag.attrib['toID']
                    if sub_tag.attrib['fromID'] in nodes_in_graph_dict_copy:
                        from_id = nodes_in_graph_dict_copy[sub_tag.attrib['fromID']]
                    if sub_tag.attrib['toID'] in nodes_in_graph_dict_copy:
                        to_id = nodes_in_graph_dict_copy[sub_tag.attrib['toID']]
                    my_edge = pydot.Edge(from_id, to_id, color='red', penwidth=3, label=sub_tag.attrib['relType'])
                    graph.add_edge(my_edge)
                    continue
                elif sub_tag.tag == "OLINK":
                    from_id = sub_tag.attrib['fromID']
                    to_id = sub_tag.attrib['toID']
                    if sub_tag.attrib['fromID'] in nodes_in_graph_dict_copy:
                        from_id = nodes_in_graph_dict_copy[sub_tag.attrib['fromID']]
                    if sub_tag.attrib['toID'] in nodes_in_graph_dict_copy:
                        to_id = nodes_in_graph_dict_copy[sub_tag.attrib['toID']]
                    my_edge = pydot.Edge(from_id, to_id, color='blue', penwidth=3, label=sub_tag.attrib['relType'])
                    graph.add_edge(my_edge)
                    continue


    final_name = name
    graph.write_png(final_name)
    return

def visualisierung_fuer_nummber_vier(abs_paths_to_xml_files):
    files_to_visualize = []
    for file in abs_paths_to_xml_files:
        if file[-12:] == "Bicycles.xml" or file[-34:] == "Highlights_of_the_Prado_Museum.xml":
            files_to_visualize.append(file)
    for file in files_to_visualize:
        if file[-12:] == "Bicycles.xml":
            name = "Bicycles_visualisierung.png"

        else:
            name = "Highlights_of_the_Prado_Museum_visualisierung.png"
            #continue
        create_picture(file, name)


