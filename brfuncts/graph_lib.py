__all__ = ["add_title_to_node",
          "generate_cooc_graph",
          "cooc_graph_html_plot",
          "create_star_graph",
          "plot_graph_countries",
          "plot_graph_departement",
          "get_filename_listeconsolideepubli",
          "get_filename_listeconsolideebook",
          "get_departements_list",]

# Standard library import    
import math
from collections import defaultdict
from pathlib import Path
import webbrowser

# 3rd party import
import jinja2
import json
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

    # Dataframe cleaning
    df_corpus.drop_duplicates(inplace=True)  # Keeps unique occurrence of an item per article
    df_corpus.drop(
        index=df_corpus[df_corpus["item"] == rg.UNKNOWN].index, inplace=True
    )  # Drops rows with UNKNOWN items

    dg = (
        df_corpus.groupby("item").count().reset_index()
    )  # Number of occurrences of an item
    dg.columns = ["item", "count"]
    labels_to_drop = dg.query("count<@size_min")[
        "item"
    ].to_list()  # List of items whith a number of occurrences less than size_min
    index_to_drop = [
        x[0] for x in zip(df_corpus.index, df_corpus["item"]) if x[1] in labels_to_drop
    ]
    df_corpus.drop(index_to_drop, inplace=True)  # Cleaning of the dataframe

    # Building the set of nodes and the set of edges
    df_corpus.columns = ["pub_id", "item"]
    nodes_id = list(set(df_corpus["item"]))
    
    # Attribution of an integer id to the different items
    dic_nodes = dict(zip(nodes_id, range(len(nodes_id)))) 
    
    # Number of an item occurrence keyed by the node id
    dic_size = dict(zip(dg["item"], dg["count"]))
    nodes_size = {dic_nodes[x]: dic_size[x] for x in nodes_id}

    if len(nodes_size) < 2:  # Dont build a graph with one or zero node
        G = None

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
                        
        # Building the networx object graph G
        G = nx.Graph()

        G.add_nodes_from(dic_nodes.values())
        nx.set_node_attributes(G, nodes_size, "node_size")
                
        nodes_label = dict(zip(dic_nodes.values(), dic_nodes.keys()))
        nx.set_node_attributes(G, nodes_label, "label")  

        G.add_edges_from(list_edges)
        nx.set_edge_attributes(G, weight, "nbr_edges")
        kess = {}
        for edge in list_edges:  # Computes the Kessler similarity betwween node edge[0] and node edge[1]
            kess[edge] = weight[edge] / math.sqrt(
                nodes_size[edge[0]] * nodes_size[edge[1]]
            )
        nx.set_edge_attributes(G, kess, "kessler_similarity")
        nx.set_node_attributes(G, dict(G.degree),"degree")
        
    return G

def add_long_lat_to_node(G):
    
    """
    The function add_long_lat_to_node adds two attributes to the nodes : the latitude of the country capital and the
    longitude of the country capital.
    """
    
    lat, lon = map(
                list, zip(*[rg.COUNTRIES_GPS[G.nodes[node]['label']] for node in G.nodes])
            )
    lat_dict = dict(zip(G.nodes, lat))
    lon_dict = dict(zip(G.nodes, lon))
    nx.set_node_attributes(G, lat_dict, "latitude")
    nx.set_node_attributes(G, lon_dict, "longitude")
    
    return G

def add_total_edges_to_node(G):
    
    """
    The function `add_total_edges_to_node`adds the node attribute "tot_edges" to total number
    of edges connected to the node (not to be cofused with the node degree).
    """
    
    dic_tot_edges = {node:G.degree(node,'nbr_edges') for node in G.nodes}
    nx.set_node_attributes(G, dic_tot_edges, 'tot_edges')
    
    return G    
    
