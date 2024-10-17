__all__ = ['make_document']
import re
from pathlib import Path

import pandas as pd
from difflib import SequenceMatcher
from docxtpl import DocxTemplate

# Local imports
from brfuncts.toolbox import  get_filename_listeconsolideepubli 
from brfuncts.toolbox import  get_filename_listeconsolideebook
from brfuncts.toolbox import  get_departements_list

join_prenom = lambda x:''.join([y[0].upper() for y in x.split()])

def capitalize_nom(nom):
    
    """
    Function `capitalize_nom` capitalize name taking care of composite name
    """
    flag_apostrophe = True if "'" in nom else False
    nom = ' '.join([x.capitalize() for x in re.split(r"[\s\-']+", nom)])
    if flag_apostrophe: nom = nom.replace(' ',"'")
    return nom

def is_premier_author_inst(row, inst):
    
    """
    Function `is_premier_author_inst` return the boolean `check`set to Tue if the 
    first author of the article is part of the institute/departement.
    """
    
    label_column = 'Liste ordonnée des auteurs ' + inst.capitalize()
    x = row['Premier auteur']
    y = row[label_column].split(',')
    similarity = SequenceMatcher(None, x, y[0]).ratio()
    
    check = False
    if similarity> 0.6:
        check = True

    return check

def supress_first_author_from_list(row, inst):
    
    """
    Function `is_premier_author_inst` return the boolean `check`set to Tue if the 
    first author of the article is part of the institute/departement.
    """
    
    label_column = 'Liste ordonnée des auteurs ' + inst.capitalize()
    list_author = row[label_column]
    if  row['Premier auteur inst']:
        list_author = ', '.join(list_author.split(',')[1:])
    return list_author
        

def reverse_nom_prenom(row):
    
    """
    Function `reverse_nom_prenom` reverse the name and surname : Doe John --> John Doe
    """
    first_author = row['Premier auteur']
    first_author =  first_author.split()[1] + ' ' + first_author.split()[0]
    return first_author
    
def extact_nom_prenom(row,inst):
    
    """
    From a string formatted as "<surname1, name1>(stuff1);surname2, name2>(stuff2), ..."
    the function` builds a new string formatted as "n1 surname1, N2 surname2,..." whewere n1, n2,.. stand
    for the names initials.
    """    
    
    label_column = 'Liste ordonnée des auteurs ' + inst.capitalize()
    authors_list = row[label_column]
    nom_prenom_list = re.sub(r'\([\w,]*\)', '', authors_list).split(';')
    authors_list = ', '.join([join_prenom(x.split(',')[1].strip())+' '+
                              capitalize_nom(x.split(',')[0].strip())
                              for x in nom_prenom_list])+', '
    return authors_list

def extract_doctorants(row, inst):
    
    """
    Function `extract_doctorants` extact the list of names and surnames of the PhD 
    from a string "<surname1, name1>(stuff1);surname2, name2>(stuff2) ...". The surname and name
    are those of a PhD iff stuff1 contains "(<d+>,Doc>".
    """ 

    label_column = 'Liste ordonnée des auteurs ' + inst.capitalize()
    item = row[label_column]
    doctorants = []
    for author in item.split(';'):
        if re.findall(r'\((\d+,)?Doc', author):
            author = re.sub(r'\([\w\d,]*\)', '', author).strip()
            nom = capitalize_nom(author.split(',')[0].strip())
            prenom_initiale = author.split(',')[1].strip()[0]
            author =  f'{prenom_initiale} {nom}'
            doctorants.append(author)
    doctorants = ', '.join(doctorants)
    
    return doctorants


def read_and_format(file, inst):
    
    """
    Function `read_and_format` read the Excel file "Liste consolidée 2023_Articles & Proceedings.xlsx" 
    or "Liste consolidée 2023_Books & Editorials.xlsx" as a dataframe and adds the column "liste doctorants",
    "Premier auteur inst" (boolan True if the first author of the article is part of the institute/department).
    Modifiy the columns "Premier auteur"
    """

    df = pd.read_excel(file)
    label_column = 'Liste ordonnée des auteurs ' + inst.capitalize()
    df['liste doctorants'] = df.apply(extract_doctorants,args=(inst,),axis=1)
    df[label_column] = df.apply(extact_nom_prenom, args=(inst,),axis=1)
    df['Premier auteur inst'] = df.apply(reverse_nom_prenom,axis=1)
    df['Premier auteur'] = df.apply(reverse_nom_prenom,axis=1)
    df['Premier auteur inst'] = df.apply(is_premier_author_inst,args=(inst,),axis=1)
    #df[label_column] = df.apply(supress_first_author_from_list,args=(inst,),axis=1)

    return df

def make_document(bm_path, file_template, year, inst, datatype):
    
    """
    Function `make_document` builds the bibliograpy as a Word document fir the corpus
    of year `year`, the institute ìnst`and the data base `datatype`. A Word template is use
    see the docxtpl :   https://docxtpl.readthedocs.io/en/latest/  for usage.
    """
    
    file_article = get_filename_listeconsolideepubli(bm_path,year,datatype)
    publi_df = read_and_format(file_article, inst)
    file_book = get_filename_listeconsolideebook(bm_path,year,datatype)
    book_df = read_and_format(file_book, inst)
    
    # Load the template
    doc = DocxTemplate(file_template)
    
    # Define the list of publications
    inst_publi_dict = {}
    inst_book_dict = {}
    inst_tot_publi_dict = {}
    inst_tot_book_dict = {}
    
    inst_publi_list_dict = []
    inst_book_list_dict = []
    for idx, row in enumerate(publi_df.iterrows()):
        inst_publi_list_dict.append(row[1].to_dict() | dict(index=idx+1))
    for idx,row in enumerate(book_df.iterrows()):
        inst_book_list_dict.append(row[1].to_dict() | dict(index=idx+1))
        
    departements_list = get_departements_list(bm_path, inst)
    for dep in departements_list:
        dg = publi_df.query(f"`{dep}` == 1")
        dh = book_df.query(f"`{dep}` == 1")
        dep_publi_list_dict = []
        dep_book_list_dict = []
        for idx,row in enumerate(dg.iterrows()):
            dep_publi_list_dict.append(row[1].to_dict() | dict(index=idx+1))
        for idx, row in enumerate(dh.iterrows()):
            dep_book_list_dict.append(row[1].to_dict() | dict(index=idx+1))
        
        inst_publi_dict[dep] = dep_publi_list_dict
        inst_book_dict[dep] = dep_book_list_dict
    
    context = {
        "year" : year,
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
    file_output = Path(file_article).parents[0] / f'biblio_{inst}_{str(year)}.docx'
    print(f'document saved in {file_output}')
    doc.save(file_output)