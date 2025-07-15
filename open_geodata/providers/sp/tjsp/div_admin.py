"""
ssss


"""

import concurrent.futures
import re
import unicodedata
import urllib.request

import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import html
from more_itertools import one
from requests_ip_rotator import ApiGateway

import open_geodata as geo


def keep_numbers(my_string):
    """
    Mantem apenas números
    '987978098098098'
    https://stackoverflow.com/questions/1249388/removing-all-non-numeric-characters-from-string-in-python

    :return: _description_
    :rtype: _type_
    """
    return re.sub('[^0-9]', '', my_string)


def strip_accents(my_string: str) -> str:
    """
    Retira acentos das palavras
    https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string

    :param my_string: Texto com acento
    :type my_string: string
    :return: Texto sem acento
    :rtype: my_string
    """
    return ''.join(
        c
        for c in unicodedata.normalize('NFD', str(my_string))
        if unicodedata.category(c) != 'Mn'
    )


def adjust_columns(df: pd.DataFrame, column_ajust: str) -> pd.DataFrame:
    """
    Adiciona coluna à tabela, com sufixo _temp,
    com correções diversas para fins de "fazer bater"

    :param df: tabela bruta
    :return: tabela com coluna a mais
    """
    #

    # Coluna para ajustar
    col_temp = f'{column_ajust}_temp'

    # Para Bater
    df[col_temp] = df[column_ajust]
    df[col_temp] = df[col_temp].str.strip()
    df[col_temp] = df[col_temp].str.lower()
    df[col_temp] = df.apply(
        lambda x: strip_accents(x[col_temp]), axis='columns'
    )
    df[col_temp] = df[col_temp].str.replace('’', '')
    df[col_temp] = df[col_temp].str.replace('´', '')
    df[col_temp] = df[col_temp].str.replace("'", '')

    #
    dd_fix = {
        # Errado / Certo
        'rio grande de serra': 'rio grande da serra',
        'santa rosa de viterbo': 'santa rosa do viterbo',
        'santana do parnaiba': 'santana de parnaiba',
        'sao luis do paraitinga': 'sao luiz do paraitinga',
    }

    df[col_temp] = df[col_temp].rename(dd_fix, axis='rows')
    df = df.replace({col_temp: dd_fix})

    # Results
    df.info()
    df.head()
    return df


