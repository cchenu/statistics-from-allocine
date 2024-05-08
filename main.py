"""Create csv files for films data of a Allocine films collection."""

import csv
from tqdm import tqdm
from film import Film
from watched import watched_list


def films(collection_id, token):
    """
    Create csv files for films, countries and genres.

    Parameters
    ----------
    collection_id : string
        ID of the Allocine collection.
    token : TYPE
        Token to be connected to Allocine.

    Returns
    -------
    None.

    """
    list_id = watched_list(collection_id, token)
    headers = ['id', 'title', 'duration', 'genres', 'year', 'countries']
    country_dict = {}
    genre_dict = {}
    progress_bar = tqdm(total=len(list_id), desc="Progression")
    with open('films.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write headers
        writer.writeheader()

        # Write film data
        for id_ in list_id:
            film = Film(id_)
            for country in film.get_countries():  # Dictionary of countries
                country_dict[country] = country_dict.get(country, 0) + 1
            for genre in film.get_genres():  # Dictionary of genres
                genre_dict[genre] = genre_dict.get(genre, 0) + 1
            writer.writerow(film.get_total())
            progress_bar.update(1)
    progress_bar.close()

    # Creation of the country csv file
    headers = ['country', 'number']
    with open('countries.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write headers
        writer.writeheader()

        # Write film data
        for country, occurrences in country_dict.items():
            writer.writerow({'country': country, 'number': occurrences})

    # Creation of the genre csv file
    headers = ['genre', 'number']
    with open('genres.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write headers
        writer.writeheader()

        # Write film data
        for genre, occurrences in genre_dict.items():
            writer.writerow({'genre': genre, 'number': occurrences})

    print('\nCompleted!')


if __name__ == "__main__":
    ID = "VXNlckNvbGxlY3Rpb246NDgxMjc"
    TOKEN = ("eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MDc2ODE5MjEsImV"
             "4cCI6MTczOTMwNDMyMSwidXNlcm5hbWUiOiJjaGVudTQ0MkBnbWFpbC5jb20iLCJ"
             "hcHBsaWNhdGlvbl9uYW1lIjoid3d3IiwidXVpZCI6IjAzZDFiNjljLTY3YzgtNDQ"
             "wMy1iNTQ5LWU3MmUzNjU5YzA1MSIsInNjb3BlIjpudWxsfQ.nVSS4ARwEFXJ9Hid"
             "0IcSF4Bwsb0F8LjYoSw3Mke47fM5jWyP1s3FcIdtiRc_RIxi_TXiz_XyG1cMaZPs"
             "BIyodpHKeqSYlSac5uw0OsS_F4q3WY7t2T2auH44cLBTj96azoTpdMEbNelBwK2x"
             "y6nWBxC-O5cs8qiqoUnGWlOuaioDKEmY1Q_L0DDggx-HRRBndne7UHc3huX1GW7u"
             "q5QHeg1qxmpeSoOx64pX3ca53EJXUNCez_AZuzM6GWDz9vEaL6hTC_rTKATGyIA3"
             "6T2kioROtT3pKWraoAqCsVmDkq5UYpA9NIRp2vkS9sY3Fmc9lu_qr7XBSNXZl-Bx"
             "VslHXMPGRDUeB_9S5KdmAL2_rxn53LcTx5oxRP1TzAL09oCx0gZfJj8Tkr1zXKwy"
             "Ir1fsIdgjwUnV0l3ZQ8DZ3KHntUgsZwHjuPsgGXHV1L7yBg55hyKrlFB5PPrPdb0"
             "kpRLdDNL0SETbXrThzBq2fwIyKrSC3z5jTITsRDxBemQ0SKFuiWK8CiOBBdvtJbT"
             "LWTGZ3A0RTHgqU6XJV0GwGt4gQ1rvU7MsplCCRpgc9O38XvrouQEdZoYVdJ_s5Q_"
             "hYs06aPxcl6-_qe5BM8ig1MREZWjP2M1UOr1Bf0Oz-apu5hkeAYft2YvO_menFEq"
             "tA66_o0SvedxxycafL0jXnueVuE")
    films(ID, TOKEN)
