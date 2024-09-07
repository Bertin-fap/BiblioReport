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



def parse_kw_filename(bibliometer_path, year, metric, extension):
    '''Builds a list of namedtuples which entries are associated to files with extenson `extention` loacated in the ìnput_path`directory.
    The nametuples has 3 fields : `dep` hosts the departement name, `year` hosts the year and `kw` hosts the keyword type
    '''
    
    # Setting useful aliases
    xlsx_extent_alias        = ".xlsx"
    kw_analysis_folder_alias = pg.ARCHI_YEAR["keywords analysis"]
    if_analysis_folder_alias = pg.ARCHI_YEAR["if analysis"]
    analysis_folder_alias    = pg.ARCHI_YEAR["analyses"]
    pub_list_filename_base   = pg.ARCHI_YEAR["pub list file name base"]
    pub_list_filename        = pub_list_filename_base + " " + str(year) + xlsx_extent_alias
    pub_list_folder_alias    = pg.ARCHI_YEAR["pub list folder"]
    
    # Setting useful paths
    year_folder_path        = bibliometer_path / Path(str(year))
    pub_list_folder_path    = year_folder_path / Path(pub_list_folder_alias)
    analysis_folder_path    = year_folder_path / Path(analysis_folder_alias)
    kw_analysis_folder_path = analysis_folder_path / Path(kw_analysis_folder_alias)
    if_analysis_folder_path = analysis_folder_path / Path(if_analysis_folder_alias)
    
    if metric == "IF":
        metric_analysis_folder_path = if_analysis_folder_path
        pattern = re.compile('(?P<kw>^\w*\s)(?P<year>\d{4})-(?P<dep>\w*)\.')
    elif metric == "KW":
        metric_analysis_folder_path = kw_analysis_folder_path
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
    
def select_if_file(year,dep,bibliometer_path):
    
    '''selects the articles impact factor .xlsx file of year `year` witch contain the departement aconym `dep'''
    
    # Setting aliases
    analysis_folder_alias    = pg.ARCHI_YEAR["analyses"]
    if_analysis_folder_alias = pg.ARCHI_YEAR["if analysis"]
    
    # Setting useful paths
    year_folder_path        = bibliometer_path / Path(str(year))
    analysis_folder_path    = year_folder_path / Path(analysis_folder_alias)
    if_analysis_folder_path = analysis_folder_path / Path(if_analysis_folder_alias)
    
    files = [x for x in os.listdir(if_analysis_folder_path) 
                 if x.endswith(".xlsx") and dep in x]
    if files:
        dept_xlsx_file_path = Path(if_analysis_folder_path) / Path(files[0])
        return dept_xlsx_file_path
    else:
        print(f'file not found')
    
    
    
def create_kw_cloud(institute, year, kw_type, dep, bibliometer_path,
                     verbose = False):
    """Creates a wordcloud of the keywords.
    """
    # Setting useful aliases
    org_tup = set_org_params(institute, bibliometer_path)
    final_col_dic, depts_col_list = set_final_col_names(institute, org_tup)
    depts_col_list           = [dep] # overwrite depts_col_list as we dont loop on all departements
    parsing_pub_id_col_alias = bp.COL_NAMES['pub_id']
    kw_analysis_folder_alias = pg.ARCHI_YEAR["keywords analysis"]
    final_pub_id_col_alias   = final_col_dic['pub_id']
    keywords_col_alias       = bp.COL_NAMES['keywords'][1]
    weight_col_alias         = pg.COL_NAMES_BONUS['weight']
    unknown_alias            = bp.UNKNOWN
    analysis_folder_alias    = pg.ARCHI_YEAR["analyses"]
    pub_list_filename_base   = pg.ARCHI_YEAR["pub list file name base"]
    xlsx_extent_alias        = ".xlsx"
    pub_list_filename        = pub_list_filename_base + " " + str(year) + xlsx_extent_alias
    pub_list_folder_alias    = pg.ARCHI_YEAR["pub list folder"]

    # Setting useful paths
    year_folder_path        = bibliometer_path / Path(str(year))
    pub_list_folder_path    = year_folder_path / Path(pub_list_folder_alias)
    #pub_list_file_path      = pub_list_folder_path / Path(pub_list_filename)
    analysis_folder_path    = year_folder_path / Path(analysis_folder_alias)
    kw_analysis_folder_path = analysis_folder_path / Path(kw_analysis_folder_alias)
    

    # Setting the maximum length of the words for the cloud
    kw_length = gr.CLOUD_MAX_WORDS_LENGTH

    # Getting the dataframe of keywords with their weight
    dept_xlsx_file_path = kw_analysis_folder_path / Path(f'{dep.strip()} {year}-{kw_type}.xlsx')
    if not os.path.exists(dept_xlsx_file_path):
        messagebox.showwarning("Plot KW", f"Sorry unable to find a .xlsx files corresponding to {dep}")
        return
    dept_kw_df = pd.read_excel(dept_xlsx_file_path)
    dept_kw_df[keywords_col_alias] = dept_kw_df[keywords_col_alias].\
        apply(lambda x: x[0:kw_length])

    # Building the keywords list with each keyword repeated up to its weight
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
        dept_png_file_path = kw_analysis_folder_path / Path(f"{kw_type} {year}-{dep}.png")
        keywords_cloud(dept_kw_txt,
                       dept_png_file_path,
                       gr.CLOUD_BCKG,
                       gr.CLOUD_HEIGHT,
                       gr.CLOUD_WIDTH,
                       gr.CLOUD_MAX_WORDS,
                       year,
                       dep,
                       kw_type)

    message = ("\n    Wordcloud images for all keywords types "
               f"and all departments saved in : \n {kw_analysis_folder_path}")
    if verbose:
        print(message, "\n")
        