class QuemSomos:
    def __init__(self) -> None:

        # Get Source Page
        url = 'https://www.tjsp.jus.br/QuemSomos/QuemSomos/RegioesAdministrativasJudiciarias'
        content = urllib.request.urlopen(url=url).read()
        tree = html.fromstring(content)

        # Get Box of Circunscrição
        list_divs = tree.xpath("//div[contains(@style, 'background')]")

        list_dfs_rajs = []
        list_dfs_cjs = []

        for div in list_divs:
            # A partir da div, pega os "p"
            list_p = div.xpath('.//p')
            raj = list_p[0].text_content().strip()
            raj_list = re.split(pattern=r'[-–]', string=raj, maxsplit=0)
            raj_num = raj_list[0].strip()
            raj_regiao = raj_list[1].strip()
            juiz = list_p[1].text_content().strip().split(':')[1].strip()
            email = re.sub('[()]', '', list_p[2].text_content().strip())

            # Para cada div, pega o primeiro ul que encontramos
            list_ul = div.xpath('./..//ul')[0]
            list_ul = div.getnext()
            list_li = list_ul.xpath('.//li')

            dict_raj = {
                'raj_nome': raj,
                'raj_sigla': raj_num,
                'raj_regiao': raj_regiao,
                'juiz_diretor_nome': juiz,
                'juiz_diretor_email': email,
            }
            list_dfs_rajs.append(dict_raj)

            # Circunscrição Judiciária
            list_cjs = [x.text_content() for x in list_li]
            df = pd.DataFrame(data=list_cjs, columns=['comarca_cirscunscricao'])
            df['raj_sigla'] = raj_num
            list_dfs_cjs.append(df)

        # ddd
        df = pd.concat(list_dfs_cjs, ignore_index=True)
        self.df = df
        self.list_dfs_rajs = list_dfs_rajs

    def get_raj(self) -> pd.DataFrame:
        df_raj = pd.DataFrame(self.list_dfs_rajs)
        df_raj['raj_nome'] = df_raj['raj_nome'].str.replace('–', '-')
        df_raj['id_raj'] = df_raj['raj_sigla'].apply(lambda x: keep_numbers(x))
        df_raj['id_raj'] = df_raj['id_raj'].astype(int)
        df_raj = df_raj.sort_values(by='id_raj', ascending=True)
        df_raj = df_raj.reset_index(drop=True)

        df_raj = df_raj[
            [
                # RAJ
                'id_raj',
                'raj_nome',
                'raj_sigla',
                'raj_regiao',
                'juiz_diretor_nome',
                'juiz_diretor_email',
            ]
        ]
        return df_raj

    def get_cj(self) -> pd.DataFrame:
        # ddd
        df_cj = self.df.copy()
        df_cj[['comarca', 'cj_sigla']] = df_cj[
            'comarca_cirscunscricao'
        ].str.rsplit('-', n=1, expand=True)

        df_cj['cj_sigla'] = df_cj['cj_sigla'].str.strip()

        # Id RAJ
        df_cj['id_raj'] = df_cj['raj_sigla'].apply(lambda x: keep_numbers(x))
        df_cj['id_raj'] = df_cj['id_raj'].astype(int)

        # Id CJ
        df_cj['id_cj'] = df_cj['cj_sigla'].apply(lambda x: keep_numbers(x))
        df_cj.loc[df_cj['id_cj'] == '', 'id_cj'] = '0'
        df_cj['id_cj'] = df_cj['id_cj'].astype(int)

        df_cj['cj_nome'] = df_cj['cj_sigla'].replace(
            'CJ', 'Circunscrição Judiciária', regex=True
        )
        df_cj['cj_nome'] = df_cj['cj_nome'].str.strip()

        df_cj = df_cj[
            [
                # CJ
                'id_cj',
                'cj_sigla',
                'cj_nome',
                #'comarca_cirscunscricao',
                # Comarca
                #'comarca',
                'id_raj',
            ]
        ]

        df_cj = df_cj.drop_duplicates()
        df_cj = df_cj.sort_values(by='id_cj')
        df_cj = df_cj.reset_index(drop=True)
        df_cj = df_cj.drop_duplicates()

        # Results
        # df_cj.to_clipboard(index=False)
        # df_cj.info()
        # df_cj.head(20)
        return df_cj

    def get_comarcas(self):
        # ddd
        df_comarca = self.df.copy()
        df_comarca[['comarca', 'cj_sigla']] = df_comarca[
            'comarca_cirscunscricao'
        ].str.rsplit('-', n=1, expand=True)

        df_comarca['cj_sigla'] = df_comarca['cj_sigla'].str.strip()

        # Id RAJ
        # df_comarca['id_raj'] = df_comarca['raj_sigla'].apply(lambda x: keep_numbers(x))
        # df_comarca['id_raj'] = df_comarca['id_raj'].astype(int)

        # Id CJ
        df_comarca['id_cj'] = df_comarca['cj_sigla'].apply(
            lambda x: keep_numbers(x)
        )
        df_comarca.loc[df_comarca['id_cj'] == '', 'id_cj'] = '0'
        df_comarca['id_cj'] = df_comarca['id_cj'].astype(int)

        df_comarca['cj_nome'] = df_comarca['cj_sigla'].replace(
            'CJ', 'Circunscrição Judiciária', regex=True
        )
        df_comarca['cj_nome'] = df_comarca['cj_nome'].str.strip()

        df_comarca = df_comarca[
            [
                # CJ
                'comarca',
                'id_cj',
                #'cj_sigla',
                #'cj_nome',
                #'comarca_cirscunscricao',
                # Comarca
                #'id_raj',
            ]
        ]

        df_comarca = df_comarca.drop_duplicates()

        # Renomear
        df_comarca = df_comarca.rename(
            {
                'comarca': 'comarca_tjsp',
            },
            axis='columns',
        )

        # Ordena
        df_comarca = df_comarca.iloc[
            df_comarca['comarca_tjsp'].str.normalize('NFKD').argsort()
        ]
        df_comarca = df_comarca.reset_index(drop=True)

        # Aplica strip em todo o dataframe
        df_comarca = df_comarca.map(
            lambda x: x.strip() if isinstance(x, str) else x
        )

        # Reordena as colunas
        df_comarca = df_comarca[['id_cj', 'comarca_tjsp']]

        # Results
        # df_comarca.to_clipboard(index=False)
        # df_comarca.info()
        # df_comarca.head(20)
        return df_comarca


