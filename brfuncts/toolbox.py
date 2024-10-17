__all__ = ["get_departements_list",
         "get_filename_listeconsolideepubli",
         "get_filename_listeconsolideebook",]
         
from pathlib import Path
import json
        
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
 