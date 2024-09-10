'''
Toolbox of functions used to plot the key factors indicator (kpi) computed using the package BiblioMeter.
Three kpi are ploted : the keywords using wordcloud; the numbers of paper coauthored with foreign countries
as a geoplot representation; the number of articles per journal represented as a barchart. 
In this module:
    - dept stands for the departement of the institute
    - the prfix kw stands for Key Word kw_type can be :AK, IK, TK
    - corpus_year is the year of the corpus extraction
    - datatype is the name of the databases used to build the corpus (WoS, Scopus, Hal)
    - bibliometer_path is the root path of the data base (for more detail consults https://github.com/TickyWill/BiblioMeter/blob/main/BiblioMeterUserManual-Fr.pdf)
'''

__all__ = ['create_kw_cloud',
           'parse_kw_filename',
           'plot_countries_analysis',
           'plot_if_analysis']

# Standard library imports
import os
import re
from collections import namedtuple
from pathlib import Path
from tkinter import messagebox
import webbrowser

# Third party imports
import bmfuncts.pub_globals as pg
import BiblioParsing.BiblioSpecificGlobals as bp
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import plotly.offline as py
import plotly.graph_objs as go
import bmrfuncts.functs_globals as gr
from bmfuncts.rename_cols import set_final_col_names
from bmfuncts.config_utils import set_org_params
from bmfuncts.rename_cols import set_final_col_names

def set_paths(bibliometer_path,corpus_year,datatype):

    '''
    creates the dict `path_dic` ={kpi_type:kpi_path} where kpi_type stands for 
    "key parameter indicator" (alias kpi) type (kw,geo,ifs,kpi) and where kpi_path is the full name 
    of the directory which hosts the excel files related to this kpi.
    '''
    
    # Setting useful aliases
    save_folder_alias         = pg.ARCHI_RESULTS["root"]
    if_analysis_folder_alias  = pg.ARCHI_RESULTS["impact-factors"]
    kw_analysis_folder_alias  = pg.ARCHI_RESULTS["keywords"]
    geo_analysis_folder_alias = pg.ARCHI_RESULTS["countries"]
    kpi_analysis_folder_alias = pg.ARCHI_RESULTS["kpis"]
    
    # Finding the directory name associated with datatype
    datatype_idx = pg.DATATYPE_LIST.index(datatype)
    datatype_dir = pg.ARCHI_RESULTS[pg.DATATYPE_LIST[datatype_idx]]
    
    # Setting useful paths
    base_folder_path         = bibliometer_path / Path(save_folder_alias)
    datatype_folder_path     = base_folder_path / Path(datatype_dir)
    year_folder_path         = datatype_folder_path / Path(str(corpus_year))
    if_analysis_folder_path  = year_folder_path / Path(if_analysis_folder_alias)
    kw_analysis_folder_path  = year_folder_path / Path(kw_analysis_folder_alias)
    geo_analysis_folder_path = year_folder_path / Path(geo_analysis_folder_alias)
    kpi_folder_path          = datatype_folder_path / Path(kpi_analysis_folder_alias)
    
    path_dic =dict(kw  = kw_analysis_folder_path,
                   geo = geo_analysis_folder_path,
                   ifs = if_analysis_folder_path,
                   kpi = kpi_folder_path)
    return path_dic
    

def parse_kw_filename(bibliometer_path, corpus_year, metric, extension, datatype):
    
    '''Parse the files name with extention `extension` of a kpi directory to extract : (i) the year
    of the corpus `corpus_year`; (ii) the departement `dep`; (iii) the kpi type `kw`. For each files, these 
    three values are stored in a namedtuple.
    '''

    path_dic = set_paths(bibliometer_path,corpus_year,datatype)
    
    if metric == "IF":
        metric_analysis_folder_path = path_dic["ifs"] # if_analysis_folder_path
        pattern = re.compile('(?P<kw>^\w*\s)(?P<year>\d{4})-(?P<dep>\w*)\.')
    elif metric == "KW":
        metric_analysis_folder_path = path_dic["kw"] # kw_analysis_folder_path
        pattern = re.compile('(?P<dep>^\w*\s)(?P<year>\d{4})-(?P<kw>\w*)\.')

    kw_tup = namedtuple('kw_tup',['dep' , 'year', 'kw'])
    
    dep_list = []
    year_list = []
    kw_list = []
    
    
    files = [x for x in os.listdir(metric_analysis_folder_path) 
                 if x.endswith(extension)]
    for file in files:
        match = pattern.match(file)
        if match:
            dep_list.append(match.group('dep'))
            year_list.append(match.group('year'))
            kw_list.append(match.group('kw'))

    kw = kw_tup (list(set(dep_list)), list(set(year_list)),  list(set(kw_list)))
    
    return kw
    
