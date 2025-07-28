# Outros

Os dados espaciais são compilados no _packages_ do python, disponíveis para serem instalados por meio do _pip install_. Todos os dados estão em formato _geopackage_ (extensão _.gpkg_) e são comprimidos usando o _7zip_. Existem também alguns dados em formatos tabulares, em arquivos _.csv_, também comprimidos usando o _7zip_.

Com o pacote **_OpenGeodata_**, os dados espaciais são lidos como _geodataframes_(Geopandas), enquanto os dados tabulares são lidos como _dataframe_ (Pandas).

O projeto disponibiliza poucos dados, tendo em vista a limitação de 100mb do repositório oficial [PyPI](https://pypi.org/). É possível acessar outros dados instalando pacotes adicionais listados...

<br>

Para possibilitar testes do pacote, criei um [Google Colab](https://colab.research.google.com/drive/1s_w9t599OstJ0KS99NusH2EVGYa5twMh?usp=sharing).<br>
Todos os _datasets_ estão com _datum_ WGS84 (EPSG: 4326).

<br>

---

## Funções

Além das funções principais (para listar e carregar dados), o pacote entrega outras funções para uso com dados
geoespaciais.

## Maps Folium

Cria mapa folium com diversos _titles_ diferentes.

```python
from open_geodata import folium_plus

# Create Map
m = folium_plus.adds.create_map_multitiles()
m
```

## Layers

Cria objetos de _layers_ para serem inlcuidos no map folium.

```python
from open_geodata import lyr

# Add Layers
lyr.base.google_hybrid(min_zoom, max_zoom)
```

## Convert

Será removido!
Usei em um projeto quando não sabia fazer de outra forma.

```python
from open_geodata import converts

converts.df2geojson(df, lat='latitude', long='longitude', remove_coords_properties=True)
```
