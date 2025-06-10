"""Create the home page of the streamlit app."""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import list_films, list_persons


def create_hist_numbers(
    df_films: pd.DataFrame,
    value: str,
    mean: bool = False,
    hist_title: str | None = None,
) -> None:
    """
    Create a histogram with numerical values in x-axis.

    Parameters
    ----------
    df_films : pd.DataFrame
        DataFrame with watched movies data.
        Required columns: value, title.
    value : str
        Column we want in x axis, must be numerical.
        For example "year" or "duration".
    mean : bool, optional
        True to add a line for the mean value of x axis. The default is False.
    hist_title : str, optional
        Title of the histogram.
        The default is None, title will be created with value.

    Returns
    -------
    None.

    """
    # Count films by year
    df_count = df_films.groupby(value).size().reset_index(name="number")
    # Add an infotip to the dataframe
    df_count["hover_text"] = df_count[value].apply(
        lambda val: f"{value.title()}: {val}<br>Films: "
        f"{df_count[df_count[value] == val]['number'].values[0]}<br>"
        + "<br>".join(df_films[df_films[value] == val]["title"].head(5))
    )

    hist_title = hist_title or f"Films by {value}"

    fig = px.bar(
        df_count,
        x=value,
        y="number",
        title=hist_title,
        height=500 if "rating" not in value else 400,
        hover_name="hover_text",
        hover_data={value: False, "number": False, "hover_text": False},
    )
    # Change label
    fig.update_layout(
        xaxis_title=value.title(),
        yaxis_title="Number of films",
        dragmode="zoom",
    )
    if mean:  # If we add the mean
        mean_value = df_films[value].mean()
        fig.add_vline(
            x=mean_value,
            line_dash="dash",
            line_color="#0068C9",
            annotation_text=f"Mean: {mean_value:.3g}",
            annotation_position="top",
        )
    if "rating" in value:  # If it is a rating chart, values are from 0 to 5
        fig.update_xaxes(range=[0, 5.05])

    # Add graph in streamlit
    chart = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

    if chart["selection"]["points"]:
        bar = chart["selection"]["points"][0]["x"]
        if value == "duration":
            st.session_state["details_title"] = f"{bar} min"
        else:
            st.session_state["details_title"] = bar
        st.session_state["details_films"] = df_films[df_films[value] == bar]
        st.switch_page("src/details_page.py")


def create_hist_categories(
    df_categories: pd.DataFrame,
    categories: str,
    df_films: pd.DataFrame,
    id_: str,
) -> None:
    """
    Create a histogram with literal values in x-axis.

    Parameters
    ----------
    df_categories : pd.DataFrame
        DataFrame with data for each category.
        Required columns: categories, id_, number.
    categories : str
        Type of data to plot, in singular. For example, country or genre.
    df_films : pd.DataFrame
        DataFrame with watched movies data.
        Required columns: plural of categories, title.
    id_ : str
        Column of df_categories which is used in df_films to save data.
        For example, in df_films, genres are save with their ID but
        countries are saved with their french name.

    Returns
    -------
    None.

    """
    # Plural of the word categories
    plural = (
        categories + "s" if categories[-1] != "y" else categories[:-1] + "ies"
    )
    df_categories["hover_text"] = df_categories.apply(
        lambda row: f"{categories.title()}: {row[categories]}"
        f"<br>Films: {row['number']}<br>"
        + "<br>".join(
            df_films[df_films[plural].str.contains(str(row[id_]))][
                "title"
            ].head(5)
        ),
        axis="columns",
    )

    fig = px.bar(
        df_categories,
        x=categories,
        y="number",
        title=f"Films by {categories}",
        height=500,
        hover_name="hover_text",
        hover_data={categories: False, "number": False, "hover_text": False},
    )
    # Change label
    fig.update_layout(
        xaxis_title=categories.title(),
        yaxis_title="Number of films",
        xaxis={"tickangle": 315},  # Orientation
        dragmode="zoom",
    )
    # Add graph in streamlit
    chart = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

    if chart["selection"]["points"]:
        bar = chart["selection"]["points"][0]["x"]
        st.session_state["details_title"] = bar
        st.session_state["details_films"] = df_films[
            df_films[plural].str.contains(
                str(
                    df_categories[df_categories[categories] == bar][id_].iloc[
                        0
                    ]
                )
            )
        ]
        st.switch_page("src/details_page.py")


