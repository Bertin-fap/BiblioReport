__all_ = ['CLOUD_BCKG',
          'CLOUD_HEIGHT',
		  'CLOUD_WIDTH',
		  'CLOUD_MAX_WORDS',
		  'CLOUD_MAX_WORDS_LENGTH',
		  'BAR_Y_LABEL_MAX',
          'BAR_X_RANGE',
		  'BAR_Y_MAX',
		  'BAR_WIDTH',
		  'BAR_HEIGHT',
		  'BAR_HEIGHT_RATIO',
		  'BAR_COLOR_RANGE',
		  'BAR_COLOR_SCALE'
		  'DIC_CODE_COUNTRIES',
          'DIC_COUNTRIES_CONTINENT',
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
BAR_HEIGHT       = 1600
BAR_HEIGHT_RATIO = 1.7
BAR_COLOR_RANGE  = [0,30]     # IFs
BAR_COLOR_SCALE  = px.colors.sequential.Rainbow

# Parameters of countries plot

DIC_CODE_COUNTRIES = bp.COUNTRIES_CODES
DIC_COUNTRIES_CONTINENT = bp.COUNTRIES_CONTINENT