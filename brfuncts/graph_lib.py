__all__ = ["generate_cooc_graph",
           "cooc_graph_html_plot"]

# Standard library import    
import math
from collections import defaultdict
import webbrowser

# 3rd party import
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from more_itertools import distinct_combinations
from pyvis.network import Network

# Local imports
import brfuncts.functs_globals as rg 


def generate_cooc_graph(df_corpus, size_min, item=None):

    """The `generate_cooc_graph` function builds a co-occurrence networkx object `G(N,E)` 
    out of the dataframe `df_corpus` composed of two columns : 
    `pub_id` (article identifier) and `item` (item value).
       
    Example:
        ========= =======
         pub_id    item    
        ========= =======    
             0      item1  
             0      item2       
             1      item1     
             1      item1     
             1      item3      
             1      item3     
             2      item4      
             2      item5   
             2    unknown 
        ========= =======
    
    First, `df_corpus` is cleaned by eliminating duplicated rows or with the item-value equal to UNKNOWN global.
    This results in:
        ========= =======
         pub_id    item    
        ========= =======    
           0      item1  
           0      item2    
           1      item1    
           1      item3          
           2      item4     
           2      item5  
        ========= =======     
    
    The set of nodes `N` is the set of the items `{item1,item2,item3,...}`.
    The set of edges `E` is the set of tuples `{(item_i,item_j),...}` where:   
          1.  `item_i` and `item_j` are related to the same `pub_id`;
          2.  `item_i` and `item_j` are different;
          3.  `(item_i,item_j)` and `(item_j,item_i)` are equivalent.
     
    This means:
          `N = {item1,item2,item3,item4,item5}`
          
          `E={(item1,item2),(item1,item3),(item4,item5)}`.
     
    The size of the node associated with `item_i` is the number of occurrences of `item_i` 
    that should be >= than `size_min`. So we have: 
    
        size of `item1` node is 2
        
        size of `item2` node is 1
     
    The weight `w_ij` of an edge is the number of occurrences of the tuple `(item_i,item_j)` in the
    list of tuples `[(item_i,item_j),...]` where: 
         1.  `item_i` and `item_j` are related to the same `pub_id`;
         2.  `item_i` and `item_j` are different; 
         3.  `(item_i,item_j)` and `(item_j,item_i)` are equivalent.
     
    The nodes have one ID and two attributes: the size of the node and its label. 
    If `item = "CU"`, the longitude and latitude (in degree) of the country capital 
    are added as attributes of the node to be compatible with the Geo Layout of Gephy.
     
    The edges have two attributes: the edge weight `w_ij` and its Kessler similarity `kess_ij`.
    The Kessler similarity of the edge of the nodes `node_i` and node_j` is defined as:                              
    
    .. math:: kess_{ij} = \\frac{w_{ij}}{\\sqrt{size(node\_i) . size(node\_j)}} 
    
    Args:
        df_corpus (dataframe): dataframe structured as `|pub_id|item|`.
        size_min (int): minimum size of the nodes to be kept (default: 1).
        item (str): item label (ex: "AU", "CU") of which co-occurrence graph is generated.

    Returns:
        `networkx object`: co-occurrence graph `G` of the item `item`; 
                          `G=None` if the graph has only one node.
        
    """


    #                           Cleaning of the dataframe
    # -----------------------------------------------------------------------------------------
    df_corpus.drop_duplicates(inplace=True)  # Keeps unique occurrence of an item 
    # per article
    df_corpus.drop(
        index=df_corpus[df_corpus["item"] == rg.UNKNOWN].index, inplace=True
    )  # Drops rows with UNKNOWN items

    dg = (
        df_corpus.groupby("item").count().reset_index()
    )  # Number of occurrences of an item
    dg.columns = ["item", "count"]
    labels_to_drop = dg.query("count<@size_min")[
        "item"
    ].to_list()  # List of items whith a number
    # of occurrences less than size_min
    index_to_drop = [
        x[0] for x in zip(df_corpus.index, df_corpus["item"]) if x[1] in labels_to_drop
    ]
    df_corpus.drop(index_to_drop, inplace=True)  # Cleaning of the dataframe

    #                 Building the set of nodes and the set of edges
    # -----------------------------------------------------------------------------------------
    df_corpus.columns = ["pub_id", "item"]
    nodes_id = list(
        set(df_corpus["item"])
    )  
    # Attribution of an integer id to the different items
    dic_nodes = dict(
        zip(nodes_id, range(len(nodes_id)))
    )  
    # Number of an item occurrence keyed by the
    # node id
    dic_size = dict(zip(dg["item"], dg["count"]))
    nodes_size = {dic_nodes[x]: dic_size[x] for x in nodes_id}

    if len(nodes_size) < 2:  # Dont build a graph with one or zero node
        G = None
        del df_corpus, dic_nodes

    else:
        list_edges = []
        weight = defaultdict(int)
        for pub_id,group_by_pub_id in df_corpus.groupby("pub_id"):
            
            for edges in list(
                distinct_combinations(sorted(group_by_pub_id["item"].to_list()), 2)
            ):
                if edges:
                    edge = (dic_nodes[edges[0]], dic_nodes[edges[1]])
                    if edge not in list_edges:
                        list_edges.append(edge)
                        weight[edge] = 1
                    else:
                        weight[edge] += 1
        del df_corpus
        #                            Building the networx object graph G
        # -------------------------------------------------------------------------------------
        G = nx.Graph()

        G.add_nodes_from(dic_nodes.values())
        nx.set_node_attributes(G, nodes_size, "node_size")
        nodes_label = dict(zip(dic_nodes.values(), dic_nodes.keys()))
        del dic_nodes

        nx.set_node_attributes(G, nodes_label, "label")
        if item == "CU":
            lat, lon = map(
                list, zip(*[rg.COUNTRIES_GPS[nodes_label[node]] for node in G.nodes])
            )
            lat_dict = dict(zip(G.nodes, lat))
            lon_dict = dict(zip(G.nodes, lon))
            nx.set_node_attributes(G, lat_dict, "latitude")
            nx.set_node_attributes(G, lon_dict, "longitude")
            del lat_dict, lon_dict

        G.add_edges_from(list_edges)
        nx.set_edge_attributes(G, weight, "nbr_edges")
        kess = {}
        for edge in list_edges:  # Computes the Kessler similarity betwween node edge[0] and node edge[1]
            kess[edge] = weight[edge] / math.sqrt(
                nodes_size[edge[0]] * nodes_size[edge[1]]
            )
        nx.set_edge_attributes(G, kess, "kessler_similarity")
       
    return G


