# FastFindOSM.py
#
# Created By: J. Mitchell Green
# Email: jamesmitchellgreen@yahoo.com


import requests
import osm2geojson
import geojson
import json
import argparse
import inquirer
import pprint


class FastFindOSM:
    """
    This class accesses the open street map 'Overpass' API from a 'Nominatim' geocoding API
    search or direct query and transforms the response into a geojson
    """

    def __init__(self, outname):
        self.OVERPASS_URL = "http://overpass-api.de/api/interpreter/"
        self.NOMINATIM_SEARCH_URL = "https://nominatim.openstreetmap.org/search?"
        self.outname = outname

    def osm_query_to_geojson(self, query):
        # call overpass API
        response = requests.get(url=self.OVERPASS_URL, params={"data": query})

        # read response as json
        osm_json = response.json()

        # convert to geojson
        my_geojson = osm2geojson.json2geojson(osm_json)

        # dump to file
        with open(self.outname, "w") as file:
            geojson.dump(my_geojson, file)

    def query_file(self, query_file):
        # read query file
        with open(query_file, "r") as file:
            query = file.read()

        self.osm_query_to_geojson(query)

    def nominatim_search(self, search_param, download=False):
        # request for Nominatim Search geocoder
        response = requests.get(
            url=self.NOMINATIM_SEARCH_URL,
            params={"q": search_param, "format": "json"},
        )

        # read response as json
        response_json = response.json()

        # get list display names from osm items
        results = [item["display_name"] for item in response_json]

        if not results:
            print("No results, try again with different keywords")
            return

        # inquirer CLI
        questions = [
            inquirer.List(
                "response",
                message="Please select a OSM feature",
                choices=results,
            ),
        ]

        # user selection
        answer = inquirer.prompt(questions)

        # grab answer info
        for item in response_json:
            if item["display_name"] == answer["response"]:
                osm_id =  item["osm_id"]
                osm_type = item["osm_type"]
                display_name = item["display_name"]


        if download:
            # query for Overpass API
            query = f"""
            [out:json][timeout:1000];
            nwr({osm_id});
            (._;>;);
            out;
            """

            self.osm_query_to_geojson(query)

        if not download:
            info = {
                "Feature Name:": display_name,
                "OSM ID": osm_id,
                "OSM Type": osm_type
            }
            pprint.pprint(info)

        return

if __name__ == "__main__":
    # initialize parser
    parser = argparse.ArgumentParser(
        description="Query OpenStreetMap and download as geojson"
    )

    # add argparse arguments
    parser.add_argument("-q", "--queryfile", help="File containing OSM Overpass query")
    parser.add_argument("-s", "--search", help="Use Nominatim (geocoding) search to query OSM")
    parser.add_argument("-i", "--info", help="Info on selected OSM feature")
    parser.add_argument("-o", "--outfile", help="Output name for geojson file (need to include .geojson extension)")


    # get args
    args = parser.parse_args()
    # print(args)

    # flag options to call function
    if args.queryfile:
        FastFindOSM(args.outfile).query_file(args.queryfile)
    if args.search:
        FastFindOSM(args.outfile).nominatim_search(args.search, download=True)
    if args.info:
        FastFindOSM(args.outfile).nominatim_search(args.info)