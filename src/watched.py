"""Module which gives the list of films' IDs."""

from typing import Any

import requests


def watched_list(collection_id: str, token: str) -> list[int]:
    """
    Create the list of movie IDs from a specific Allocine collection.

    Parameters
    ----------
    collection_id : str
        ID of the Allocine collection.
    token : str
        Token to be connected to Allocine.

    Returns
    -------
    list_id : list[int]
        List of movie IDs from the specified Allocine collection.
    """
    # URL of Allocine's API
    url = "https://graph.allocine.fr/v1/public"

    # Header of the requests
    headers = {"Authorization": "Bearer " + token}

    # Parameters of the post requests
    params: dict[Any, Any] = {
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
        "variables": {"collectionId": collection_id, "first": 120},
    }

    response = requests.post(url, headers=headers, json=params, timeout=10)
    # Information are in entities
    entities = response.json()["data"]["me"]["user"]["social"]["collections"][
        "edges"
    ][0]["node"]["entities"]
    number_films = entities["totalCount"]
    list_id: list[int] = []
    # Each request retrieves up to 120 films; check if additional pages exist.
    while len(list_id) != number_films:
        # Find the films id on this page
        list_id.extend(
            film["node"]["entity"]["internalId"] for film in entities["edges"]
        )

        after = entities["pageInfo"]["endCursor"]  # Find the end of this page
        params["variables"]["after"] = after  # Set the beginning of next page
        response = requests.post(url, headers=headers, json=params, timeout=10)
        entities = response.json()["data"]["me"]["user"]["social"][
            "collections"
        ]["edges"][0]["node"]["entities"]
    return list_id
