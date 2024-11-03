"""
The `makeword` module builds a bibliography as a Word .docx document.
The files "Liste consolidée <year>_Articles & Proceedings.xlsx", "Liste consolidée <year>_Books & Editorials.xlsx" are used as well as
the file "Informations auteur par publication <year>.xlsx". These files are built by the package BiblioMeter.
The template Word file "template_liste.docx" is used.
The main function of this module is `make_document`.
"""

__all__ = ['make_document']
import re
from pathlib import Path
import pathlib

import pandas as pd
from docxtpl import DocxTemplate

# Local imports
from brfuncts.toolbox import  get_filename_listeconsolideepubli 
from brfuncts.toolbox import  get_filename_listeconsolideebook
from brfuncts.toolbox import  get_filename_analyseparauteurs
from brfuncts.toolbox import  get_departements_list

def dicriminate_nom_prenom(row:str,col_name:str)->str:
    
    """
    The function `dicriminate_nom_prenom` normalizes the composite surname as surname_1 surnam_2 name into
    surname_1-surnam_2 name. Ex: Bauer Cathenot F --> Bauer-Cathenot F.
    """
    
    auth = row[col_name]
    chunk_list = auth.split(' ')
    if len(chunk_list)>2:
        auth = f'{chunk_list[0]}-{chunk_list[1]} {chunk_list[2]}'
    return auth

def normalize_nom_prenom(auth:str)->str:
    auth_normalized = f"{normalize_prenom(auth.split()[1])} {normalize_nom(auth.split()[0])}"
    return auth_normalized

def normalize_prenom(prenom:str)->str:
    prenom = prenom.replace('-','').upper()
    prenom = '-'.join(list(prenom))+'.'

    return prenom
    
def normalize_nom(nom:str)->str:
    
    """
    Function `normalize_nom` capitalize name taking care of composite name
    """
    
    flag_apostrophe = True if "'" in nom else False
    flag_dash = True if "-" in nom else False
    nom = ' '.join([x.capitalize() for x in re.split(r"[\s\-']+", nom)])
    if flag_apostrophe: nom = nom.replace(' ',"'")
    if flag_dash: nom = nom.replace(' ',"-")
    return nom

    
def add_premier_dernier_auteur_colonnes(article_df:pd.DataFrame,auth_df:pd.DataFrame)->pd.DataFrame:

    """
    Function `add_premier_dernier_auteur_colonnes` adds the for columns : 'Is premier auteur inst',
    'Is dernier auteur inst', 'Dernier auteur', 'Premier auteur' to the dataframe `article_df` using the
    dataframe `auth_df`.
    """
    
    check_is_premier_auteur_list = []
    check_is_dernier_auteur_list = []
    last_author_list = []
    first_author_list = []
    for pub_id in article_df['Pub_id']:
        
        dg = auth_df.query('Pub_id==@pub_id') # & Auteur_id==0')
        dg.reset_index(drop=True, inplace=True)
        first_author_list.append(dg.loc[0,'Premier auteur'])
        check_is_premier_auteur_list.append(dg.loc[0,'Status premier auteur'])
        
        check_last_author = dg.loc[len(dg)-1,'Status dernier auteur']
        check_is_dernier_auteur_list.append(check_last_author)
        last_author_list.append(dg.loc[len(dg)-1,'Employee_full_name'])
        
    article_df['Is premier auteur inst'] = check_is_premier_auteur_list
    article_df['Is dernier auteur inst'] = check_is_dernier_auteur_list
    article_df['Dernier auteur'] = last_author_list
    article_df['Premier auteur'] = first_author_list
    
    return article_df       


def reverse_nom_prenom(row:str,col_name:str)->str:
    
    """
    Function `reverse_nom_prenom` reverse the name and surname : Doe John --> John Doe
    """
    
    first_author = row[col_name]
    if first_author:
        first_author = normalize_nom_prenom(first_author)
        return first_author
    return ''


def extract_doctorants(row:str, inst:str)->str:
    
    """
    Function `extract_doctorants` extact the list of names and surnames of the PhD 
    from a string "<surname1, name1>(stuff1);surname2, name2>(stuff2) ...". The surname and name
    are those of a PhD iff stuff<i> contains "(<d+>,Doc>". Then `extract_doctorants builds a
    string N1. Surname1, N2. Surname2, ... with all the PhD normalized names and surnames.
    """ 

    label_column = 'Liste ordonnée des auteurs ' + inst.capitalize()
    item = row[label_column]
    doctorants_list = []
    for author in item.split(';'):
        if re.findall(r'\((\d+,)?Doc', author):
            doctorant = re.sub(r'\([\w\d,]*\)', '', author).strip()
            nom = normalize_nom(doctorant.split(',')[0].strip())
            prenom = doctorant.split(',')[1].strip()
            prenom_initiale = '-'.join([chunck[0].upper() for chunck in prenom.split('-')])+'.'
            doctorant =  f'{prenom_initiale} {nom}'
            doctorants_list.append(doctorant)
    doctorants = ', '.join(doctorants_list)
    
    return doctorants


