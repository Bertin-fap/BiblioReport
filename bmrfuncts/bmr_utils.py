import os
import re
from collections import namedtuple



def parse_kw_filename(input_path,extension='.png'):
    

    kw_tup = namedtuple('kw_tup',['dep' , 'year', 'kw'])
    
    dep_list = []
    year_list = []
    kw_list = []
    
    pattern = re.compile('(?P<kw>^\w*\s)(?P<year>\d{4})-(?P<dep>\w*)\.')
    for file in [x for x in os.listdir(input_path) if x.endswith(extension)]:
        match = pattern.match(file)
        if match:
            dep_list.append(match.group('dep'))
            year_list.append(match.group('year'))
            kw_list.append(match.group('kw'))

    kw = kw_tup (list(set(dep_list)), list(set(year_list)),  list(set(kw_list)))
    
    return kw