def create_map(df_countries: pd.DataFrame, df_films: pd.DataFrame) -> None:
    """
    Create a map with movies watched by country.

    Parameters
    ----------
    df_countries : pd.DataFrame
        DataFrame with number of films watched by country.
        Required columns: country_en and number.
    df_films : pd.DataFrame
        DataFrame with watched movies data.
        Required columns: plural of categories, title.

    Returns
    -------
    None.

    """
    fig = px.choropleth(
        df_countries,
        locations="country_en",
        locationmode="country names",
        color="number",
        hover_name="hover_text",
        hover_data={
            "country_en": False,
            "number": False,
            "hover_text": False,
        },
        color_continuous_scale=["#83C9FF", "#0068C9"],
        title="Films by country",
        labels={"number": "Number of films"},
    )
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="#303C44",
        showocean=True,
        oceancolor="#14181C",
        showframe=False,
        showcountries=True,
        countrycolor="black",
        countrywidth=0.5,
    )
    fig.update_layout(
        coloraxis_showscale=False,  # Delete colorbar
        height=500,
        margin={"t": 40},
    )

    chart = st.plotly_chart(
        fig,
        use_container_width=True,
        config={"scrollZoom": False},
        on_select="rerun",
    )

    if chart["selection"]["points"]:
        country = (
            chart["selection"]["points"][0]["hovertext"]
            .split("<br>")[0]
            .replace("Country: ", "")
        )
        st.session_state["details_title"] = country
        st.session_state["details_films"] = df_films[
            df_films["countries"].str.contains(country)
        ]
        st.switch_page("src/details_page.py")


def create_progression(award: str, title: str, df_films: pd.DataFrame) -> None:
    """
    Create a pie chart showing ratio of watched movies for a specific award.

    Parameters
    ----------
    award : str
        Name of the award. For example Césars, Oscars or Palmes.
    title : str
        Title of the pie chart.
    df_films : pd.DataFrame
        DataFrame with watched movies data.
        Required columns: id, title.

    Returns
    -------
    None.

    """
    df_award = pd.read_csv(f"csv/{award.lower().replace("é", "e")}.csv")

    watched = df_award[df_award["id"].isin(df_films["id"])]["title"].tolist()
    not_watched = df_award[~df_award["id"].isin(df_films["id"])][
        "title"
    ].tolist()

    # Text in tooltip
    watched_str = (
        f"Number: {len(watched)}<br>" + "<br>".join(map(str, watched[:5]))
        or "None"
    )
    not_watched_str = (
        f"Number: {len(not_watched)}<br>"
        + "<br>".join(map(str, not_watched[:5]))
        or "None"
    )

    # DataFrame used for the chart
    df_pie = pd.DataFrame(
        {
            "category": ["Watched", "Not watched"],
            "number": [len(watched), len(not_watched)],
            "hover_text": [watched_str, not_watched_str],
        }
    )

    # Create the donut chart
    fig = px.pie(
        df_pie,
        values="number",
        names="category",
        hole=0.6,
        title=title,
        hover_name="hover_text",
        hover_data={"category": False, "number": False, "hover_text": False},
    )

    chart = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

    if chart["selection"]["points"]:
        country = (
            chart["selection"]["points"][0]["hovertext"]
            .split("<br>")[0]
            .replace("Country: ", "")
        )
        st.session_state["details_title"] = country
        st.session_state["details_films"] = df_films[
            df_films["countries"].str.contains(country)
        ]
        st.switch_page("src/details_page.py")


def create_progression_countries(
    df_countries: pd.DataFrame, countries_not_watched: list[str]
) -> None:
    """
    Create a pie chart with the ratio of countries with one watched movie.

    Parameters
    ----------
    df_countries : pd.DataFrame
        DataFrame with number of films watched by country.
        Required columns: country.
    countries_not_watched : list[str]
        List of french country names without any watched movie.

    Returns
    -------
    None.

    """
    watched = df_countries["country"].tolist()
    not_watched = countries_not_watched

    # Text in tooltip
    watched_str = (
        f"Number: {len(watched)}<br>" + "<br>".join(map(str, watched[:5]))
        or "None"
    )
    not_watched_str = (
        f"Number: {len(not_watched)}<br>"
        + "<br>".join(map(str, not_watched[:5]))
        or "None"
    )

    # DataFrame used for the chart
    df_pie = pd.DataFrame(
        {
            "category": ["Watched", "Not watched"],
            "number": [len(watched), len(not_watched)],
            "hover_text": [watched_str, not_watched_str],
        }
    )

    # Create the donut chart
    fig = px.pie(
        df_pie,
        values="number",
        names="category",
        hole=0.6,
        title="Countries with a watched film",
        hover_name="hover_text",
        hover_data={"category": False, "number": False, "hover_text": False},
    )

    st.plotly_chart(fig, use_container_width=True)


