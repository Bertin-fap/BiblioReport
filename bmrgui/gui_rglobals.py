"""The `guir_globals` module  defines the global parameters useful for the GUI settings.
"""

__all__ = ['PAGES_LABELS',
           'APPLICATION_WINDOW_TITLE',
           'TEXT_KW_ANALYSIS',
           'TEXT_KW',
           'TEXT_GEOPLOT',
           'BUTT_GEOPLOT',
           'TEXT_WORDCLOUD',
           'TEXT_IFPLOT',
           'TEXT_MODE',
           'TEXT_IF_ANALYSIS',]

PAGES_LABELS = dict(Word="Bibliographie Word",
                    Plots="KPI plots")
APPLICATION_WINDOW_TITLE = "BiblioReport Création de documents et de graphes"
TEXT_YEAR_PI = "Sélection de(s) année(s)"

TEXT_KW_ANALYSIS = "Plot KW"
TEXT_DEPT = "Département ?"
TEXT_KW = "Mot clé ?"
TEXT_GEOPLOT = "Analyse géographique des collaborations"
BUTT_GEOPLOT = "Lancer le tracé"
TEXT_WORDCLOUD = "Tracé des nuages de mots des mots-clés"
TEXT_IFPLOT = "Tracé des Facteurs d'Impacts du corpus bibliographique"
TEXT_MODE = "Type fichier ?"
TEXT_IF_ANALYSIS = "Lancer le tracé"