def cooc_graph_html_plot(G,html_file, html_title, cooc_html_param=None):
    
    """
    Correction of pyviz-network double title by applying :
    https://stackoverflow.com/questions/74890203/pyvis-network-has-double-heading
    """
       
    if cooc_html_param==None:
        cooc_html_param=rg.COOC_HTML_PARAM
        
    algo = cooc_html_param['algo']
    height = cooc_html_param['height']
    width = cooc_html_param['width']
    bgcolor = cooc_html_param['bgcolor']
    font_color = cooc_html_param['algo']
    
    
    
    def map_algs(g,alg='barnes'):
        if alg == 'barnes':
            g.barnes_hut()
        if alg == 'forced':
            g.force_atlas_2based()
        if alg == 'hr':
            g.hrepulsion()
    
    dic_tot_edges ={node:G.degree(node,'nbr_edges') for node in G.nodes}
    nt = Network(height=height,
                 width=width, 
                 bgcolor=bgcolor, 
                 font_color=font_color,
                 notebook=False,
                 heading = html_title)

    # populates the nodes and edges data structures
    nt.from_nx(G)
    dic_node_label = {str(node['id']):f'{str(node["node_size"])}-{node["label"]}'
                       for node in nt.nodes}
    map_algs(nt,alg='barnes')
    
    for edge in nt.edges:
        edge['title'] = edge['nbr_edges']
        edge['value'] = edge['nbr_edges']
    
    for node in nt.nodes:     
        node['title'] = node['label']
        node['size'] = node['node_size']
        node['tot_edges'] = dic_tot_edges[node['id']]
        node['nbr_edges_to'] = {}
        for edge in nt.edges:
            if edge['from'] == node['id']:
                node_to_label = dic_node_label[str(edge['to'])]
                node['nbr_edges_to'][node_to_label] = edge['nbr_edges']
            if edge['to'] == node['id']:
                node_from_label = dic_node_label[str(edge['from'])]
                node['nbr_edges_to'][node_from_label]=edge['nbr_edges']

    neighbor_map = nt.get_adj_list()
                 
    dic_label_neighbors = {}
    for node in nt.nodes:
        node_id = node['id']
        dic_label_neighbors[node_id] = []
        for id_key in sorted(node['nbr_edges_to'].keys(),key=lambda x:int(x.split('-')[0]),reverse=True):
            dic_label_neighbors[node_id].append(f'{id_key}({str(node["nbr_edges_to"][id_key])})') 
    
    dic_label_main = {node['id']: f"{str(node['node_size'])}-{node['label']}({str(node['tot_edges'])},{str(len(dic_label_neighbors[node['id']]))})" 
                                  for node in nt.nodes}
    
    # add neighbor data to node hover data
    for node in nt.nodes:
        idd = node['id']
        text = f'{dic_label_main[idd]}\n\n'
        text = text + '\n'.join([dic_label_neighbors[idd][i] 
                            for i in range(len(dic_label_neighbors[idd]))])
        node['title'] = text
        node["font"]={"size": rg.NODE_FONT_SIZE,"color": rg.NODE_FONT_COLOR}

    nt.show_buttons(filter_=['physics'])
    
    nt.write_html(html_file)
    webbrowser.open(html_file)
                     