class TJSP:
    def __init__(self) -> None:
        df_mun = geo.load_dataset(db='sp', name='tab.municipio_nome')
        self.lista_municipios = df_mun['municipio_nome']
        self.list_termos = self.list_terms_search()

    @property
    def get_max_caracteres_numero(self) -> int:
        return max([len(x) for x in self.lista_municipios])

    def get_lista_municipios_tjsp(self, contain):
        """
        Pesquisa de municípios a partir de alguns caracteres.
        A função sempre retorna 10 itens.
        A cada caractere, o número de registros afunila!

        Exemplo de uso:
        df = get_lista_municipios_tjsp('Santos')

        :param municipio: _description_
        :type municipio: _type_
        :raises Exception: _description_
        """
        if len(contain) < 3:
            raise Exception(
                'A pesquisa de município deve ter mais de 3 caracteres'
            )

        r = requests.post(
            url='https://www.tjsp.jus.br/AutoComplete/ListarMunicipios',
            json={'texto': contain},
        )
        if r.json() == 'listaVazia':
            pass

        else:
            df = pd.DataFrame(r.json())
            df = df.rename(
                mapper={
                    'Codigo': 'id_municipio_tjsp',
                    'Descricao': 'municipio_tjsp',
                },
                axis='columns',
            )
            return df

    def list_terms_search(self):
        """
        A partir do número de caracteres máximo dos 645 municícípios,
        é possível ver todas as combinações de 3 caracteres
        """
        # list_dfs = []
        list_termos = []
        for i in range(self.get_max_caracteres_numero)[3:]:
            lista_municipios_temp = list(
                set([mun[:i] for mun in self.lista_municipios if len(mun) >= i])
            )
            for search_text in lista_municipios_temp:
                list_termos.append(search_text)

        list_termos = list(set(list_termos))
        print(f'São {len(list_termos)} termos para pesquisa')
        return list_termos

    def search_terms(self, threads=4) -> pd.DataFrame:

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=threads
        ) as executor:
            temp = executor.map(
                self.get_lista_municipios_tjsp, self.list_termos
            )
            df_tjsp = pd.concat(list(temp), ignore_index=True)

        return df_tjsp

    def search_terms_aws(
        self, aws_access_key_id, aws_secret_access_key
    ) -> pd.DataFrame:
        """
        sss
        """

        # Cria Gateway
        gateway = ApiGateway(
            site='https://www.tjsp.jus.br',
            access_key_id=aws_access_key_id,
            access_key_secret=aws_secret_access_key,
            regions=['sa-east-1'],
            verbose=True,
        )
        gateway.pool_connections = 5
        gateway.pool_maxsize = 5
        gateway.start()

        try:
            # Cria Session
            session = requests.Session()
            session.mount(prefix='https://www.tjsp.jus.br', adapter=gateway)

            # Parameters
            # MAX_THREADS = 4
            list_dfs = []
            # list_futures = []

            # Em 23.01.2025 tentei o uso do API
            for term in self.list_termos:
                # print(term)
                df = self.get_lista_municipios_tjsp(contain=term)
                list_dfs.append(df)

            # Crio a tabela
            df_tjsp = pd.concat(list_dfs, ignore_index=True)

            # Results
            return df_tjsp

        except Exception as e:
            raise Exception(e)

        finally:
            # Encerra o worker
            gateway.shutdown()

    def adjust_data(self, df):

        # Ajusta a tabela
        df_tjsp = df.drop_duplicates()
        df_tjsp = df_tjsp.sort_values(by='municipio_tjsp')
        df_tjsp = df_tjsp.iloc[
            df_tjsp['municipio_tjsp'].str.normalize('NFKD').argsort()
        ]
        df_tjsp = df_tjsp.reset_index(drop=True)

        num_municipios = len(df_tjsp)
        if num_municipios != 645:
            raise Exception(f'Falta Município! Temos {num_municipios}')

        # Resultados
        # df_tjsp.info()
        # df_tjsp.head()
        return df_tjsp


class ListaTelefonica:
    def __init__(self) -> None:
        pass

    def get_lista_unidades_tjsp(self, cod_municipio: int):
        """
        Pega a lista de unidades (Fóruns) de um determinado Município,
        a partir do Código do Município do TJSP
        :param cod_municipio: _description_
        :type cod_municipio: _type_
        :return: _description_
        """

        # Requests
        r: requests.Response = requests.post(
            'https://www.tjsp.jus.br/ListaTelefonica/RetornarResultadoBusca',
            json={'parmsEntrada': cod_municipio, 'codigoTipoBusca': 1},
            timeout=60,
        )

        # BS4
        soup = BeautifulSoup(r.text, 'html.parser')
        text_comarca = soup.find_all('h4')
        if text_comarca == []:
            raise Exception('Erro')

        else:
            text_comarca = one(text_comarca)
            text_comarca = text_comarca.text

            #
            comarca = text_comarca.split(' - ')[0]
            raj = text_comarca.strip().split(' - ')[-1]
            # print(raj)

            # comarca = comarca.split('está jurisdicionado à Comarca ')
            comarca = comarca.replace('Município ', '')
            comarca = comarca.replace('está jurisdicionado à Comarca', ' | ')
            comarca = comarca.replace('da Comarca', ' | ')
            # print(comarca)

            mun = comarca.strip().split(' | ')[0]
            com = comarca.strip().split(' | ')[-1]

            if mun.strip() == com.strip():
                comarca_sede = 1
            else:
                comarca_sede = 0

            # print(text_comarca)
            # print(text_comcarca.split('jurisdicionado à comarca '))

        lista_unidades = [x.text for x in soup.find_all('span')]

        return pd.DataFrame(
            {
                'id_municipio_tjsp': cod_municipio,
                'raj': raj.strip(),
                'municipio_tjsp': mun.strip(),
                'comarca_tjsp': com.strip(),
                'comarca_sede': comarca_sede,
                'unidades': lista_unidades,
            }
        )


if __name__ == '__main__':
    tjsp = QuemSomos()
    print(tjsp.df.head())

    df_raj = tjsp.get_raj()
    print(df_raj.head())

    df_cj = tjsp.get_cj()
    print(df_cj.head())

    df_comarca = tjsp.get_comarcas()
    print(df_comarca.head())
