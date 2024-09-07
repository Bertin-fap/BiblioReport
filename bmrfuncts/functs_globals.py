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
		  ]
# Standard library imports
import plotly.express as px

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
