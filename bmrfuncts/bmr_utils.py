__all__ = ['create_kw_cloud',
           'parse_kw_filename',
           'plot_countries_analysis']

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
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import plotly.offline as py
import plotly.graph_objs as go
from bmfuncts.rename_cols import set_final_col_names
from bmfuncts.config_utils import set_org_params



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
    #pub_list_file_path      = pub_list_folder_path / Path(pub_list_filename)
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
    
def create_kw_cloud(institute, year, kw_type, dep, bibliometer_path,
                     verbose = False):
    """
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
    kw_length = pg.CLOUD_MAX_WORDS_LENGTH

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
                       pg.CLOUD_BCKG,
                       pg.CLOUD_HEIGHT,
                       pg.CLOUD_WIDTH,
                       pg.CLOUD_MAX_WORDS,
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
   
    COUNTRIES_CODES = '''United States:USA,Afghanistan:AFG,Albania:ALB,Algeria:DZA,American Samoa:ASM,Andorra:AND,
    Angola:AGO,Anguilla:AIA,Antarctica:ATA,Antigua And Barbuda:ATG,Argentina:ARG,Armenia:ARM,Aruba:ABW,
    Australia:AUS,Austria:AUT,Azerbaijan:AZE,Bahamas:BHS,Bahrain:BHR,Bangladesh:BGD,Barbados:BRB,
    Belarus:BLR,Belgium:BEL,Belize:BLZ,Benin:BEN,Bermuda:BMU,Bhutan:BTN,Bolivia:BOL,
    Bosnia And Herzegowina:BIH,Botswana:BWA,Bouvet Island:BVT,Brazil:BRA,Brunei Darussalam:BRN,
    Bulgaria:BGR,Burkina Faso:BFA,Burundi:BDI,Cambodia:KHM,Cameroon:CMR,Canada:CAN,Cape Verde:CPV,
    Cayman Islands:CYM,Central African Rep:CAF,Chad:TCD,Chile:CHL,China:CHN,Christmas Island:CXR,
    Cocos Islands:CCK,Colombia:COL,Comoros:COM,Congo:COG,Cook Islands:COK,Costa Rica:CRI,
    Cote D`ivoire:CIV,Croatia:HRV,Cuba:CUB,Cyprus:CYP,Czech Republic:CZE,Denmark:DNK,Djibouti:DJI,
    Dominica:DMA,Dominican Republic:DOM,East Timor:TLS,Ecuador:ECU,Egypt:EGY,El Salvador:SLV,
    Equatorial Guinea:GNQ,Eritrea:ERI,Estonia:EST,Ethiopia:ETH,Falkland Islands (Malvinas):FLK,
    Faroe Islands:FRO,Fiji:FJI,Finland:FIN,France:FRA,French Guiana:GUF,French Polynesia:PYF,
    French S. Territories:ATF,Gabon:GAB,Gambia:GMB,Georgia:GEO,Germany:DEU,Ghana:GHA,Gibraltar:GIB,
    Greece:GRC,Greenland:GRL,Grenada:GRD,Guadeloupe:GLP,Guam:GUM,Guatemala:GTM,Guinea:GIN,
    Guinea-bissau:GNB,Guyana:GUY,Haiti:HTI,Honduras:HND,Hong Kong:HKG,Hungary:HUN,Iceland:ISL,
    India:IND,Indonesia:IDN,Iran:IRN,Iraq:IRQ,Ireland:IRL,Israel:ISR,Italy:ITA,Jamaica:JAM,Japan:JPN,
    Jordan:JOR,Kazakhstan:KAZ,Kenya:KEN,Kiribati:KIR,North Korea:PRK,South Korea:KOR,Kuwait:KWT,
    Kyrgyzstan:KGZ,Laos:LAO,Latvia:LVA,Lebanon:LBN,Lesotho:LSO,Liberia:LBR,Libya:LBY,Liechtenstein:LIE,
    Lithuania:LTU,Luxembourg:LUX,Madagascar:MDG,Malawi:MWI,Malaysia:MYS,Maldives:MDV,Mali:MLI,
    Malta:MLT,Marshall Islands:MHL,Martinique:MTQ,Mauritania:MRT,Mauritius:MUS,Mayotte:MYT,Mexico:MEX,
    Monaco:MCO,Mongolia:MNG,Montserrat:MSR,Morocco:MAR,Mozambique:MOZ,Myanmar:MMR,Namibia:NAM,
    Nauru:NRU,Nepal:NPL,Netherlands:NLD,New Caledonia:NCL,New Zealand:NZL,Nicaragua:NIC,Niger:NER,
    Nigeria:NGA,Niue:NIU,Norfolk Island:NFK,Northern Mariana Islands:MNP,Norway:NOR,Oman:OMN,
    Pakistan:PAK,Palau:PLW,Panama:PAN,Papua New Guinea:PNG,Paraguay:PRY,Peru:PER,Philippines:PHL,
    Pitcairn:PCN,Poland:POL,Portugal:PRT,Puerto Rico:PRI,Qatar:QAT,Romania:ROU,Russian Federation:RUS,
    Rwanda:RWA,Saint Kitts And Nevis:KNA,Saint Lucia:LCA,St Vincent/Grenadines:VCT,Samoa:WSM,
    San Marino:SMR,Sao Tome:STP,Saudi Arabia:SAU,Senegal:SEN,Seychelles:SYC,Sierra Leone:SLE,
    Singapore:SGP,Slovakia:SVK,Slovenia:SVN,Solomon Islands:SLB,Somalia:SOM,South Africa:ZAF,
    Spain:ESP,Sri Lanka:LKA,St. Helena:SHN,St.Pierre:SPM,Sudan:SDN,Suriname:SUR,Swaziland:SWZ,
    Sweden:SWE,Switzerland:CHE,Syrian Arab Republic:SYR,Taiwan:TWN,Tajikistan:TJK,Tanzania:TZA,
    Thailand:THA,Togo:TGO,Tokelau:TKL,Tonga:TON,Tunisia:TUN,Turkey:TUR,Turkmenistan:TKM,Tuvalu:TUV,
    Uganda:UGA,Ukraine:UKR,United Arab Emirates:ARE,United Kingdom:GBR,Uruguay:URY,Uzbekistan:UZB,
    Vanuatu:VUT,Vatican City State:VAT,Venezuela:VEN,Viet Nam:VNM,Virgin Islands (British):VGB,
    Virgin Islands (U.S.):VIR,Western Sahara:ESH,Yemen:YEM,Zambia:ZMB,Zimbabwe:ZWE'''
    
    dic_code_countries = {y.split(':')[0].strip('\n').strip():y.split(':')[1]  for y in COUNTRIES_CODES.split(',')}
    
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
    
    countries= pd.read_excel(geo_file,engine="openpyxl")
    countries['Code'] = countries['Pays'].map(dic_code_countries)
    countries['number_publis'] =  countries.apply(lambda row: len(row['Liste des Pub_ids'].split(';')),axis=1)
    
                                                                              
    list_countries,nbr_articles_per_country = countries['Code'] .tolist(),  countries['number_publis'].tolist()
    
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
    py.plot(map)
    html_path = bibliometer_path / Path(str(year)) / Path("5 - Analyses")/ Path('Géographique') / Path('Statistiques par pays.html')
    map.write_html(str(html_path)) 
    # show file 
    webbrowser.open(html_path) 