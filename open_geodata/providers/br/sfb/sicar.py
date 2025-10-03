"""
_summary_

:raises ValueError: _description_
:return: _description_
:rtype: _type_
"""

from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests
import requests.adapters
import urllib3
from urllib3.util import create_urllib3_context

# from SICAR import Polygon, Sicar, State


# from geodata.owslib.scripts.car.general import CustomWebFeatureService
class CustomSSLContextHTTPAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs) -> None:
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(
        self, connections, maxsize, block=False, **kwargs
    ) -> None:
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context,
        )


class CAR:
    def __init__(self, uf='SP') -> None:
        self.uf = uf

    @property
    def url(self) -> str:
        # Base URL
        base_url = 'https://geoserver.car.gov.br/geoserver/sicar/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=sicar%3Asicar_imoveis_es&outputFormat=application%2Fjson'

        # Divide URL
        split_url = urlsplit(url=base_url)
        # print(split_url)

        # Muda o Layer
        params = dict(parse_qsl(split_url.query))
        params['typeName'] = f'sicar:sicar_imoveis_{self.uf.lower()}'
        # print(params)

        # Params Encoded
        encode_params = urlencode(query=params, doseq=True)
        # print(encode_params)

        return urlunsplit(
            (
                split_url.scheme,  # https
                split_url.netloc,  # servidor.com
                split_url.path,  # /wfs
                encode_params,  # Parâmetros modificados (a nova query)
                split_url.fragment,  # fragmento (#anchor)
            )
        )

    def download_file(self, filepath: str | Path):
        """
        Faz o downlaod do arquivo

        :param filepath: Nome e pasta do arquivo
        :type filepath: str | Path
        :return: _description_
        :rtype: str | Path
        """

        ctx = create_urllib3_context()
        ctx.load_default_certs()
        ctx.set_ciphers('AES256-GCM-SHA384')

        session = requests.session()
        session.adapters.pop('https://', None)
        session.mount('https://', CustomSSLContextHTTPAdapter(ctx))

        with session.get(url=self.url, stream=True) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)


# # uf = 'SP'
# car = CAR(uf='SP')
# car.url


# class SICAR:
#     """
#     Class to handle the Sicar data provider.
#     """

#     def __init__(
#         self,
#         tesseract_path: str | Path,
#     ):
#         """
#         Initialize the Sicar data provider with optional parameters.
#         """
#         tesseract_path = Path(tesseract_path)
#         if tesseract_path.is_file():
#             self.tesseract_path = Path(tesseract_path)

#             # Set the tesseract command path for pytesseract
#             pytesseract.pytesseract.tesseract_cmd = (
#                 self.tesseract_path.as_posix()
#             )

#         else:
#             raise ValueError(f"Invalid tesseract path: {tesseract_path}")

#         # Create Sicar instance
#         self.car = Sicar()

#     @property
#     def release_dates(self):
#         """
#         Method to retrieve data from the Sicar provider.
#         """
#         # Implementation for retrieving data goes here
#         return self.car.get_release_dates()

#     @property
#     def list_states(self) -> list[State]:
#         return [x for x in State]

#     @property
#     def list_layers(self) -> list[Polygon]:
#         return [x for x in Polygon]

#     def download_data(
#         self, sigla_estado: State, layer: Polygon, output_path, *args, **kwargs
#     ):
#         """
#         Download data for a specific state.
#         """
#         n_tentativas = kwargs.get('n_tentativas', 3)
#         tentativa = 0

#         while tentativa < n_tentativas:
#             try:
#                 self.car.download_state(
#                     state=sigla_estado,
#                     polygon=layer,
#                     folder=output_path,
#                 )
#                 print(f"Polygon for {sigla_estado} downloaded successfully.")
#                 break

#             except Exception as e:
#                 print(f"Error downloading polygon for {sigla_estado}: {e}")
#                 tentativa += 1


# if __name__ == "__main__":
#     # Example usage
#     # sicar = SICAR(tesseract_path="/usr/bin/tesseract")
#     sicar = SICAR(
#         tesseract_path=r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
#     )
#     release_dates = sicar.release_dates
#     pprint.pprint(release_dates)

#     #
#     print(sicar.list_states)

#     # Example of using the Sicar class to get a state
#     # state = sicar.car.get_state(State.ACRE)
#     # print(f"State: {state.name}, Code: {state.code}")