def select_if_file(corpus_year,dept,bibliometer_path, datatype):
    
    '''
    Selects the excel files name of the kpi impact factor of the year `corpus_year` witch contain 
    the departement acronyme `dept`. Only one file should comply with this criteria
    and the full path of this file is returned.
    '''
    
    path_dic = set_paths(bibliometer_path,corpus_year,datatype)
    
    files = [x for x in os.listdir(path_dic['ifs']) 
             if x.endswith(".xlsx") and dept in x]
    if files:
        dept_xlsx_file_path = Path(path_dic['ifs']) / Path(files[0])
        return dept_xlsx_file_path
    else:
        print(f'file not found')
    
    
    
def create_kw_cloud(institute, corpus_year, kw_type, dept, bibliometer_path,datatype,
                     verbose = False):
                         
    """Creates a wordcloud of the keywords.
    """

    # Setting useful aliases
    keywords_col_alias       = bp.COL_NAMES['keywords'][1]
    weight_col_alias         = pg.COL_NAMES_BONUS['weight']
    unknown_alias            = bp.UNKNOWN

    # Setting useful paths
    path_dic = set_paths(bibliometer_path,corpus_year,datatype)
    kw_analysis_folder_path = path_dic["kw"]
    
    # Setting the maximum length of the words for the cloud
    kw_length = gr.CLOUD_MAX_WORDS_LENGTH

    # Builds file name and exit if the file do nont exist
    dept_xlsx_file_path = kw_analysis_folder_path / Path(f'{dept.strip()} {corpus_year}-{kw_type}.xlsx')
    if not os.path.exists(dept_xlsx_file_path):
        messagebox.showwarning("Plot KW", f"Sorry unable to find a .xlsx files corresponding to {dept}")
        return
        
    # Builds the dataframe of keywords with their weight (number of occurrences)  
    dept_kw_df = pd.read_excel(dept_xlsx_file_path)
    dept_kw_df[keywords_col_alias] = dept_kw_df[keywords_col_alias].\
        apply(lambda x: x[0:kw_length])

    # Building the keywords list where each keyword is repeated as many times as its number of occurrences (weight)
    dept_kw_list = []
    for _, row in dept_kw_df.iterrows():
        keyword = row[keywords_col_alias]
        weight  = row[weight_col_alias]
        if keyword != unknown_alias:
            keyword_list = [keyword] * weight
            dept_kw_list = dept_kw_list + keyword_list

    # Building the text 'dept_kw_txt' that contains the keywords
    dept_kw_txt = ' '.join(dept_kw_list)
    dept_kw_txt.encode(encoding = 'UTF-8', errors = 'strict')

    # create and save the cloud image for department 'dept'
    if dept_kw_txt!='':
        dept_png_file_path = kw_analysis_folder_path / Path(f"{kw_type} {corpus_year}-{dept}.png")
        _keywords_cloud(dept_kw_txt,
                       dept_png_file_path,
                       gr.CLOUD_BCKG,
                       gr.CLOUD_HEIGHT,
                       gr.CLOUD_WIDTH,
                       gr.CLOUD_MAX_WORDS,
                       corpus_year,
                       dept,
                       kw_type,
                       datatype,
                       institute,)

    message = ("\n    Wordcloud images for all keywords types "
               f"and all departments saved in : \n {kw_analysis_folder_path}")
    if verbose:
        print(message, "\n")
        
