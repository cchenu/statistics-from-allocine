# Statistics-from-allocine
> Python program to generate statistics from an Allocine film collection.

## Table of Contents
* [General Information](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Usage](#usage)
* [Project Status](#project-status)
* [Contact](#contact)
* [License](#license)

## General Information
Allocine allows users to create film collections, but the website does not provide statistics on these collections.  
The goal of this project is to generate statistics based on a given collection.  

This project retrieves various data about films from a collection using Python and generates CSV files.  
A **Streamlit** web app is also available to visualize the data.

## Technologies Used
- **Python** - version 3.12.2  
  - Python libraries: streamlit, pandas, plotly, requests, tqdm, beautifulsoup4, dotenv, and more (see `requirements.txt` for the full list).

## Features
### CSV File Generation
- Extract data from an Allocine collection and save it as CSV files.
  - `films.csv`: Contains information about each film, including its Allocine ID, title, duration, genres, release year, countries, press rating, spectator rating, actors, and directors.
  - `cesars.csv`, `palmes.csv`, and `oscars.csv`: Similar to `films.csv` but only include award-winning films from existing Allocine collections.
  - `countries.csv`: Lists the number of films per country.
  - `genres.csv`: Lists the number of films per genre.
  - `actors.csv`: Lists the number of films per actor IDs.
  - `directors.csv`: Lists the number of films per director IDs.

### Streamlit Web App
- Create a Streamlit web app.
  - Provide general statistics on the number of watched films, total watch time, countries with at least one watched film, most-watched actors, and most-watched directors.
  - Create a histogram of films by year.
  - Create a histogram of films by genre.
  - Create a histogram of films by country.
  - Create a map of films by country.
  - Create a histogram of films by duration.
  - Create a doughnut chart with watched César-winning films.
  - Create a doughnut chart with watched Oscar-winning films.
  - Create a doughnut chart with watched Palmes d'Or-winning films.
  - Create a doughnut chart with countries with at least one watched film.
  - Create a histogram of films by spectator rating.
  - Create a histogram of films by press rating.
  - Create a histogram of films without press rating by spectator rating.
  - Create a scatter plot of spectator rating as a function of press rating.
  - Show the nine most-watched directors, including their names, photos, and number of watched films.
  - Show the nine most-watched actors, including their names, photos, and number of watched films.

![First part of the streamlit app](https://zupimages.net/up/25/13/0ryo.png)
![Second part of the streamlit app](https://zupimages.net/up/25/13/x06n.png)
![Third part of the streamlit app](https://zupimages.net/up/25/13/lw17.png)

## Usage
### Setup
**Ensure you have Python 3.x installed.**

**Retrieve your Allocine collection ID and token:**
   - Go to your Allocine collections page.
   - Open your browser’s Developer Tools (`Right-click > Inspect` or press `F12`).
   - Navigate to the **Network** tab.
   - Click on your collection; an event named **"public"** should appear.
   - Under the **Headers** tab, find `Authorization`:  
     - The token is the value after **"Bearer"**.
   - Under the **Payload** tab, find `collectionId`:  
     - This is your collection ID.

**Create your `.env` file in your command prompt:**  
   ```bash
   cp .env.example .env
   ```

**Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
To launch the Streamlit app, navigate to your project folder in the command prompt (with `cd` command) and run:
   ```bash
   streamlit run app.py
   ```

### Other
Some data about durations or release years may be incorrect on the Allocine website. You can correct it in `corrections.py`.

If you only need the CSV files, you can find them in the `csv/` folder.


## Project Status
Project is: _complete_ - version 3.0.0.


## Contact
Created by [@cchenu](https://github.com/cchenu/) - feel free to contact me!

## License
This project is open source and available under the [MIT License](LICENSE).

