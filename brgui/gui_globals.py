"""The `guir_globals` module  defines the global parameters useful for the GUI settings.
"""

__all__ = ['ADD_SPACE_MM',
           'CORPUSES_NUMBER',
           'FONT_NAME',
           'HELP_GEO_PLOT',
           'HELP_GRAPH_DEP',
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
           'TEXT_GRAPH_DEP',
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
           'TEXT_TITLE',
           'BUTT_GRAPH_COUNTRIES',]
           
import bmgui.gui_globals as bmgg

FONT_NAME = bmgg.FONT_NAME
TEXT_DATATYPE = bmgg.TEXT_DATATYPE
TEXT_BMF_CHANGE = bmgg.TEXT_BMF_CHANGE
TEXT_BMF = bmgg.TEXT_BMF
PPI = bmgg.PPI
CORPUSES_NUMBER = bmgg.CORPUSES_NUMBER
TEXT_CORPUSES = bmgg.TEXT_CORPUSES
ADD_SPACE_MM = bmgg.ADD_SPACE_MM
REF_BUTTON_FONT_SIZE = bmgg.REF_BUTTON_FONT_SIZE
REF_SUB_TITLE_FONT_SIZE = bmgg.REF_SUB_TITLE_FONT_SIZE
REF_INST_POS_X_MM = bmgg.REF_INST_POS_X_MM
REF_INST_POS_Y_MM = bmgg.REF_INST_POS_Y_MM
REF_BMF_POS_X_MM = bmgg.REF_BMF_POS_X_MM
REF_BMF_POS_Y_MM = bmgg.REF_BMF_POS_Y_MM
REF_BUTTON_DY_MM = bmgg.REF_BUTTON_DY_MM
REF_ENTRY_NB_CHAR = bmgg.REF_ENTRY_NB_CHAR
REF_CORPI_POS_X_MM = bmgg.REF_CORPI_POS_X_MM
REF_CORPI_POS_Y_MM = bmgg.REF_CORPI_POS_Y_MM
REF_DATATYPE_POS_X_MM = bmgg.REF_DATATYPE_POS_X_MM
REF_DATATYPE_POS_Y_MM = bmgg.REF_DATATYPE_POS_Y_MM
TEXT_INSTITUTE = bmgg.TEXT_INSTITUTE
REF_ETAPE_FONT_SIZE = bmgg.REF_ETAPE_FONT_SIZE
REF_YEAR_BUT_POS_X_MM = bmgg.REF_YEAR_BUT_POS_X_MM
REF_YEAR_BUT_POS_Y_MM = bmgg.REF_YEAR_BUT_POS_Y_MM
HELP_IF_PLOT = "L'analyse des IFs est effectuée à partir des fichiers Excel générés par BibloMeter"
HELP_GEO_PLOT = "L'analyse géographique des collaborations est effectuée à partir des fichiers Excel générés par BibloMeter"
HELP_KW_PLOT =  "L'analyse des mots cléf est effectuée à partir des fichiers Excel générés par BibloMeter"
REF_PAGE_TITLE_FONT_SIZE = bmgg.REF_PAGE_TITLE_FONT_SIZE
REF_PAGE_TITLE_POS_Y_MM = bmgg.REF_PAGE_TITLE_POS_Y_MM
TEXT_TITLE = "- BiblioReport -\nInitialisation de l'analyse"
REF_LABEL_FONT_SIZE = bmgg.REF_LABEL_FONT_SIZE
REF_LABEL_POS_Y_MM = bmgg.REF_LABEL_POS_Y_MM
REF_LABEL_DX_Y_MM = bmgg.REF_LABEL_DX_Y_MM


PAGES_LABELS = dict(Word="Bibliographie Word",
                  Plots="KPI plots",
                  Graph="Graph plots",)
APPLICATION_WINDOW_TITLE = "BiblioReport Création de documents et de graphes"
TEXT_YEAR_PI = "Sélection de(s) année(s)"
TEXT_YEAR_KPI = "Sélection de l'année"

TEXT_KW_ANALYSIS = "Lancer le tracé"
TEXT_DEPT = "Département ?"
TEXT_KW = "Mot clé ?"
TEXT_GEOPLOT = "Analyse géographique des collaborations"
BUTT_GEOPLOT = "Tracé mappemonde"
BUTT_GRAPH_COUNTRIES = "Tracé du graph"
TEXT_WORDCLOUD = "Tracé des nuages de mots des mots-clés"
TEXT_IFPLOT = "Tracé des Facteurs d'Impacts du corpus bibliographique"
TEXT_IF_ANALYSIS = "Lancer le tracé"
KW_DICT = dict(AK = "Authors",
               TK = "Title",
               IK = "Index")
TEXT_GRAPH_DEP = "Tracé du graphe des collaborations entre départements"
HELP_GRAPH_DEP = "L'analyse du graphe des collaborations entre départements est effectuée à partir des fichiers Excel générés par BibloMeter"