def plot_cooc_graph(G, item, size_min=None, node_size_ref=None):

    """The `plot_cooc_graph` function plots the co-occurrence graph G.
       The layout is fixed as "spring_layout".
    
    Args:
        G (networkx ogject): a co-occurrence graph built using 
                             the function `_generate_cooc_graph`.
        item (str): item name (ex: "Authors", "Country"...).
        size_min (int): minimum size of the kept nodes.
        Node_size_ref (int): maximum size of a node.
    
    Note:
        The global `COOC_AUTHORIZED_ITEMS` is used.
    
     
    """
    
    if node_size_ref==None: node_size_ref = rg.NODE_SIZE_REF
    if size_min==None: size_min = rg.SIZE_MIN    

    pos = nx.spring_layout(G)
    node_sizes = np.array(list(nx.get_node_attributes(G, "node_size").values()))
    nodes_sizes_normalized = node_sizes / max(node_sizes)
    node_sizes = (nodes_sizes_normalized * node_size_ref).astype(int)

    title_item_dict = {
        item: full_name for full_name, item in rg.COOC_AUTHORIZED_ITEMS_DICT.items()
    }

    # cmap = cm.get_cmap('viridis', max(partition.values()) + 1) (for future use)
    fig = plt.figure(figsize=(15, 15))
    _ = nx.draw_networkx_nodes(
        G, pos, node_size=node_sizes
    )  # , partition.keys(),(for future use)
    # cmap=cmap, node_color=list(partition.values())) (for future use)
    _ = nx.draw_networkx_edges(
        G, pos, alpha=0.9, width=1.5, edge_color="k", style="solid",
    )
    labels = nx.draw_networkx_labels(G, pos=pos, font_size=8, font_color="w")
    plt.title(
        "Co-occurrence graph for item "
        + title_item_dict[item]
        + "\nNode minimum size: "
        + str(size_min),
        fontsize=23,
        fontweight="bold",
    )

    plt.show()


def _write_cooc_gexf(G, filename):

    """The `_write_cooc_gexf` function saves the graph `G"`
       in Gephy (`.gexf`) format using full path filename.
       
    Args:
        G (networkx ogject): a co-occurrence graph built using 
                             the function `_generate_cooc_graph`.
        filename (Path): full path for saving the Gephy file (`.gexf`).
        
    """

    assert isinstance(G, nx.classes.graph.Graph), "G should be a networkx Graph"

    nx.write_gexf(G, filename)


def _write_cooc_gdf(G, item, color, filename):

    """The `_write_cooc_gdf` function saves the graph `G` 
       in Gephy (`.gdf`) format using full path filename.
       If `item = "CU"`, the longitude and latitude (in degree) of the country capital 
       are added as attributes of the node to be compatible with the Geo Layout of Gephy.
       
    Args:
        G (networkx ogject): a co-occurrence graph built using 
                             the function `_generate_cooc_graph`.
        item (str): label of the item. 
        color (str): color of the nodes in rgb format (ex: "150,0,150").                    
        filename (Path): full path for saving the Gephy file (`.gdf`).
    
    """
    

    assert isinstance(G, nx.classes.graph.Graph), "G should be a networkx Graph"

    with open(filename, "w") as f_gephi:
        nodes_label = nx.get_node_attributes(G, "label")
        nodes_weight = nx.get_node_attributes(G, "node_size")
        label_columns_nodes = (
            "nodedef>name VARCHAR,label VARCHAR,type VARCHAR,width DOUBLE,"
        )
        if item != "CU":
            label_columns_nodes += "height DOUBLE,size DOUBLE,color VARCHAR\n"
        else:  # we add the node attributes lon and lat
            label_columns_nodes += (
                "height DOUBLE,size DOUBLE,color VARCHAR,lat DOUBLE,lon DOUBLE\n"
            )
        f_gephi.write(label_columns_nodes)

        for node in G.nodes:
            size = nodes_weight[node]
            row = f"{node},'{nodes_label[node]}',{item},"
            if item != "CU":
                row += (
                    f"{math.sqrt(size):.5f} ,{math.sqrt(size):.5f},{size},'{color}'\n"
                )
            else:
                lat, lon = bg.COUNTRIES_GPS[nodes_label[node]]
                row += f"{math.sqrt(size):.5f} ,{math.sqrt(size):.5f},{size},'{color}',"
                row += f"{lat},{lon}\n"
            f_gephi.write(row)

        edge_weight = nx.get_edge_attributes(G, "nbr_edges")
        edge_similarity = nx.get_edge_attributes(G, "kessler_similarity")
        f_gephi.write(
            "edgedef>node1 VARCHAR,node2 VARCHAR,weight DOUBLE,nb_cooc DOUBLE\n"
        )
        for edge in G.edges:
            row = f"{edge[0]},{edge[1]},{edge_similarity[edge]:.10f},{edge_weight[edge]}\n"
            f_gephi.write(row)
            
