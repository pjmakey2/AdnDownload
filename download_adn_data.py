import argparse, \
    requests, \
    os, \
    logging, \
    sys

logging.basicConfig(filename='/tmp/adn_data_download.log', encoding='utf-8', level=logging.DEBUG)

URL = 'https://datosabiertos.aduana.gov.py/ddaa/mainctrl/listaArchivos'
GURL = 'https://datosabiertos.aduana.gov.py/all_data'

parser = argparse.ArgumentParser(
            prog='Adn download data',
            description='Get data from the ADN website',
        )

parser.add_argument('--year', type=int, nargs='?')
parser.add_argument('--month', type=str, nargs='?')
parser.add_argument('--output_dir', type=str, nargs='?')

def download_data(url: str, year: int, nmonth:int , output_dir:str):
    logging.info('Calling download_data')
    rsp = requests.get(url)
    ttj = rsp.json()
    try:
        os.mkdir(output_dir)
    except:
        pass
    else:
        logging.info(f'Creating output folder {output_dir}')
    for l in ttj:
        ttyp, tyear, tmonth = l.get('separatePath')
        tyear = int(tyear)
        if l.get('ext') != 'csv': 
            continue
        filename = l.get('fileName')
        if (nmonth == tmonth) and (year == tyear):
            sub_output_dir = f'{output_dir}/{year}/{tmonth}'
            try:
                os.makedirs(sub_output_dir)
            except:
                pass
            else:
                logging.info(f'Creating sub output folder {sub_output_dir}')
            ext = l.get('ext')
            ff = f'{GURL}/{year}/{month}/{filename}.{ext}'
            logging.info(f'Downloading file {ff}')
            data = requests.get(ff)
            fvo = f'{sub_output_dir}/{filename}.{ext}'
            with open(fvo, 'wb') as ff:
                ff.write(data.content)
            logging.info(f'Saving {fvo}')
        
if __name__ == '__main__':
    args = parser.parse_args()
    year = args.year
    month = args.month
    output_dir = args.output_dir
    if not year or not month or not output_dir:
        logging.info('You have to provide all the arguments')
        sys.exit(0)
    logging.info(f"""Passing parameters:
                URL: {URL}
                YEAR:{year}
                MONTH:{month}
                OUTPUT_DIR:{output_dir}""")
    download_data(URL, year, month, output_dir)
        