def add_title_to_node(G, txt):
    
    """
    add hover data attribute to node. These hover data are formatted as html text.
    There consist in : (i) a heading <h4> containing the attribute of the node and a ordered list
    containing the number of articles co-authored with other countries.
    
    """
    
    from_to_dict = defaultdict(list)
    to_from_dict = defaultdict(list)
    
    labels_idx_dict = {G.nodes[node]['label']:node  for node in G.nodes}
    
    # Builds dicts {node_label: list of tuple (u,v)} where u or v is the node_label
    for u,v in G.edges:
        from_to_dict[G.nodes[u]['label']].append((G.nodes[v]['label'],G[u][v]['nbr_edges']))
        to_from_dict[G.nodes[v]['label']].append((G.nodes[u]['label'],G[u][v]['nbr_edges']))
    
    # dict concatenation of from_to_dict and to_from_dict
    tot_edges_dict = {key: from_to_dict.get(key, []) + to_from_dict.get(key, []) 
              for key in (from_to_dict.keys() | to_from_dict.keys())}
    
    tot_edges_dict = {k: sorted(v,key=lambda x: x[1],reverse=True) for k,v in tot_edges_dict.items()}
    tot_edges_dict = {k:[f'{x[0]} : {str(x[1])} articles' for x in v] for k,v in tot_edges_dict.items()}
    
    text_dict = {}
    env = jinja2.Environment()
    for node_label,label_list in tot_edges_dict.items():
        idx_node = labels_idx_dict[node_label]
        context = dict(node_label=node_label,
                      node_size=G.nodes[idx_node]['node_size'],
                      node_degree=G.nodes[idx_node]['degree'],
                      label_list=label_list)     
        
        template = env.from_string(("<h5><font color=green>"
                                       "{{node_label}} : {{node_size}} articles. "
                                       "Number of collaborative {{txt}} : {{node_degree}}"
                                  "</font color></h5>"
                                  "<ol>"
                                        "{% for item in label_list %}"
                                            "<li> {{item}} </li>"
                                        "{% endfor %}"
                                  "</ol>"))
        text_dict[idx_node] = template.render(context)
    
    nx.set_node_attributes(G, text_dict,"title")

    return G

def create_star_graph(G,central_node_label):
    
    '''
    create_star_graph create a subgraph of G by retaining only the central node which label is `central_node_label` 
    and all its edges
    '''
    # removing of edges not connected to the central node 
    nodes_labels_dict = {G.nodes[node]['label']:node  for node in G.nodes}
    idx = nodes_labels_dict[central_node_label]
    edge_to_remove_list = [x for x in G.edges if idx not in x]
    G.remove_edges_from(edge_to_remove_list)
    
    # removing of isolated nodes by retaining the higher connected graph which is unique
    nodes = max(nx.connected_components(G), key=len)
    G = nx.subgraph(G, nodes)

    return G

def cooc_graph_html_plot(G,html_file, html_title, cooc_html_param=None, size="size"):
    
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
    
    nt = Network(height=height,
                 width=width, 
                 bgcolor=bgcolor, 
                 font_color=font_color,
                 notebook=False,
                 heading = html_title)

    # populates the nodes and edges data structures
    nt.from_nx(G)
    
    map_algs(nt,alg='barnes')
    
    for edge in nt.edges:
        edge['title'] = edge['nbr_edges']
        edge['value'] = edge['nbr_edges']
    
    for node in nt.nodes:
        if size == "size":        
            node['size'] = node['node_size']
        elif size == "degree":
            node['size'] = node['degree']*10           
        node["font"]={"size": rg.NODE_FONT_SIZE,"color": rg.NODE_FONT_COLOR}

    #nt.show_buttons(filter_=['physics'])
    
    nt.write_html(html_file)
    webbrowser.open(html_file)
    
    return nt
    
def plot_graph_countries(bm_path,institute,year,datatype,central_node_label):
    
    """
    Function `plot_graph_countries` builds and plots a star graph with central node of label `central_node_label` 
    of the articles co-authored by the `central_node_label` country and other countries.
    """
   
    path_base = bm_path / Path(str(year)) / Path(r'Corpus\deduplication\parsing')
    
    filename_dat = 'countries.dat'
    countries_file_dat = path_base / Path(filename_dat)
    
    
    filename_html = 'countries_graph.html'
    countries_file_html = path_base / Path(filename_html)    
    
    filename_gefx = 'countries.gexf'
    countries_file_gefx = path_base / Path(filename_gefx)
    
    counties_df = pd.read_csv(countries_file_dat,
                              sep='\t',
                              usecols = ['Pub_id','Country'])
    counties_df.columns = ['pub_id', 'item' ]
    
    G = generate_cooc_graph(counties_df, 2, item="CU")
    G = add_long_lat_to_node(G)
    G = add_title_to_node(G,'countries')

    G = create_star_graph(G,central_node_label)
    node_size_comment = "Taille des noeuds : nombre de pays collaboratifs"
    header = build_header(institute,year,datatype,node_size_comment)

    nt = cooc_graph_html_plot(G,str(countries_file_html),
                         header,size="degree")
    
    #plot_cooc_graph(G,"CU")
    _write_cooc_gexf(G, countries_file_gefx)

    return G

