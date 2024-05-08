"""Module which give the list of films' id."""

import requests


def watched_list(collection_id, token):
    """
    Create the list of films' id.

    Parameters
    ----------
    collection_id : string
        ID of the Allocine collection.
    token : TYPE
        Token to be connected to Allocine.

    Returns
    -------
    list_id : list of integer
        List of the films' id on Allocine.

    """
    # URL of the Allocine's api
    url = "https://graph.allocine.fr/v1/public"

    # Header of the requests
    headers = {"Authorization": "Bearer " + token}

    # Parameters of the post requests
    params = {
        "operationName": "GetCollectionEntities",
        "query": """
        fragment MovieFragment on Movie {
          id
          internalId
          title
          poster {
            path
            __typename
          }
          releaseFlags {
            release {
              svod {
                original
                exclusive
                __typename
              }
              __typename
            }
            upcoming {
              svod {
                original
                exclusive
                __typename
              }
              __typename
            }
            __typename
          }
          data {
            productionYear
            __typename
          }
          __typename
        }

        fragment SeriesFragment on Series {
          id
          internalId
          title
          status
          poster {
            path
            __typename
          }
          releaseFlags {
            release {
              svod {
                original
                exclusive
                __typename
              }
              __typename
            }
            upcoming {
              svod {
                original
                exclusive
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }

        query GetCollectionEntities(
          $after: String,
          $collectionId: String!,
          $first: Int
        ) {
          me {
            user {
              id
              social {
                collections(id: $collectionId, first: 1) {
                  edges {
                    node {
                      id
                      internalId
                      owner {
                        id
                        legacyId
                        __typename
                      }
                      name
                      description
                      seriesCount
                      moviesCount
                      followersCount
                      entities(after: $after, first: $first) {
                        totalCount
                        pageInfo {
                          hasNextPage
                          endCursor
                          __typename
                        }
                        edges {
                          node {
                            id
                            opinion {
                              id
                              content {
                                rating(base: 5)
                                __typename
                              }
                              __typename
                            }
                            entity {
                              ... on Movie {
                                ...MovieFragment
                                __typename
                              }
                              ... on Series {
                                ...SeriesFragment
                                __typename
                              }
                              __typename
                            }
                            __typename
                          }
                          __typename
                        }
                        __typename
                      }
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        """,
        "variables": {"collectionId": collection_id, "first": 120}}

    response = requests.post(url, headers=headers, json=params, timeout=10)
    # Information are in entities
    entities = (response.json()['data']['me']['user']['social']['collections']
                ['edges'][0]['node']['entities'])
    number_films = entities['totalCount']
    list_id = []
    # We can just have 120 films for one request, we have to know if there is
    # another page
    while len(list_id) != number_films:
        for films in entities['edges']:  # Find the films id on this page
            list_id.append(films['node']['entity']['internalId'])
        after = entities['pageInfo']['endCursor']  # Find the end of this page
        params['variables']['after'] = after  # Set the beginning of next page
        response = requests.post(url, headers=headers, json=params, timeout=10)
        entities = (response.json()['data']['me']['user']['social']
                    ['collections']['edges'][0]['node']['entities'])
    return list_id


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
    watched = watched_list(ID, TOKEN)
