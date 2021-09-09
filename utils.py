import json
import re
import pandas as pd
import requests

class Config:
    def __init__(self):
        with open('config.json') as f:
            self.config = json.load(f)

    @staticmethod
    def write_config_example():
        """
        Write config_example.json file for easy creation config.json
        :return:
        """
        ru_funds = {'seb': {'description': 'SEB Russia Fund', 'type': 'csv',
                             'url': 'http://seb.se/pow/fmk/2500/csv/SEB_Russia_Fund_52990077SLDTU8UMXF91.csv'},
                    'franklin': {'description': 'Franklin FTSE Russia ETF', 'type': 'xls',
                                'url': 'https://www.franklintempleton.com/investor/investments-and-solutions'
                                       '/investment-options/etfs/portfolio/26356/franklin-ftse-russia-etf/FLRU?gwbid'
                                       '=gw.portfolio'},
                    'msci': {'description': 'MSCI Russia', 'type': 'xls',
                    'url': 'https://app2.msci.com/eqb/custom_indexes/russia_performance.xls'}}

        ru_holdings = {'SBER.ME': 'Sberbank of Russia',
                       'GAZP.ME': 'Gazprom',
                       'SBERP.ME': 'Sberbank of Russia (Preferred)',
                       'LKOH.ME': 'Lukoil',
                       'GMKN.ME': 'MMC "NORILSK NICKEL',
                       'YNDX.ME': 'Yandex',
                        'NVTK.ME': 'Novatek',
                       'TATN.ME': 'TATNEFT',
                       'TATNP.ME': 'TATNEFT (Preferred)',
                       'ROSN.ME': 'Rosneft',
                       'SNGS.ME': 'Surgutneftegas',
                       'SNGSP.ME': 'Surgutneftegas (Preferred)',
                        'MGNT.ME': 'Magnit',
                       'FIVE.ME': 'X5 Retail Group N.V.',
                       'MTSS.ME': 'Mobile TeleSystems',
                       'POLY.ME': 'Polymetal International plc',
                       'ALRS.ME': 'Alrosa',
                       'CHMF.ME': 'Severstal',
                       'PLZL.ME': 'Polyus',
                       'IRAO.ME': 'Inter RAO',
                       'NLMK.ME': 'NLMK',
                       'VTBR.ME': 'VTB Bank',
                       'MOEX.ME': 'Moscow Exchange',
                       'PHOR.ME': 'PhosAgro',
                        'TRNFP.ME': 'Transneft (Preferred)',
                       'MAGN.ME': 'Magnitogorsk Iron & Steel Works',
                       'RTKM.ME': 'Rostelecom',
                       'RUAL.ME': 'Rusal',
                       'AFLT.ME': 'Aeroflot',
                       'PIKK.ME': 'PIK GROUP',
                       'HYDR.ME': 'RusHydro',
                       'FEES.ME': 'Federal Grid Company of Unified Energy System',
                       'AFKS.ME': 'Sistema',
                       'LSRG.ME': 'LSR Group',
                       'CBOM.ME': 'CREDIT BANK OF MOSCOW',
                       'UPRO.ME': 'Unipro',
                       'DSKY.ME': 'Detsky mir',
                       'RNFT.ME': 'RussNeft',
                       'LNTA.ME': 'Lenta',
                       'SFIN.ME': 'SAFMAR Financial investments',
                       'MVID.ME': 'M.video'}
        universe_dict = {'ru': {'description': 'Russian stocks', 'funds': ru_funds, 'holdings': ru_holdings}}

        data = {'provider': 'yahoo',
                'universe': universe_dict}

        with open('config.json', 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)

def fnv64(data):
    hash_ = 0xcbf29ce484222325
    for b in data:
        hash_ *= 0x100000001b3
        hash_ &= 0xffffffffffffffff
        hash_ ^= b
    return hash_

def fast_hash(dn, salt):
    # Turn dn into bytes with a salt, dn is expected to be ascii data
    data = salt.encode("ascii") + dn.encode("ascii")
    return fnv64(data)

def r_(float):
    return round(float, 2)

def is_isin_code(isisin):
    pattern = re.compile("([A-Z]{2})((?![A-Z]{10})[A-Z0-9]{10})")
    return (isinstance(isisin, str) and len(isisin) == 12 and bool(pattern.search(isisin)))

def get_df_from_ExcelFile(file_path):
    '''
    Return DataFrame from first sheet
    '''
    xl_file = pd.ExcelFile(file_path)
    return [xl_file.parse(sheet_name) for sheet_name in xl_file.sheet_names][0]

def download(url, filename):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content():
            fd.write(chunk)



