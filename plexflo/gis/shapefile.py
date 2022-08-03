from osgeo import gdal
import geopandas as gpd
import glob
import os
from zipfile import ZipFile
from pathlib import Path



def shapefile2geojson(infile, outfile):
    """
    Convert a shapefile to a GeoJSON file. Make sure that the corresponding SHX, DBF file is in the same folder as
    the SHP file.
    Args:
        infile: path to a shapefile (*.shp) format outfile: name of the geojson file to be created

    Returns:
        None
    """
    # TODO: create the exception when the SHX and DBF files are not in the same folder as the SHP file
    # TODO: make sure that the geojson file is created in the same folder as the SHP file

    options = gdal.VectorTranslateOptions(format="GeoJSON",
                                          dstSRS="EPSG:4326")
    gdal.VectorTranslate(outfile, infile, options=options)


def geojson2geopandas(infile):
    """
    Convert a GeoJSON file to a GeoPandas dataframe.
    Args:
        infile: path to a GeoJSON file

    Returns:
        GeoPandas dataframe
    """
    data = gpd.read_file(infile)
    print("Here is the dataframe:")
    return data


def shapefile_centroid(infile, feature_column_name):
    pass

def split_shpfile_into_multiple_shpfiles(infile, feature_column_name):
    outfolder = Path(infile).stem
    Path(outfolder).mkdir(exist_ok=True, parents=True)
    file_of_interest = []

    with ZipFile(infile, 'r') as zip_ref:
        zip_ref.extractall(outfolder)
        os.chdir(f"{outfolder}/{outfolder}")
        for file in glob.glob("*.shp"):
            file_of_interest.append(file)

        file_of_interest = file_of_interest[0]

        data = gpd.read_file(file_of_interest)

        for idx, row in data.iterrows():
            output_name = f"{row[feature_column_name].replace(' ', '_')}.shp"
            shp_name = row[feature_column_name]
            Path(f"{shp_name}/ArcGIS_shpfile").mkdir(exist_ok=True, parents=True)
            output_path = os.path.join(shp_name, "ArcGIS_shpfile", output_name)
            tmp_df = data[data[feature_column_name] == shp_name]
            tmp_df.to_file(output_path)


def split_shpfile_into_multiple_geojson(infile, feature_column_name):
    outfolder = Path(infile).stem
    Path(outfolder).mkdir(exist_ok=True, parents=True)
    file_of_interest = []

    with ZipFile(infile, 'r') as zip_ref:
        zip_ref.extractall(outfolder)
        os.chdir(f"{outfolder}/{outfolder}")
        for file in glob.glob("*.shp"):
            file_of_interest.append(file)

        file_of_interest = file_of_interest[0]

        data = gpd.read_file(file_of_interest)

        for idx, row in data.iterrows():
            shpfile_output_name = f"{row[feature_column_name].replace(' ', '_')}.shp"
            geojson_output_name = f"{row[feature_column_name].replace(' ', '_')}.geojson"
            shp_name = row[feature_column_name]
            Path(f"{shp_name}/ArcGIS_shpfile").mkdir(exist_ok=True, parents=True)
            Path(f"{shp_name}/GeoJSON").mkdir(exist_ok=True, parents=True)
            shpfile_output_path = os.path.join(shp_name, "ArcGIS_shpfile", shpfile_output_name)
            geojson_output_path = os.path.join(shp_name, "GeoJSON", geojson_output_name)
            tmp_df = data[data[feature_column_name] == shp_name]
            tmp_df.to_file(shpfile_output_path)
            shapefile2geojson(shpfile_output_path, geojson_output_path)
            try:
                pass
                # remove_path(Path(f"{shp_name}/ArcGIS_shpfile"))
            except OSError as e:
                print("Error Code 901: Could not delete temporary *.shpfile folder %s \n%s" % (
                    shpfile_output_path, e.strerror))



infile = "Test.geojson"
print("Hekko")
df = geojson2geopandas(infile)
breakpoint()