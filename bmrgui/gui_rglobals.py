"""The `guir_globals` module  defines the global parameters useful for the GUI settings.
"""

__all__ = ['ADD_SPACE_MM',
           'CORPUSES_NUMBER',
           'DIC_CODE_COUNTRIES',
           'FONT_NAME',
           'HELP_ETAPE_7',
           'HELP_ETAPE_8',
           'HELP_ETAPE_9',
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
           'TEXT_IFPLOT',
           'TEXT_MODE',
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
HELP_ETAPE_7 = ggr.HELP_ETAPE_7
HELP_ETAPE_8 = ggr.HELP_ETAPE_8
HELP_ETAPE_9 = ggr.HELP_ETAPE_9
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

TEXT_KW_ANALYSIS = "Plot KW"
TEXT_DEPT = "Département ?"
TEXT_KW = "Mot clé ?"
TEXT_GEOPLOT = "Analyse géographique des collaborations"
BUTT_GEOPLOT = "Lancer le tracé"
TEXT_WORDCLOUD = "Tracé des nuages de mots des mots-clés"
TEXT_IFPLOT = "Tracé des Facteurs d'Impacts du corpus bibliographique"
TEXT_MODE = "Type fichier ?"
TEXT_IF_ANALYSIS = "Lancer le tracé"

COUNTRIES_CODES = '''United States:USA,Afghanistan:AFG,Albania:ALB,Algeria:DZA,American Samoa:ASM,Andorra:AND,
Angola:AGO,Anguilla:AIA,Antarctica:ATA,Antigua And Barbuda:ATG,Argentina:ARG,Armenia:ARM,Aruba:ABW,
Australia:AUS,Austria:AUT,Azerbaijan:AZE,Bahamas:BHS,Bahrain:BHR,Bangladesh:BGD,Barbados:BRB,
Belarus:BLR,Belgium:BEL,Belize:BLZ,Benin:BEN,Bermuda:BMU,Bhutan:BTN,Bolivia:BOL,
Bosnia And Herzegowina:BIH,Botswana:BWA,Bouvet Island:BVT,Brazil:BRA,Brunei Darussalam:BRN,
Bulgaria:BGR,Burkina Faso:BFA,Burundi:BDI,Cambodia:KHM,Cameroon:CMR,Canada:CAN,Cape Verde:CPV,
Cayman Islands:CYM,Central African Rep:CAF,Chad:TCD,Chile:CHL,China:CHN,Christmas Island:CXR,
Cocos Islands:CCK,Colombia:COL,Comoros:COM,Congo:COG,Cook Islands:COK,Costa Rica:CRI,
Cote D`ivoire:CIV,Croatia:HRV,Cuba:CUB,Cyprus:CYP,Czech Republic:CZE,Denmark:DNK,Djibouti:DJI,
Dominica:DMA,Dominican Republic:DOM,East Timor:TLS,Ecuador:ECU,Egypt:EGY,El Salvador:SLV,
Equatorial Guinea:GNQ,Eritrea:ERI,Estonia:EST,Ethiopia:ETH,Falkland Islands (Malvinas):FLK,
Faroe Islands:FRO,Fiji:FJI,Finland:FIN,France:FRA,French Guiana:GUF,French Polynesia:PYF,
French S. Territories:ATF,Gabon:GAB,Gambia:GMB,Georgia:GEO,Germany:DEU,Ghana:GHA,Gibraltar:GIB,
Greece:GRC,Greenland:GRL,Grenada:GRD,Guadeloupe:GLP,Guam:GUM,Guatemala:GTM,Guinea:GIN,
Guinea-bissau:GNB,Guyana:GUY,Haiti:HTI,Honduras:HND,Hong Kong:HKG,Hungary:HUN,Iceland:ISL,
India:IND,Indonesia:IDN,Iran:IRN,Iraq:IRQ,Ireland:IRL,Israel:ISR,Italy:ITA,Jamaica:JAM,Japan:JPN,
Jordan:JOR,Kazakhstan:KAZ,Kenya:KEN,Kiribati:KIR,North Korea:PRK,South Korea:KOR,Kuwait:KWT,
Kyrgyzstan:KGZ,Laos:LAO,Latvia:LVA,Lebanon:LBN,Lesotho:LSO,Liberia:LBR,Libya:LBY,Liechtenstein:LIE,
Lithuania:LTU,Luxembourg:LUX,Madagascar:MDG,Malawi:MWI,Malaysia:MYS,Maldives:MDV,Mali:MLI,
Malta:MLT,Marshall Islands:MHL,Martinique:MTQ,Mauritania:MRT,Mauritius:MUS,Mayotte:MYT,Mexico:MEX,
Monaco:MCO,Mongolia:MNG,Montserrat:MSR,Morocco:MAR,Mozambique:MOZ,Myanmar:MMR,Namibia:NAM,
Nauru:NRU,Nepal:NPL,Netherlands:NLD,New Caledonia:NCL,New Zealand:NZL,Nicaragua:NIC,Niger:NER,
Nigeria:NGA,Niue:NIU,Norfolk Island:NFK,Northern Mariana Islands:MNP,Norway:NOR,Oman:OMN,
Pakistan:PAK,Palau:PLW,Panama:PAN,Papua New Guinea:PNG,Paraguay:PRY,Peru:PER,Philippines:PHL,
Pitcairn:PCN,Poland:POL,Portugal:PRT,Puerto Rico:PRI,Qatar:QAT,Romania:ROU,Russian Federation:RUS,
Rwanda:RWA,Saint Kitts And Nevis:KNA,Saint Lucia:LCA,St Vincent/Grenadines:VCT,Samoa:WSM,
San Marino:SMR,Sao Tome:STP,Saudi Arabia:SAU,Senegal:SEN,Seychelles:SYC,Sierra Leone:SLE,
Singapore:SGP,Slovakia:SVK,Slovenia:SVN,Solomon Islands:SLB,Somalia:SOM,South Africa:ZAF,
Spain:ESP,Sri Lanka:LKA,St. Helena:SHN,St.Pierre:SPM,Sudan:SDN,Suriname:SUR,Swaziland:SWZ,
Sweden:SWE,Switzerland:CHE,Syrian Arab Republic:SYR,Taiwan:TWN,Tajikistan:TJK,Tanzania:TZA,
Thailand:THA,Togo:TGO,Tokelau:TKL,Tonga:TON,Tunisia:TUN,Turkey:TUR,Turkmenistan:TKM,Tuvalu:TUV,
Uganda:UGA,Ukraine:UKR,United Arab Emirates:ARE,United Kingdom:GBR,Uruguay:URY,Uzbekistan:UZB,
Vanuatu:VUT,Vatican City State:VAT,Venezuela:VEN,Viet Nam:VNM,Virgin Islands (British):VGB,
Virgin Islands (U.S.):VIR,Western Sahara:ESH,Yemen:YEM,Zambia:ZMB,Zimbabwe:ZWE'''

DIC_CODE_COUNTRIES = {y.split(':')[0].strip('\n').strip():y.split(':')[1]  for y in COUNTRIES_CODES.split(',')}