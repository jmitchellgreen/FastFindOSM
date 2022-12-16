# Fast Find OSM
#### A Python command line interface for quickly searching or querying OpenStreetmap  features and downloading as a geoJSON

_____  
        
Usage

`fastfindosm.py [-h] [-q QUERYFILE] [-s SEARCH] OUTFILE`

```
positional arguments:
  OUTFILE               Output name for geojson file (need to include .geojson extension)

optional arguments:
  -h, --help            show this help message and exit
  -q QUERYFILE, --queryfile QUERYFILE
                        Text file containing OSM Overpass API querylangauge query
  -s SEARCH, --search SEARCH
                        Use the Nominatim API (geocoding) search to find OSM features
```

  
### Examples
`python fastfindosm -s "New York City" nyc.geojson`

`python fastfindosm -q query.txt my_query.geojson`

### Features
- Includes pick list of OSM features  
  - For example, if you are looking for *Paris, Texas, USA*, not *Paris, France* simply navigate down with the arrow keys to select the appropiate choice.  
`python fastfindosm -s "Paris" paris.geojson`  
Gives the following options:  
```Paris, Île-de-France, France métropolitaine, France
   Paris, Île-de-France, France métropolitaine, France
 > Paris, Lamar County, Texas, 75460, United States
   Paris, Bourbon County, Kentucky, 40361, United States
   Paris, Île-de-France, France métropolitaine, France
   Paris, Henry County, West Tennessee, Tennessee, United States
   Paris, Edgar County, Illinois, 61944, United States
   Paris, Oxford County, Maine, 04281, United States
   Town of Paris, Oneida County, New York, United States
   Paris, Logan County, Arkansas, 72855, United States
   ```