def _set_wordcloud_title(corpus_year, dept, kw_type, datatype, institute):
    
    ''' Sets the title of wordcoud plot'''
    
    title = f'Année: {corpus_year}, Institut: {institute},Départemement: {dept}\n' 
    title = title + f'Mot-clé: {kw_type}, Base de données : {datatype}'
    
    return title
    
def _keywords_cloud(txt,
                    out,
                    bckg,
                    h,
                    w,
                    mxw,
                    corpus_year,
                    dept,
                    kw_type,
                    datatype,
                    institute,
                    verbose = False):
    """
    Plots the wordcloud of the text `txt`.
    
    Args:
        txt (str): Text which words will be plot as cloud.
        out (path): Full path of the png file that will contain the plot image.
        bckg (str): Color of the plot background.
        h (int): Height of the plot in pixels.
        w (int): Width of the plot in pixels.
        mxw (int): Maximum number of words to be plot.

    Returns:
        (str): Message about the completion of the image building.

    """

    wc = WordCloud(background_color = bckg,
                   height           = h,
                   width            = w,
                   max_words        = mxw,
                   collocations     = False)
    cloud = wc.generate(txt)
    cloud.to_file(out)
    plt.imshow(wc, interpolation='bilinear')
    title = _set_wordcloud_title(corpus_year, dept, kw_type, datatype, institute)
    plt.title(title)
    plt.axis("off")
    plt.show()

    message = f"\n    Wordcloud image saved in file: \n {out}"
    if verbose:
        print(message)

def _sets_title_countries_analysis(continents_df,
                                  nbr_pubi_france,
                                  corpus_year,
                                  datatype,
                                  institute):
                                      
    '''Sets the title of the html plot
    '''                                 
    title = f'Institut {institute}, Année {corpus_year}<br> '
    title = title + f'Base de données {datatype}, Nbre publications françaises : {nbr_pubi_france}<br> '
    for idx,row in continents_df.iterrows():
        title = title + f'{row[0]}: {row[1]}; '
    return title

def plot_countries_analysis(corpus_year,bibliometer_path, datatype, institute):
    
    '''Interactive geographic representatin of the number of articles co-authored  by the `institute`
    and a country. 
    '''
    
    # Setting useful aliases
    unknown_alias            = bp.UNKNOWN
    geo_file_alias = pg.ARCHI_YEAR["country weight file name"]+' '+str(corpus_year)
    cont_file_alias = pg.ARCHI_YEAR["continent weight file name"]+' '+str(corpus_year)
    
    # Setting useful paths
    path_dic = set_paths(bibliometer_path,corpus_year,datatype)
    geo_analysis_folder_path = path_dic["geo"]
    continent_file           = geo_analysis_folder_path / Path(cont_file_alias+".xlsx")              
    geo_file                 = geo_analysis_folder_path / Path(geo_file_alias+".xlsx")
    
    # Reads the country and continent Excel files and remap countries with there iso code   
    countries = pd.read_excel(geo_file,engine="openpyxl")
    countries['Code'] = countries['Pays'].map(gr.DIC_CODE_COUNTRIES)
    continents_df = pd.read_excel(continent_file,engine="openpyxl")
    
    # Builds the relevent list forcing the number of publication of France to 1
    list_countries           = countries['Code'] .tolist() 
    nbr_articles_per_country = countries['Nombre de publications'].tolist()
    ifx_france = list_countries.index("FRA")
    nbr_pubi_france = nbr_articles_per_country[ifx_france]
    nbr_articles_per_country[ifx_france] = 1
    
    # Sets the title of the map
    title = _sets_title_countries_analysis(continents_df, nbr_pubi_france, corpus_year, datatype, institute)
    
    # Builds the map
    layout = dict(geo={'scope': 'world'})
    
    data = dict(type='choropleth',
                locations=list_countries,
                locationmode='ISO-3',
                colorscale = 'Portland',
                autocolorscale = False,
                marker = dict(line = dict (color = 'rgb(255,255,255)', width = 1)),
                z=nbr_articles_per_country,
                colorbar = {'title':'# Publications'})
    
    map = go.Figure(data=[data], layout=layout)
    map.update_layout(title_text=title, title_x=0.5)
    
    # showing html plot 
    map.show()
    
    # Saving the map as html and png files
    _save_plot_countries_analysis(map,bibliometer_path,corpus_year, datatype) 
    
    # ploting png
    png_plot = messagebox.askquestion('png plot','Voulez vous tracer le fichier .png')
    if png_plot == "yes":
        _plot_countries_analysis_png(bibliometer_path,corpus_year, datatype)
    
 
    
