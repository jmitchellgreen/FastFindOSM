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


class FastFindOSM:
    """
    This class accesses the open street map 'Overpass' API from a 'Nominatim' geocoding API
    search or direct query and transforms the response into a geojson
    """

    def __init__(self, outname):
        self.OVERPASS_URL = "http://overpass-api.de/api/interpreter/"
        self.NOMINATIM_SEARCH_URL = "https://nominatim.openstreetmap.org/search?"
        self.outnane = outname

    def osm_query_to_geojson(self, query):
        # call overpass API
        response = requests.get(url=self.OVERPASS_URL, params={"data": query})

        # read response as json
        osm_json = response.json()

        # convert to geojson
        my_geojson = osm2geojson.json2geojson(osm_json)

        # dump to file
        with open(self.outnane, "w") as file:
            geojson.dump(my_geojson, file)

    def query_file(self, query_file):
        # read query file
        with open(query_file, "r") as file:
            query = file.read()

        self.osm_query_to_geojson(query)

    def nominatim_search(self, search_param):
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

        # grab osm_type and osm_id
        for item in response_json:
            if item["display_name"] == answer["response"]:
                osm_item = [item["osm_type"], item["osm_id"]]

        key = osm_item[0]
        val = osm_item[1]

        # query for Overpass API
        query = f"""
        [out:json][timeout:1000];
        nwr({val});
        (._;>;);
        out;
        """
        self.osm_query_to_geojson(query)


if __name__ == "__main__":
    # initialize parser
    parser = argparse.ArgumentParser(
        description="Query OpenStreetMap and download as geosjon"
    )

    # add argparse arguments
    parser.add_argument("-q", "--queryfile", help="File containing OSM Overpass query")
    parser.add_argument(
        "-s", "--search", help="Use Nominatim (geocoding) search to query OSM"
    )
    parser.add_argument(
        "OUTFILE",
        metavar="OUTFILE",
        help="Output name for geojson file (need to include .geojson extension)",
    )

    # get args
    args = parser.parse_args()

    # flag options to call function
    if args.queryfile:
        FastFindOSM(args.outname).query_file(args.queryfile)
    if args.search:
        FastFindOSM(args.outname).nominatim_search(args.search)
