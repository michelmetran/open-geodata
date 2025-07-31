# Agência Nacional de Mineração

## Python 2

Apenas para fins de registro histórico, encontrei um _script_ escrito para trabalhar com o [ArcPy](https://www.esri.com/pt-br/arcgis/products/arcgis-python-libraries/libraries/arcpy), de 04.04.2013.

```python
# Cria base de dados do SIGMINE
# 04/04/2013

# 1. Cria Geodatabase
workspace E:\GIS_Outros\BR_CPRM\SIGMINE\Geodata

CreatePersonalGDB_management %workspace% Geo_SIGMINE

workspace E:\GIS_Outros\BR_CPRM\SIGMINE\Geodata\Geo_SIGMINE

CreateFeatureDataset_management %workspace% SIGMINE "GEOGCS['GCS_South_American_1969',DATUM['D_South_American_1969',SPHEROID['GRS_1967_Truncated',6378160.0,298.25]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],VERTCS['WGS_1984_Geoid',VDATUM['WGS_1984_Geoid'],PARAMETER['Vertical_Shift',0.0],PARAMETER['Direction',1.0],UNIT['Meter',1.0]];-400 -400 11258999068426,2;-1043,7418235 4194304001953,12;-100000 10000;8,98312044744602E-09;0,001;0,001;IsHighPrecision"

# 2. Importa shapefiles
workspace E:\GIS_Outros\BR_CPRM\SIGMINE\Geodata\shp

FeatureClassToGeodatabase_conversion %workspace%\AC.shp;%workspace%\AL.shp;%workspace%\AM.shp;%workspace%\AP.shp;%workspace%\BA.shp;%workspace%\CE.shp;%workspace%\DF.shp;%workspace%\ES.shp;%workspace%\GO.shp;%workspace%\MA.shp;%workspace%\MG.shp;%workspace%\MS.shp;%workspace%\MT.shp;%workspace%\PA.shp;%workspace%\PB.shp;%workspace%\PE.shp;%workspace%\PI.shp;%workspace%\PR.shp;%workspace%\RJ.shp;%workspace%\RN.shp;%workspace%\RO.shp;%workspace%\RR.shp;%workspace%\RS.shp;%workspace%\SC.shp;%workspace%\SE.shp;%workspace%\SP.shp;%workspace%\TO.shp E:\GIS_Outros\BR_CPRM\SIGMINE\Geodata\Geo_SIGMINE.mdb\SIGMINE
```

<br>

Bem como um _.pdf_ da época, com as instruções para baixar os arquivos no extindo DNPM.

![2013.04.04 - DNPM - Departamento Nacional de Produção Mineral](./../../../assets/br/amn/2013.04.04%20-%20DNPM%20-%20Departamento%20Nacional%20de%20Produ%C3%A7%C3%A3o%20Mineral.pdf){ type=application/pdf style="min-height:50vh;width:100%" }
