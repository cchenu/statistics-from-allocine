"""Types for the project."""

from collections.abc import Mapping
from typing import Literal, NotRequired, TypedDict


class CorrectionsDict(TypedDict):
    """Type for `corrections` constant in `corrections.py`."""

    year: Mapping[int, int]
    duration: Mapping[int, int]
    directors: Mapping[int, list[int]]


class PageInfoDict(TypedDict):
    """Type for key `pageInfo` in EntitiesDict."""

    hasNextPage: bool
    endCursor: str
    __typename: Literal["PageInfo"]


class EntityDict(TypedDict):
    """Type for key `entity` in SecondNodeDict."""

    internalId: int


class SecondNodeDict(TypedDict):
    """Type for key `node` in SecondEdgeDict."""

    entity: EntityDict


class SecondEdgeDict(TypedDict):
    """Type for key `edges` in EntitiesDict."""

    node: SecondNodeDict


class EntitiesDict(TypedDict):
    """Type for key `entities` in FirstNodeDict."""

    totalCount: int
    pageInfo: PageInfoDict
    edges: list[SecondEdgeDict]
    __typename: Literal["UserEntityConnection"]


class FirstNodeDict(TypedDict):
    """Type for key `node` in FirstEdgeDict."""

    entities: EntitiesDict


class FirstEdgeDict(TypedDict):
    """Type for key `collections` in CollectionsDict."""

    node: FirstNodeDict


class CollectionsDict(TypedDict):
    """Type for key `collections` in SocialDict."""

    edges: list[FirstEdgeDict]


class SocialDict(TypedDict):
    """Type for key `social` in UserDict."""

    collections: CollectionsDict


class UserDict(TypedDict):
    """Type for key `user` in MeDict."""

    social: SocialDict


class MeDict(TypedDict):
    """Type for key `me` in DataDict."""

    user: UserDict


class DataDict(TypedDict):
    """Type for key `data` in JsonCollectionDict."""

    me: MeDict


class JsonCollectionDict(TypedDict):
    """Type for `response.json()` in `watched.py`."""

    data: DataDict


class VariablesDict(TypedDict):
    """Type for key `variables` in ParamsDict."""

    collectionId: str
    first: int
    after: NotRequired[str]


class ParamsDict(TypedDict):
    """Type for `params` variable in `watched.py`."""

    operationName: Literal["GetCollectionEntities"]
    query: str
    variables: VariablesDict


class PictureDict(TypedDict):
    """Type for key `picture` in ActorDict."""

    id: str
    internalId: int
    url: str
    path: str
    __typename: Literal["InternalImage"]


class TagsDict(TypedDict):
    """Type for key `tags` in ActorDict."""

    list: list[Literal["Person.Gender.Male", "Person.Gender.Female"]]
    __typename: Literal["TagCollection"]


class SeoDict(TypedDict):
    """Type for key `seo` in ActorDict."""

    browsable: bool
    __typename: Literal["Seo"]


class AppearanceStatsDict(TypedDict):
    """Type for key `appearanceStats` in ActorDict."""

    totalMovies: int
    totalSeries: int
    __typename: Literal["PersonAppearanceStats"]


class ActorDict(TypedDict):
    """Type for key `actor` in ActorsDict."""

    internalId: int
    firstName: str
    lastName: str
    gender: Literal["MALE", "FEMALE"] | None
    picture: PictureDict | None
    tags: TagsDict
    seo: SeoDict
    appearanceStats: AppearanceStatsDict
    __typename: Literal["Person"]


class ActorsDict(TypedDict):
    """Type for `response` variable in `set_actors` method of `Film` class."""

    role: str | None
    actor: ActorDict
    __typename: Literal["CastMember"]
