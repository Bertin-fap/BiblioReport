__all__ = ['make_document']
import re

import pandas as pd
from difflib import SequenceMatcher
from docxtpl import DocxTemplate


join_prenom = lambda x:''.join([y[0].upper() for y in x.split()])
#capitalize_nom = lambda x : ' '.join([y.capitalize() for y in x.split()])

def capitalize_nom(nom):
    flag_apostrophe = True if "'" in nom else False
    nom = ' '.join([x.capitalize() for x in re.split(r"[\s\-']+", nom)])
    if flag_apostrophe: nom = nom.replace(' ',"'")
    return nom

def is_premier_author_inst(row):
    x = row['Premier auteur']
    y = row['Liste ordonnée des auteurs Liten'].split(',')
    similarity = SequenceMatcher(None, x, y[0]).ratio()
    
    check = False
    if similarity> 0.6:
        check = True

    return check

def supress_first_author_from_list(row):
    list_author = row['Liste ordonnée des auteurs Liten']
    if  row['Premier auteur inst']:
        list_author = ', '.join(list_author.split(',')[1:])
    return list_author
        

def reverse_nom_prenom(row):
    first_author = row['Premier auteur']
    first_author =  first_author.split()[1] + ' ' + first_author.split()[0]
    return first_author
    
def extact_nom_prenom(row):
    authors_list = row['Liste ordonnée des auteurs Liten']
    nom_prenom_list = re.sub(r'\([\w,]*\)', '', authors_list).split(';')
    authors_list = ', '.join([join_prenom(x.split(',')[1].strip())+' '+
                              capitalize_nom(x.split(',')[0].strip())
                              for x in nom_prenom_list])+', '
    return authors_list

def extract_doctorants(row):

    item = row['Liste ordonnée des auteurs Liten']
    doctorants = []
    for author in item.split(';'):
        if '(Doc,' in author:
            author = re.sub(r'\([\w,]*\)', '', author).strip()
            nom = capitalize_nom(author.split(',')[0].strip())
            prenom_initiale = author.split(',')[1].strip()[0]
            author =  f'{prenom_initiale} {nom}'
            doctorants.append(author)
    doctorants = ', '.join(doctorants)
    return doctorants


def read_and_format(file):

    df = pd.read_excel(file)
    
    df['liste doctorants'] = df.apply(extract_doctorants,axis=1)
    df['Liste ordonnée des auteurs Liten'] = df.apply(extact_nom_prenom,axis=1)
    df['Premier auteur inst'] = df.apply(reverse_nom_prenom,axis=1)
    df['Premier auteur'] = df.apply(reverse_nom_prenom,axis=1)
    df['Premier auteur inst'] = df.apply(is_premier_author_inst,axis=1)
    df['Liste ordonnée des auteurs Liten'] = df.apply(supress_first_author_from_list,axis=1)

    return df

def make_document(file_article, file_book, file_template, file_output, year, inst):
    
    publi_df = read_and_format(file_article)
    book_df = read_and_format(file_book)
    
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
    
    for dep in ['DEHT','DTCH','DTNM','DTS','DIR']:
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
    doc.save(file_output)