def read_and_format(type_publi:str, inst:str, bm_path:pathlib.Path,year:int,datatype:str)->pd.DataFrame:
    
    """
    Function `read_and_format` read the Excel file "Liste consolidée 2023_Articles & Proceedings.xlsx" 
    or "Liste consolidée 2023_Books & Editorials.xlsx" as a dataframe and adds the column "liste doctorants",
    "Premier auteur inst" (boolan True if the first author of the article is part of the institute/department),
    "Dernier auteur inst" (boolan True if the last author of the article is part of the institute/department)
    Modifiy the columns "Premier auteur"
    """
    
    auth_path = get_filename_analyseparauteurs(bm_path,year,datatype)
    auth_df = pd.read_excel(auth_path)
    auth_df = auth_df.rename(columns={"Nombre d'auteurs": 'Nb_auth',})
    auth_df['Premier auteur'] = auth_df['Premier auteur'].replace(r'\s+-\s+','-',regex=True)
    auth_df['Employee_full_name'] = auth_df['Employee_full_name'].replace(r'\s+-\s+','-',regex=True)
    auth_df['Co_auteur Liten'] = auth_df['Co_auteur Liten'].replace(r'\s+-\s+','-',regex=True)
    auth_df['Premier auteur'] = auth_df.apply(dicriminate_nom_prenom,col_name='Premier auteur',axis=1)
    auth_df['Employee_full_name'] = auth_df.apply(dicriminate_nom_prenom,col_name='Employee_full_name',axis=1)

    if type_publi == "article":
        file = get_filename_listeconsolideepubli(bm_path,year,datatype)
    elif type_publi == "book":
        file = get_filename_listeconsolideebook(bm_path,year,datatype)
    else:
        pass
        
    df = pd.read_excel(file)
    df = add_premier_dernier_auteur_colonnes(df,auth_df)
    df['liste doctorants'] = df.apply(extract_doctorants,args=(inst,),axis=1)
    df['Premier auteur'] = df.apply(reverse_nom_prenom,col_name='Premier auteur',axis=1)
    df['Dernier auteur'] = df.apply(reverse_nom_prenom,col_name='Dernier auteur',axis=1)
    # Suppreesion of the markdown used to format in the title (ex : subscipt)
    df['Titre'] = df['Titre'].replace(r'<[\w/]+>','',regex=True)
    return df

def builds_dep_dict(publi_df:pd.DataFrame, inst:str)->dict:

    """
    The function `builds_dep_dic` builds a dict of list of dicts as: 
    {<dep_name>:[{"Pub_id":<pub_id1>,...,"DOI":<doi1>},{"Pub_id":<pub_id2>,...,"DOI":<doi2>}...],...}
    """
    
    inst_publi_dict = {}
        
    departements_list = get_departements_list(bm_path, inst)
    for dep in departements_list:
        dg = publi_df.query(f"`{dep}` == 1")
        dep_publi_list_dict = []
        for idx,row in enumerate(dg.iterrows()):
            dep_publi_list_dict.append(row[1].to_dict() | dict(index=idx+1))
        
        inst_publi_dict[dep] = dep_publi_list_dict
        
    return inst_publi_dict
    
def builds_inst_list(publi_df:pd.DataFrame, inst:str)->list:

    """
    The function `builds_inst_list` builds a list of dicts as: 
    [{"Pub_id":<pub_id1>,...,"DOI":<doi1>},{"Pub_id":<pub_id2>,...,"DOI":<doi2>}...]
    """
    
    inst_publi_list_dict = []
   
    for idx, row in enumerate(publi_df.iterrows()):
        inst_publi_list_dict.append(row[1].to_dict() | dict(index=idx+1))
        
    return inst_publi_list_dict
    
def make_document(bm_path:pathlib.Path, file_template:pathlib.Path, year:int, inst:str, datatype:str,perimeter:str)->None:
    
    """
    Function `make_document` builds the bibliograpy as a Word document fir the corpus
    of year `year`, the institute ìnst`and the data base `datatype`. A Word template is use
    see the docxtpl :   https://docxtpl.readthedocs.io/en/latest/  for usage.
    """
    
    publi_df = read_and_format("article", inst, bm_path,year,datatype)
    book_df = read_and_format("book", inst, bm_path,year,datatype)
    
    doc = DocxTemplate(file_template)
    
    # Builds the master dict and list
    inst_publi_list_dict = builds_inst_list(publi_df, inst)
    inst_book_list_dict = builds_inst_list(book_df, inst)
    inst_publi_dict = builds_dep_dict(publi_df, inst)
    inst_book_dict = builds_dep_dict(book_df, inst)
    
    context = {
               "year" : year,
               "perimeter" : perimeter,
               "institut":inst,
               "publi_list" : inst_publi_dict,
               "book_list" : inst_book_dict,
               "inst_publi_list" : inst_publi_list_dict,
               "inst_book_list" : inst_book_list_dict,
               "deps":list(inst_publi_dict.keys()),
              }

    # Render the template with the context
    doc.render(context)
    
    # Save the populated document
    file_article = get_filename_listeconsolideepubli(bm_path,year,datatype)
    file_output = Path(file_article).parents[0] / f'biblio_{inst}_{str(year)}_{perimeter}.docx'
    doc.save(file_output)

def master_make_document(bm_path:pathlib.Path, year:int, inst:str, datatype:str, perimeter:str="all")->None:
    # Load the template
    if perimeter=="inst":
        file_template = r"c:\users\franc\Temp\template_inst.docx"
        make_document(bm_path, file_template, year, inst, datatype, perimeter)
       
    elif perimeter=="all":
        file_template = r"c:\users\franc\Temp\template_all.docx"
        make_document(bm_path, file_template, year, inst, datatype, perimeter)
        
    elif perimeter=="departement":
        file_template = r"c:\users\franc\Temp\template_departement.docx"
        departements_list = get_departements_list(bm_path, inst)
        for departement in departements_list:
            make_document(bm_path, file_template, year, inst, datatype, departement)