def create_scatter_ratings(df_films: pd.DataFrame) -> None:
    """
    Create a scatter of audience rating by press rating.

    Parameters
    ----------
    df_films : pd.DataFrame
        DataFrame with watched movies data.
        Required columns: press rating, spectator rating.

    Returns
    -------
    None.

    """
    df_count = (
        df_films.groupby(["press rating", "spectator rating"])
        .size()
        .reset_index(name="number")
    )

    fig = px.scatter(
        df_count,
        x="press rating",
        y="spectator rating",
        size="number",
        size_max=5,  # Max size of a point
        title="Spectator ratings in function of press ratings",
        labels={
            "press rating": "Press Rating",
            "spectator rating": "Spectator Rating",
        },
        hover_name="number",
        hover_data={
            "press rating": False,
            "spectator rating": False,
            "number": False,
        },
        height=400,
    )

    # Improve layout
    fig.update_layout(
        xaxis={"range": [0, 5.05]},
        yaxis={"range": [0, 5.05]},
        xaxis_title="Press Rating",
        yaxis_title="Spectator Rating",
        dragmode="zoom",
    )

    # Show the chart in Streamlit
    chart = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

    if chart["selection"]["points"]:
        press = chart["selection"]["points"][0]["x"]
        spectator = chart["selection"]["points"][0]["y"]
        st.session_state["details_title"] = (
            f"Press: {press:.3g} - Spectator: {spectator:.3g}"
        )
        st.session_state["details_films"] = df_films[
            (df_films["press rating"] == press)
            & (df_films["spectator rating"] == spectator)
        ]
        st.switch_page("src/details_page.py")


def create_home() -> None:
    """
    Create the streamlit home page.

    Returns
    -------
    None.

    """
    df_films = st.session_state["df_films"]
    df_countries = pd.read_csv("csv/countries.csv").sort_values(
        "number", ascending=False
    )
    countries_not_watched = df_countries[df_countries["number"] == 0][
        "country"
    ].tolist()
    df_countries = df_countries[df_countries["number"] != 0]
    df_genres = pd.read_csv("csv/genres.csv").sort_values(
        "number", ascending=False
    )
    df_genres = df_genres[df_genres["number"] != 0]
    df_actors = pd.read_csv("csv/actors.csv").sort_values(
        "number", ascending=False
    )
    df_directors = pd.read_csv("csv/directors.csv").sort_values(
        "number", ascending=False
    )

    st.title("Film Statistics")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(label="Films", value=len(df_films))
    with col2:
        st.metric(label="Hours", value=round(df_films["duration"].sum() / 60))
    with col3:
        st.metric(label="Countries", value=len(df_countries))
    with col4:
        st.metric(label="Actors", value=len(df_actors))
    with col5:
        st.metric(label="Directors", value=len(df_directors))

    # Films by year
    create_hist_numbers(df_films, "year")

    # Films by genre
    create_hist_categories(df_genres, "genre", df_films, "id")

    # Films by country
    create_hist_categories(df_countries, "country", df_films, "country")

    # Map films by country
    create_map(df_countries, df_films)

    # Film by duration
    create_hist_numbers(df_films, "duration", True)

    # Progressions
    col1, col2 = st.columns(2, gap="small")
    with col1:
        create_progression(
            "Césars", "Watched César Awards for Best Film", df_films
        )
    with col2:
        create_progression(
            "Oscars", "Watched Oscar Awards for Best Film", df_films
        )

    col1, col2 = st.columns(2, gap="small")
    with col1:
        create_progression("Palmes", "Watched Palmes d'Or", df_films)
    with col2:
        create_progression_countries(df_countries, countries_not_watched)

    # Ratings
    col1, col2 = st.columns(2)
    with col1:
        create_hist_numbers(df_films, "spectator rating", True)
    with col2:
        create_hist_numbers(df_films, "press rating", True)
    col1, col2 = st.columns(2)
    with col1:
        create_hist_numbers(
            df_films[df_films["press rating"].isna()],
            "spectator rating",
            True,
            "Films without press rating by spectator rating",
        )
    with col2:
        create_scatter_ratings(df_films)

    st.subheader("Most watched directors")
    list_persons(df_directors.head(9), "home_directors")

    st.subheader("Most watched actors")
    list_persons(df_actors.head(9), "home_actors")

    st.subheader("Last watched films")
    list_films(df_films.head(3), "home_films")


if __name__ == "__main__":
    create_home()