def _save_plot_countries_analysis(map,bibliometer_path,corpus_year, datatype):
    
    # Setting useful aliases
    geo_file_alias = pg.ARCHI_YEAR["country weight file name"]+' '+str(corpus_year)
    
    # Setting useful paths
    path_dic = set_paths(bibliometer_path,corpus_year,datatype)
    geo_analysis_folder_path = path_dic["geo"]
    html_path                = geo_analysis_folder_path/ Path(geo_file_alias+".html")
    png_path                 = geo_analysis_folder_path/ Path(geo_file_alias+".png")
    
    # Saving as an htm file
    map.write_html(str(html_path))
    
    # Saving as an png file
    map.write_image(png_path)
    
    
def _plot_countries_analysis_png(bibliometer_path,corpus_year, datatype):
    
    ''' Plots the png file
    '''
    
    # Setting useful aliases
    geo_file_alias = pg.ARCHI_YEAR["country weight file name"]+' '+str(corpus_year)
    
    # Setting useful paths
    path_dic = set_paths(bibliometer_path,corpus_year,datatype)
    geo_analysis_folder_path = path_dic["geo"]
    png_path                 = geo_analysis_folder_path/ Path(geo_file_alias+".png")
    
    # ploting png image
    fig, ax = plt.subplots(nrows=1, ncols=1)
    img = mpimg.imread(png_path)
    imgplot = ax.imshow(img)
    ax.axis('off')
    plt.show()

    
def _reads_kpi_dict(institute, bibliometer_path, corpus_year, org_tup, dept, datatype):
    
    '''Builds the dictionary `dic_kpi` of the kpi (key performance indicator) out of the kpi database.
    The kpi database is an Excel file sets by BiblioMeter. `dic_kpi` = {kpi indicator: kpi valu}.
    '''
    
    # Setting aliases for KPIs database
    kpi_file_base_alias      = pg.ARCHI_RESULTS["kpis file name base"]
    
    # Setting paths for saving results
    path_dic = set_paths(bibliometer_path,corpus_year,datatype)
    results_kpis_folder_path = path_dic["kpi"]
    
    filename = dept + "_" + kpi_file_base_alias + ".xlsx"
    file_path = results_kpis_folder_path / Path(filename)
    
    kpi_df = pd.read_excel(file_path)
    kpi_dic= dict(zip(kpi_df['Année de publication'],kpi_df[corpus_year]))
    kpi_dic = {"Année de publication":corpus_year} | kpi_dic
    
    return kpi_dic    

def _builds_if_bargraph_title(kpi_dict,
                              dept,
                              corpus_year,
                              if_col,
                              part,
                              datatype):
    
    '''Builds the bargraph title from the kpi metrics'''
    
    # Setting useful values for barchart plot and title
    nb_journals          = kpi_dict[pg.KPI_KEYS_ORDER_DICT[7]]
    nb_articles          = kpi_dict[pg.KPI_KEYS_ORDER_DICT[11]]
    articles_per_journal = kpi_dict[pg.KPI_KEYS_ORDER_DICT[12]]
    if_max               = kpi_dict[pg.KPI_KEYS_ORDER_DICT[15]]
    if_min               = kpi_dict[pg.KPI_KEYS_ORDER_DICT[16]]
    if_moyen             = kpi_dict[pg.KPI_KEYS_ORDER_DICT[17]]
    wo_if_ratio          = kpi_dict[pg.KPI_KEYS_ORDER_DICT[19]]

    # Setting the first part of the barchart title
    title_base  = (f"{dept} corpus {corpus_year} database {datatype}: "
                   f"Journals = {nb_journals}, Articles = {nb_articles}, "
                   f"Articles/Journal = {articles_per_journal: .1f}")

    # Completing the barchart title
    if_values = if_col
    if part != "all":
        if_values += " " + part + " half"

    title_add = ("<br>" + f"{if_values}: IF max = {if_max:.1f}, IF min = {if_min:.1f}, "
                 f"IF mean = {if_moyen:.1f}, Articles w/o IF = {wo_if_ratio:.0f} %" + "<br>")
    title = title_base + title_add

    return title 

