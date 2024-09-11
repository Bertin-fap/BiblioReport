"""The `guir_globals` module  defines the global parameters useful for the GUI settings.
"""

__all__ = ['ADD_SPACE_MM',
           'CORPUSES_NUMBER',
           'FONT_NAME',
           'HELP_GEO_PLOT',
           'HELP_IF_PLOT',
           'HELP_KW_PLOT',
           'KW_DICT',
           'PPI',
           'REF_BMF_POS_X_MM',
           'REF_BMF_POS_Y_MM',
           'REF_BUTTON_DY_MM',
           'REF_BUTTON_FONT_SIZE',
           'REF_CORPI_POS_X_MM',
           'REF_CORPI_POS_Y_MM',
           'REF_DATATYPE_POS_X_MM',
           'REF_DATATYPE_POS_Y_MM',
           'REF_ENTRY_NB_CHAR',
           'REF_ETAPE_FONT_SIZE',
           'REF_INST_POS_X_MM',
           'REF_INST_POS_Y_MM',
           'REF_LABEL_DX_Y_MM',
           'REF_LABEL_FONT_SIZE',
           'REF_LABEL_POS_Y_MM',
           'REF_PAGE_TITLE_FONT_SIZE',
           'REF_PAGE_TITLE_POS_Y_MM',
           'REF_SUB_TITLE_FONT_SIZE',
           'REF_YEAR_BUT_POS_X_MM',
           'REF_YEAR_BUT_POS_Y_MM',
           'TEXT_BMF',
           'TEXT_BMF_CHANGE',
           'TEXT_CORPUSES',
           'TEXT_DATATYPE',
           'TEXT_INSTITUTE',
           'PAGES_LABELS',
           'APPLICATION_WINDOW_TITLE',
           'TEXT_KW_ANALYSIS',
           'TEXT_KW',
           'TEXT_GEOPLOT',
           'BUTT_GEOPLOT',
           'TEXT_WORDCLOUD',
           'TEXT_YEAR_KPI',
           'TEXT_IFPLOT',
           'TEXT_IF_ANALYSIS',
           'TEXT_TITLE',]
           
import bmgui.gui_globals as ggr

FONT_NAME = ggr.FONT_NAME
TEXT_DATATYPE = ggr.TEXT_DATATYPE
TEXT_BMF_CHANGE = ggr.TEXT_BMF_CHANGE
TEXT_BMF = ggr.TEXT_BMF
PPI = ggr.PPI
CORPUSES_NUMBER = ggr.CORPUSES_NUMBER
TEXT_CORPUSES = ggr.TEXT_CORPUSES
ADD_SPACE_MM = ggr.ADD_SPACE_MM
REF_BUTTON_FONT_SIZE = ggr.REF_BUTTON_FONT_SIZE
REF_SUB_TITLE_FONT_SIZE = ggr.REF_SUB_TITLE_FONT_SIZE
REF_INST_POS_X_MM = ggr.REF_INST_POS_X_MM
REF_INST_POS_Y_MM = ggr.REF_INST_POS_Y_MM
REF_BMF_POS_X_MM = ggr.REF_BMF_POS_X_MM
REF_BMF_POS_Y_MM = ggr.REF_BMF_POS_Y_MM
REF_BUTTON_DY_MM = ggr.REF_BUTTON_DY_MM
REF_ENTRY_NB_CHAR = ggr.REF_ENTRY_NB_CHAR
REF_CORPI_POS_X_MM = ggr.REF_CORPI_POS_X_MM
REF_CORPI_POS_Y_MM = ggr.REF_CORPI_POS_Y_MM
REF_DATATYPE_POS_X_MM = ggr.REF_DATATYPE_POS_X_MM
REF_DATATYPE_POS_Y_MM = ggr.REF_DATATYPE_POS_Y_MM
TEXT_INSTITUTE = ggr.TEXT_INSTITUTE
REF_ETAPE_FONT_SIZE = ggr.REF_ETAPE_FONT_SIZE
REF_YEAR_BUT_POS_X_MM = ggr.REF_YEAR_BUT_POS_X_MM
REF_YEAR_BUT_POS_Y_MM = ggr.REF_YEAR_BUT_POS_Y_MM
HELP_IF_PLOT = "L'analyse des IFs est effectuée à partir des fichiers Excel générés par BibloMeter"
HELP_GEO_PLOT = "L'analyse géographique des collaborations est effectuée à partir des fichiers Excel générés par BibloMeter"
HELP_KW_PLOT =  "L'analyse des mots cléf est effectuée à partir des fichiers Excel générés par BibloMeter"
REF_PAGE_TITLE_FONT_SIZE = ggr.REF_PAGE_TITLE_FONT_SIZE
REF_PAGE_TITLE_POS_Y_MM = ggr.REF_PAGE_TITLE_POS_Y_MM
TEXT_TITLE = "- BiblioReport -\nInitialisation de l'analyse"
REF_LABEL_FONT_SIZE = ggr.REF_LABEL_FONT_SIZE
REF_LABEL_POS_Y_MM = ggr.REF_LABEL_POS_Y_MM
REF_LABEL_DX_Y_MM = ggr.REF_LABEL_DX_Y_MM


PAGES_LABELS = dict(Word="Bibliographie Word",
                    Plots="KPI plots")
APPLICATION_WINDOW_TITLE = "BiblioReport Création de documents et de graphes"
TEXT_YEAR_PI = "Sélection de(s) année(s)"
TEXT_YEAR_KPI = "Sélection de l'année"

TEXT_KW_ANALYSIS = "Lancer le tracé"
TEXT_DEPT = "Département ?"
TEXT_KW = "Mot clé ?"
TEXT_GEOPLOT = "Analyse géographique des collaborations"
BUTT_GEOPLOT = "Lancer le tracé"
TEXT_WORDCLOUD = "Tracé des nuages de mots des mots-clés"
TEXT_IFPLOT = "Tracé des Facteurs d'Impacts du corpus bibliographique"
TEXT_IF_ANALYSIS = "Lancer le tracé"
KW_DICT = dict(AK = "Authors",
               TK = "Title",
               IK = "Index")
