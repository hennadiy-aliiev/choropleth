from flask import Flask, render_template
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'world_bank'
mongo = PyMongo(app)


@app.route('/')
def index():
    
    total_sum = mongo.db.code.aggregate( [
        { '$group' : { '_id' : { 'countrycode': '$countrycode'}, 'totalSum': { '$sum': '$lendprojectcost'}}}
    ] )
    countries_invest = [[item['_id']['countrycode'], item['totalSum']] for item in total_sum]

    projects = mongo.db.code.find( {}, { '_id': 0, 'countrycode': 1, 'project_name': 1, 'lendprojectcost': 1 } )
    countries_projects = {}
    # sorting projects; one country has many projects; example: {'UA':[[project_name1:lendprojectcost1],[project_name2:lendprojectcost2]]...}
    for project in projects:
        if project['countrycode'] in countries_projects.keys():
            countries_projects[project['countrycode']].append([project['project_name'], project['lendprojectcost']])
        else:
            countries_projects[project['countrycode']] = [[project['project_name'], project['lendprojectcost']]]

    # adding all projects to a country accordingly; example: ['UA', 573500000, [[project_name1:lendprojectcost1],[project_name2:lendprojectcost2]]...]
    for i in range(len(countries_invest)):
        countries_invest[i].append(countries_projects[countries_invest[i][0]])
    
    
    iso_alpha_2to3 = {"BD": "BGD", "BE": "BEL", "BF": "BFA", "BG": "BGR", "BA": "BIH", 
                    "BB": "BRB", "WF": "WLF", "BL": "BLM", "BM": "BMU", "BN": "BRN", 
                    "BO": "BOL", "BH": "BHR", "BI": "BDI", "BJ": "BEN", "BT": "BTN", 
                    "JM": "JAM", "BV": "BVT", "BW": "BWA", "WS": "WSM", "BQ": "BES", 
                    "BR": "BRA", "BS": "BHS", "JE": "JEY", "BY": "BLR", "BZ": "BLZ", 
                    "RU": "RUS", "RW": "RWA", "RS": "SRB", "TL": "TLS", "RE": "REU", 
                    "TM": "TKM", "TJ": "TJK", "RO": "ROU", "TK": "TKL", "GW": "GNB", 
                    "GU": "GUM", "GT": "GTM", "GS": "SGS", "GR": "GRC", "GQ": "GNQ", 
                    "GP": "GLP", "JP": "JPN", "GY": "GUY", "GG": "GGY", "GF": "GUF", 
                    "GE": "GEO", "GD": "GRD", "GB": "GBR", "GA": "GAB", "SV": "SLV", 
                    "GN": "GIN", "GM": "GMB", "GL": "GRL", "GI": "GIB", "GH": "GHA", 
                    "OM": "OMN", "TN": "TUN", "JO": "JOR", "HR": "HRV", "HT": "HTI", 
                    "HU": "HUN", "HK": "HKG", "HN": "HND", "HM": "HMD", "VE": "VEN", 
                    "PR": "PRI", "PS": "PSE", "PW": "PLW", "PT": "PRT", "SJ": "SJM", 
                    "PY": "PRY", "IQ": "IRQ", "PA": "PAN", "PF": "PYF", "PG": "PNG", 
                    "PE": "PER", "PK": "PAK", "PH": "PHL", "PN": "PCN", "PL": "POL", 
                    "PM": "SPM", "ZM": "ZMB", "EH": "ESH", "EE": "EST", "EG": "EGY", 
                    "ZA": "ZAF", "EC": "ECU", "IT": "ITA", "VN": "VNM", "SB": "SLB", 
                    "ET": "ETH", "SO": "SOM", "ZW": "ZWE", "SA": "SAU", "ES": "ESP", 
                    "ER": "ERI", "ME": "MNE", "MD": "MDA", "MG": "MDG", "MF": "MAF", 
                    "MA": "MAR", "MC": "MCO", "UZ": "UZB", "MM": "MMR", "ML": "MLI", 
                    "MO": "MAC", "MN": "MNG", "MH": "MHL", "MK": "MKD", "MU": "MUS", 
                    "MT": "MLT", "MW": "MWI", "MV": "MDV", "MQ": "MTQ", "MP": "MNP", 
                    "MS": "MSR", "MR": "MRT", "IM": "IMN", "UG": "UGA", "TZ": "TZA", 
                    "MY": "MYS", "MX": "MEX", "IL": "ISR", "FR": "FRA", "IO": "IOT", 
                    "SH": "SHN", "FI": "FIN", "FJ": "FJI", "FK": "FLK", "FM": "FSM", 
                    "FO": "FRO", "NI": "NIC", "NL": "NLD", "NO": "NOR", "NA": "NAM", 
                    "VU": "VUT", "NC": "NCL", "NE": "NER", "NF": "NFK", "NG": "NGA", 
                    "NZ": "NZL", "NP": "NPL", "NR": "NRU", "NU": "NIU", "CK": "COK", 
                    "XK": "XKX", "CI": "CIV", "CH": "CHE", "CO": "COL", "CN": "CHN", 
                    "CM": "CMR", "CL": "CHL", "CC": "CCK", "CA": "CAN", "CG": "COG", 
                    "CF": "CAF", "CD": "COD", "CZ": "CZE", "CY": "CYP", "CX": "CXR", 
                    "CR": "CRI", "CW": "CUW", "CV": "CPV", "CU": "CUB", "SZ": "SWZ", 
                    "SY": "SYR", "SX": "SXM", "KG": "KGZ", "KE": "KEN", "SS": "SSD", 
                    "SR": "SUR", "KI": "KIR", "KH": "KHM", "KN": "KNA", "KM": "COM", 
                    "ST": "STP", "SK": "SVK", "KR": "KOR", "SI": "SVN", "KP": "PRK", 
                    "KW": "KWT", "SN": "SEN", "SM": "SMR", "SL": "SLE", "SC": "SYC", 
                    "KZ": "KAZ", "KY": "CYM", "SG": "SGP", "SE": "SWE", "SD": "SDN", 
                    "DO": "DOM", "DM": "DMA", "DJ": "DJI", "DK": "DNK", "VG": "VGB", 
                    "DE": "DEU", "YE": "YEM", "DZ": "DZA", "US": "USA", "UY": "URY", 
                    "YT": "MYT", "UM": "UMI", "LB": "LBN", "LC": "LCA", "LA": "LAO", 
                    "TV": "TUV", "TW": "TWN", "TT": "TTO", "TR": "TUR", "LK": "LKA", 
                    "LI": "LIE", "LV": "LVA", "TO": "TON", "LT": "LTU", "LU": "LUX", 
                    "LR": "LBR", "LS": "LSO", "TH": "THA", "TF": "ATF", "TG": "TGO", 
                    "TD": "TCD", "TC": "TCA", "LY": "LBY", "VA": "VAT", "VC": "VCT", 
                    "AE": "ARE", "AD": "AND", "AG": "ATG", "AF": "AFG", "AI": "AIA", 
                    "VI": "VIR", "IS": "ISL", "IR": "IRN", "AM": "ARM", "AL": "ALB", 
                    "AO": "AGO", "AQ": "ATA", "AS": "ASM", "AR": "ARG", "AU": "AUS", 
                    "AT": "AUT", "AW": "ABW", "IN": "IND", "AX": "ALA", "AZ": "AZE", 
                    "IE": "IRL", "ID": "IDN", "UA": "UKR", "QA": "QAT", "MZ": "MOZ"}

    # converting 'iso alpha 2' to 'iso alpha 3' format
    for i in range(len(countries_invest)):
        if countries_invest[i][0] in iso_alpha_2to3.keys():
            countries_invest[i][0] = iso_alpha_2to3[countries_invest[i][0]]
    
    return render_template('index.html', title='Home', countries_invest=countries_invest)


if __name__ == '__main__':

    app.run(debug=True)