def _plot_if_png(dept_png_file_path,corpus_year,dept):
    
    ''' Plots the png file `dept_png_file_path`
    '''
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
    img = mpimg.imread(dept_png_file_path)
    imgplot = ax.imshow(img)
    ax.set(title=f'Année: {corpus_year}, Départemement: {dept}\n')
    ax.axis('off')
    plt.show()    
    
def _create_if_barchart(corpus_year,
                        dept,
                        if_df,
                        if_col, 
                        kpi_dict,
                        journal_col_alias,
                        datatype,
                        bar_height_px,
                        part = "all",
                        ):
    """
    Builds a barchart with ordinates the journal name and abscissa the number of articles 
    in the journal. The color code of the bar is related to the journal impact factor.
    """

    # internal functions
    def _short_journal_name(max_journal_short_name):
        return lambda x: (x[:max_journal_short_name] + '...'
                          if len(x) > max_journal_short_name else x)

    # Setting new col names and related parameters
    journal_short_col_alias = pg.COL_NAMES_IF_ANALYSIS['journal_short']
    articles_nb_col_alias   = pg.COL_NAMES_IF_ANALYSIS['articles_nb']
    max_journal_short_name  = pg.BAR_Y_LABEL_MAX

    # Creating columns with shortnames of journals for barchart plots
    plot_df = if_df.copy()
    plot_df[journal_short_col_alias] = plot_df[journal_col_alias].\
        apply(_short_journal_name(max_journal_short_name))

    title = _builds_if_bargraph_title(kpi_dict,
                                      dept,
                                      corpus_year,
                                      if_col,
                                      part,
                                      datatype)

    # Setting barchart parameters
    labels_dict       = {articles_nb_col_alias  : 'Articles number',
                         journal_short_col_alias: 'Short name'}
    nb_articles_range = gr.BAR_X_RANGE
    barchart_width    = gr.BAR_WIDTH
    barchart_height = bar_height_px
    nb_journals       = kpi_dict[pg.KPI_KEYS_ORDER_DICT[7]]
    if nb_journals <= gr.BAR_Y_MAX or part != "all":
        barchart_height = round(bar_height_px / gr.BAR_HEIGHT_RATIO)
    print(barchart_height)
    color_range       = gr.BAR_COLOR_RANGE
    color_scale       = gr.BAR_COLOR_SCALE

    barchart = px.bar(data_frame             = plot_df,
                      x                      = articles_nb_col_alias,
                      y                      = journal_short_col_alias,
                      orientation            = 'h',
                      title                  = title,
                      color                  = if_col,
                      color_continuous_scale = color_scale,
                      range_color            = color_range,
                      labels                 = labels_dict,
                      width                  = barchart_width,
                      height                 = barchart_height,
                      hover_name             = journal_col_alias,
                      hover_data             = {journal_short_col_alias: False,
                                                if_col: ':.1f'},
                      range_x                = nb_articles_range,)
    barchart.show()
    return barchart
    
def _save_dept_barchart(barchart, dept, if_col, if_analysis_folder_path, part = "all"):
    
    """
    """

    file_name = f"{if_col}-{dept}"
    if part != "all":
        file_name += f"_{part}"

    dept_html_file_path = Path(if_analysis_folder_path) / Path(file_name + ".html")
    barchart.write_html(dept_html_file_path)

    dept_png_file_path  = Path(if_analysis_folder_path) / Path(file_name + ".png")
    barchart.write_image(dept_png_file_path)

    end_message  = (f"\n    Barchart of {if_col} ({part} values) for {dept} "
                    f"department saved in : \n {if_analysis_folder_path}")
    return end_message, dept_png_file_path


