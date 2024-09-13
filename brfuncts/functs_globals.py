__all_ = ['CLOUD_BCKG',
          'CLOUD_HEIGHT',
		  'CLOUD_WIDTH',
		  'CLOUD_MAX_WORDS',
		  'CLOUD_MAX_WORDS_LENGTH',
          'COOC_AUTHORIZED_ITEMS',
          'COOC_AUTHORIZED_ITEMS_DICT',
          'COOC_HTML_PARAM',
          'COUNTRIES_GPS',
          'COUPL_AUTHORIZED_ITEMS',
		  'BAR_Y_LABEL_MAX',
          'BAR_X_RANGE',
		  'BAR_Y_MAX',
		  'BAR_WIDTH',
		  'BAR_HEIGHT',
		  'BAR_HEIGHT_RATIO',
		  'BAR_COLOR_RANGE',
		  'BAR_COLOR_SCALE'
		  'COUNTRIES_CODES_DICT',
          'COUNTRIES_CONTINENT_DICT',
          'NODE_SIZE_REF',
          'SIZE_MIN',
          'UNKNOWN'
		  ]
          
# Standard library imports
import plotly.express as px
import BiblioParsing.BiblioGeneralGlobals as bp

# Parameters of cloud representation
CLOUD_BCKG             = 'ivory'
CLOUD_HEIGHT           = 600
CLOUD_WIDTH            = 400
CLOUD_MAX_WORDS        = 100
CLOUD_MAX_WORDS_LENGTH = 60

# Parameters of bar chart representation
BAR_Y_LABEL_MAX  = 35          # Nb of characters
BAR_X_RANGE      = [0,10]      # Nb of articles
BAR_Y_MAX        = 60          # Nb journals (max per barchart plot)
BAR_WIDTH        = 800
BAR_HEIGHT       = 557
BAR_HEIGHT_RATIO = 1.7
BAR_COLOR_RANGE  = [0,30]     # IFs
BAR_COLOR_SCALE  = px.colors.sequential.Rainbow

# Parameters of countries plot

COUNTRIES_CODES_DICT = bp.COUNTRIES_CODES
COUNTRIES_CONTINENT_DICT = bp.COUNTRIES_CONTINENT
COUNTRIES_GPS = bp.COUNTRIES_GPS
UNKNOWN = 'unknown'

# Parameters of graph construction and  plot
COOC_HTML_PARAM = {'algo'      : 'barnes',
                   'height'    : 1000,
                   'width'     : 1000,
                   'bgcolor'   : '#9E9E9E', #     '#EAEDED',
                   'font_color': 'black',
                  }
LABEL_MEANING = {'AU':'Authors',              # ex: Nom1 J, Nom2 E, Nom3 J-P
                 'CU':'Countries',            # ex: France, United States
                 'I' :'Institutions',         # ex: Acronyme1, Acronyme2
                 'DT':'Document types',       # ex: Review, Article, Proceeding
                 'J' :'Journals',          
                 'AK':'Authors keywords',     # ex: BIOMASS, SOLAR FUEL
                 'IK':'Journal keywords',
                 'TK':'Title keywords',
                 'S' :'Subjects',             # ex: Chemical Engineering,Engineering 
                 'S2':'Sub-subjects',         # ex: Applied Mathematics, Organic Chemistry     
                 'R' :'References',
                 'RJ':'References journals',
                 'LA':'Languages',            # ex: English, French
                 'Y' :'Years',                # ex: 2019
                }
COOC_AUTHORIZED_ITEMS = ['AU','CU','AK','IK','TK','S','S2']
COOC_AUTHORIZED_ITEMS_DICT = {label:name for name,label in LABEL_MEANING.items() 
                              if name in COOC_AUTHORIZED_ITEMS}
NODE_SIZE_REF = 30
SIZE_MIN = 1 # Minimum size of co-occurrence nodes