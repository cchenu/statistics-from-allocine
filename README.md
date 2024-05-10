# Statistics-from-allocine
> Python program to have statistics about a films list from Allocine

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Usage](#usage)
* [Project Status](#project-status)
* [Contact](#contact)
* [License](#license)


## General Information
On Allocine, a feature allow to create collection of films. The website do not give statistics on a collection, the goal of this projet is to have these statistics. 
This projet recoveries different data about films of one collection with python and creates csv files with these data. It is possible to have some graphs with power BI.

## Technologies Used
- Python - version 3.11.9
  - Python library : BeautifulSoup (bs4), csv, re, requests, tqdm
- Microsoft Power BI Desktop - version 2.124

## Features
- Create csv files from a Allocine collection.
  - Create films.csv with for all films his Allocine's id, his title, his duration, his genres, his year and his countries.
  - Create countries.csv with for each country present in the Allocine collection, gives the number of films from this country.
  - Create genres.csv with for each film genre present in the Allocine collection, gives the number of films of this genre.
- Create graphs on Power BI.
  - Create a histogram films by year.
  - Create a histogram films by country.
  - Create a map with films by country.
  - Create a histogram films by genre.
  - Create a histogram films by duration.

![Four different graphs](https://zupimages.net/up/24/19/4cc1.png)
![Histogram films by duration](https://zupimages.net/up/24/19/fgw1.png)

## Usage
To use this code, first, you have to open the main.py file.
After, you must find your collection ID and your Allocine token, to find these, go to your Allocine page with all your collections, inspect the element (right click and inspect). Go on network tab. Click on your collection, an event "public" appears, click on it. On headers tab, in authorization, after "Bearer", you have your token. On payload tab, after "collectionId" you have your id.
Complete the lines 75 and 76 of main.py and launch your script.
If you just want the csv files, you have it in "csv" folder.
If you want to use Power BI, open rapport.pbix, go on home tab, on "Edit queries", in data source settings and write the paths of your csv files.


## Project Status
Project is: _complete_ - version 1.1.0.


## Contact
Created by [@cchenu](https://github.com/cchenu/) - feel free to contact me!

## License
This project is open source and available under the [MIT License](LICENSE).