def plot_if_analysis(institute,
                     corpus_year,
                     dept,
                     bibliometer_path,
                     datatype,
                     bar_height_px,
                     verbose = True):
    """
    Plots Impact Factor (IF) bargraph using the excel files generated by BiblioMeter. Two types of excel files are
    used. 
    The first files located in bibliometer_path\institute\BiblioMeter_Files\corpus_year\5-Analyses\IFs these files
    are named "IF YYYY-<dept>.xlsx" contain 3 columns named "Jounal" (journal title), "Number" (number of publications) 
    in this journal), "IF YYYY" (the Impact Factor of the journal at year YYYY).
    The second files are loacated in bibliometer_path\institute\BiblioMeter_Files\Sauvegarde des résultats\Synthèse des indicateurs.
    These files are named "<dept>_Synthèse des KPI.xlsx" the colums names are the corpus year and the cells contains Key Parameter Indicator (KPI). 
    The list of 19 KPI is is given by the global KPI_KEYS_ORDER_DICT of bmfuncts.pub_globals.

    """

    # internal functions
    def _create_save_barchart(dept,
                              bar_chart_if_df,
                              part):
                                  
        barchart = _create_if_barchart(corpus_year, dept, bar_chart_if_df,
                                       if_col, dept_kpi_dict, journal_col_alias, datatype, bar_height_px, part)
        message,dept_png_file_path  = _save_dept_barchart(barchart, dept, if_col,
                                       if_analysis_folder_path, part)
        png_plot = messagebox.askquestion('png plot','Voulez vous tracer le fichier .png')
        if png_plot == "yes":                                
            _plot_if_png(dept_png_file_path,corpus_year,dept)
        return message

    # Setting useful aliases
    org_tup = set_org_params(institute, bibliometer_path)
    final_col_dic, depts_col_list = set_final_col_names(institute, org_tup)
    journal_col_alias = final_col_dic['journal']
    
    # Setting useful path
    path_dic = set_paths(bibliometer_path,corpus_year,datatype)
    if_analysis_folder_path = path_dic["ifs"]

    dept_xlsx_file_path = select_if_file(corpus_year, dept, bibliometer_path, datatype)
    dept_if_df = pd.read_excel(dept_xlsx_file_path)
    
    if_col = dept_if_df.columns[2]
    dept_kpi_dict = _reads_kpi_dict(institute, bibliometer_path, corpus_year, org_tup, dept, datatype)
    
    if dept == institute: # We split the barchart into to parts "lower" and "upper"
        # Setting two dataframes with, respectively, upper and lower values
        # of full IF dataframe of INSTITUTE
        nb_journals       = dept_kpi_dict[pg.KPI_KEYS_ORDER_DICT[7]]
        journal_median    = dept_if_df.loc[int(nb_journals/2), journal_col_alias]
        if_median         = dept_if_df[dept_if_df[journal_col_alias] == \
                                       journal_median][if_col].values[0]
        upper_dept_if_df  = dept_if_df[dept_if_df[if_col] >= if_median]
        lower_dept_if_df  = dept_if_df[dept_if_df[if_col] < if_median]

        # Creating barchart with full IF dataframe of INSTITUTE
        message = _create_save_barchart(dept, dept_if_df, "all")
        if verbose:
            print(message, "\n")

        # Creating barchart with upper values of IF dataframe of INSTITUTE
        message = _create_save_barchart(dept, upper_dept_if_df, "upper")
        if verbose:
            print(message, "\n")

        # Creating barchart with upper values of IF dataframe of INSTITUTE
        message = _create_save_barchart(dept, lower_dept_if_df, "lower")
        if verbose:
            print(message, "\n")

    else:
        # creating barchart with full IF dataframe of dept
        message = _create_save_barchart(dept, dept_if_df, "all")
        if verbose:
            print(message, "\n")

    end_message = (f"\n    IF analysis plots for corpus {corpus_year} "
                   f"saved in : \n {if_analysis_folder_path}")
    if verbose:
        print(end_message, "\n")
