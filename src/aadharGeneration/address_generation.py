import pandas as pd
import tqdm
from ensure import ensure_annotations
from constants import config
from pathlib import Path

@ensure_annotations
def address_generation(num: int=10):
    '''

    This is for address genration from csv file which was obtained from kaggle dataset
    :param num: these many number of times diffrent addres has to be generated

    '''
    addr = pd.read_csv(Path(f'{config.data_path}/input_address.csv'))
    addr['len'] = addr['add'].str.split(',').apply(len)

    addr1 = []
    addr2 = []
    addr3 = []
    addr4 = []
    addr5 = []

    for i in tqdm.tqdm(range(num), total=num, unit='Image'):
        add1 = ''
        add2 = ''
        add3 = ''
        add4 = ''
        add5 = ''
        temp = addr['add'][i].split(',')
        for i in range(len(temp)):
            if i in (0, 1):
                add1 += ','
                add1 += temp[i].strip()
            elif i in (2, 3):
                add2 += ','
                add2 += temp[i].strip()
            elif i in (4, 5):
                add3 += ','
                add3 += temp[i].strip()
            elif i in (6, 7):
                add4 += ','
                add4 += temp[i].strip()
            else:
                add5 += ','
                add5 += temp[i].strip()
        addr1.append(add1[1:])
        addr2.append(add2[1:])
        addr3.append(add3[1:])
        addr4.append(add4[1:])
        addr5.append(add5[1:-1])

    pd.DataFrame(
        {'Address1': addr1, 'Address2': addr2, 'Address3': addr3, 'Address4': addr4, 'Address5': addr5}).to_csv(Path(f'{config.data_path}/address.csv'))