def get_filename_listeconsolideepubli(bm_path,year,datatype):

    file_name = 'Liste consolidée '+ str(year) + '_Articles & Proceedings.xlsx'
    bm_path = bm_path / 'Sauvegarde des résultats' / datatype / str(year)
    file = bm_path / 'Listes consolidées des publications' / file_name
    
    return file

def get_filename_listeconsolideebook(bm_path,year,datatype):

    file_name = 'Liste consolidée '+ str(year) + '_Books & Editorials.xlsx'
    bm_path = bm_path / 'Sauvegarde des résultats' / datatype / str(year)
    file = bm_path / 'Listes consolidées des publications' / file_name
    
    return file  
    
def get_departements_list(bm_path, institute):
    
    """
    Function `get_departements_list` gets the institute departements list from the json file
    <Institute>Org_config.json located in the "Pamametres Institut" directory
    """
    
    if institute.capitalize() == 'Liten':
        file = Path(bm_path) / 'Parametres Institut' / 'LitenOrg_config.json'
    elif institute.capitalize() == 'Leti':
        file = Path(bm_path) / 'Parametres Institut' / 'LetiOrg_config.json'
    else:
        pass # raises error
        
    with open(file) as f:
        d = json.load(f)
        
    dep_list = list(d["COL_NAMES_DPT"].values())
    
    return dep_list

def build_header(institute,year,datatype,node_size_comment):
    
    header = ( '<h1>'
                  f'<font color=#33afff><b>{institute} - {year}</b></font color>'
              '</h1>'
              '<p>'
                  f'Base de donn&eacute;es: {datatype}, {node_size_comment}'
              '</p>'
              '<p>'
                  '<a href="https://github.com/Bertin-fap/BiblioReport">Cr&eacute;&eacute par BiblioReport</a>'
              '</p>')
    return header
    
def plot_graph_departement(bm_path,institute,year,datatype):
    
    """
    Function `plot_graph_departement` builds and plots a graph G(nodes,h). The nodes are the institute departements
    and the edges connect two departements which have co-authaured at least one article during the year `year`. 
    The article corpus has been built using the database`.
    """
  
    # Get the departements liste from the json file 
    # the Excel file "Liste consolidée <year>_Articles & Proceedings.xlsx"
    dep_list = get_departements_list(bm_path, institute)
    file = get_filename_listeconsolideepubli(bm_path,year,datatype)
    df = pd.read_excel(file,usecols=['Pub_id'] + dep_list)
    
    # Build the graph G out of the Excel file 
    list_pub_id = []
    list_dep_publi = []
    for row in df.iterrows():
        row = row[1]
        for dep in dep_list:
            if row[dep]:
                list_pub_id.append(row['Pub_id'])
                list_dep_publi.append(dep)
    
    dg = pd.DataFrame(list(zip(list_pub_id, list_dep_publi)),
                   columns =['Pub_id', 'item'])
    
    G = generate_cooc_graph(dg, 1, item='item')
    G = add_title_to_node(G,'departments')
    
    node_size_comment = "Taille des noeuds : nombre de publications du d&eacute;partement"
    header = build_header(institute,year,datatype,node_size_comment)
    
    cooc_graph_html_plot(G,
                         r"c:\users\franc\Temp\dep.html",
                         header,
                         size="size")   
                         
def plot_cooc_graph(G, item, size_min=None, node_size_ref=None):

    """
    The `plot_cooc_graph` function plots the co-occurrence graph G.
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

    """
    The `_write_cooc_gexf` function saves the graph `G"`
    in Gephy (`.gexf`) format using full path filename.
       
    Args:
        G (networkx ogject): a co-occurrence graph built using 
                             the function `_generate_cooc_graph`.
        filename (Path): full path for saving the Gephy file (`.gexf`).
        
    """

    assert isinstance(G, nx.classes.graph.Graph), "G should be a networkx Graph"

    nx.write_gexf(G, filename)


def _write_cooc_gdf(G, item, color, filename):

    """
    The `_write_cooc_gdf` function saves the graph `G` 
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
            