def keywords_cloud(txt, out, bckg, h, w, mxw, year, dep, kw, verbose = False):
    """
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
    plt.title(f'Année: {year}, Départemement: {dep}, Mot-clé: {kw}\n')
    plt.axis("off")
    plt.show()

    message = f"\n    Wordcloud image saved in file: \n {out}"
    if verbose:
        print(message)

def plot_countries_analysis(year,bibliometer_path):
    
    # Setting useful aliases
    unknown_alias            = bp.UNKNOWN
    xlsx_extent_alias        = ".xlsx"
    geo_folder_alias         = pg.ARCHI_YEAR["countries analysis"]
    analysis_folder_alias    = pg.ARCHI_YEAR["analyses"]
    
    # Setting useful paths
    year_folder_path         = bibliometer_path / Path(str(year))
    analysis_folder_path     = year_folder_path / Path(analysis_folder_alias)
    geo_analysis_folder_path = analysis_folder_path / Path(geo_folder_alias) 
    geo_file                 = geo_analysis_folder_path / Path('Statistiques par pays.xlsx')
    html_path                = geo_analysis_folder_path/ Path('Statistiques par pays.html')
    
    countries= pd.read_excel(geo_file,engine="openpyxl")
    countries['Code'] = countries['Pays'].map(gr.DIC_CODE_COUNTRIES)
    countries['number_publis'] =  countries.apply(lambda row: len(row['Liste des Pub_ids'].split(';')),axis=1)
                                                                            
    list_countries           = countries['Code'] .tolist() 
    nbr_articles_per_country = countries['number_publis'].tolist()
    
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
    map.write_html(str(html_path)) 
    # show file 
    webbrowser.open(html_path)
    

def _reads_kpi_dict(institute, bibliometer_path, corpus_year, org_tup, dept, datatype):
    
    # Setting aliases for updating KPIs database
    results_root_alias       = pg.ARCHI_RESULTS["root"]
    results_folder_alias     = pg.ARCHI_RESULTS[datatype]
    results_sub_folder_alias = pg.ARCHI_RESULTS["kpis"]
    kpi_file_base_alias      = pg.ARCHI_RESULTS["kpis file name base"]

    # Setting paths for saving results
    results_root_path        = bibliometer_path / Path(results_root_alias)
    results_folder_path      = results_root_path / Path(results_folder_alias)
    results_kpis_folder_path = results_folder_path / Path(results_sub_folder_alias)
    
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
                              part):
    
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
    title_base  = (f"{dept} corpus {corpus_year}: "
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

def plot_if_png(dept_png_file_path,year,dept):
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
    img = mpimg.imread(dept_png_file_path)
    imgplot = ax.imshow(img)
    ax.set(title=f'Année: {year}, Départemement: {dept}\n')
    ax.axis('off')
    plt.show()    
    
def _create_if_barchart(corpus_year,
                        dept,
                        if_df,
                        if_col, 
                        kpi_dict,
                        journal_col_alias,
                        part = "all"):
    """
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
                                      part)

    # Setting barchart parameters
    labels_dict       = {articles_nb_col_alias  : 'Articles number',
                         journal_short_col_alias: 'Short name'}
    nb_articles_range = gr.BAR_X_RANGE
    barchart_width    = gr.BAR_WIDTH
    barchart_height   = gr.BAR_HEIGHT
    nb_journals       = kpi_dict[pg.KPI_KEYS_ORDER_DICT[7]]
    if nb_journals <= gr.BAR_Y_MAX or part != "all":
        barchart_height = round(gr.BAR_HEIGHT / gr.BAR_HEIGHT_RATIO)
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
                                       if_col, dept_kpi_dict, journal_col_alias, part)
        message,dept_png_file_path  = _save_dept_barchart(barchart, dept, if_col,
                                       if_analysis_folder_path, part)
        plot_if_png(dept_png_file_path,corpus_year,dept)
        return message

    # Setting useful aliases
    org_tup = set_org_params(institute, bibliometer_path)
    final_col_dic, depts_col_list = set_final_col_names(institute, org_tup)
    journal_col_alias = final_col_dic['journal']
    pub_list_folder_alias    = pg.ARCHI_YEAR["pub list folder"]
    analysis_folder_alias    = pg.ARCHI_YEAR["analyses"]
    if_analysis_folder_alias = pg.ARCHI_YEAR["if analysis"]
    
    # Setting useful paths
    year_folder_path        = bibliometer_path / Path(corpus_year)
    pub_list_folder_path    = year_folder_path / Path(pub_list_folder_alias)
    analysis_folder_path    = year_folder_path / Path(analysis_folder_alias)
    if_analysis_folder_path = analysis_folder_path / Path(if_analysis_folder_alias)

    dept_xlsx_file_path = select_if_file(corpus_year, dept, bibliometer_path)
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