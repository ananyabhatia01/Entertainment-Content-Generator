from langchain_core.tools import tool

@tool
def fetch_trending_movies() -> list[str]:
    """
    Fetches a list of currently trending movies.
    Use this tool when you need to find out what movies are popular right now.
    """
    return ["Inception", "Interstellar", "The Dark Knight", "Dune", "Oppenheimer"]

@tool
def get_movie_metadata(movie_name: str) -> dict:
    """
    Fetches metadata for a specific movie title.
    Returns a dictionary containing the year, director, and genre.
    """
    database = {
        "Inception": {"year": 2010, "director": "Christopher Nolan", "genre": "Sci-Fi"},
        "Interstellar": {"year": 2014, "director": "Christopher Nolan", "genre": "Sci-Fi"},
        "The Dark Knight": {"year": 2008, "director": "Christopher Nolan", "genre": "Action"},
        "Dune": {"year": 2021, "director": "Denis Villeneuve", "genre": "Sci-Fi"},
        "Oppenheimer": {"year": 2023, "director": "Christopher Nolan", "genre": "Biography"}
    }
    return database.get(movie_name, {"info": f"No metadata found for {movie_name}."})

@tool
def write_movie_review(movie_name: str, metadata: str) -> str:
    """
    Generates a creative review for a movie based on its name and metadata.
    Provide the movie name and metadata as a string.
    """
    return f"A stunning masterpiece by its director. {movie_name} is a must-watch for any cinema lover! Metadata context: {metadata}"

@tool
def generate_publishing_schedule(reviews: list[str]) -> str:
    """
    Organizes a list of movie reviews into a weekly publishing schedule.
    Pass in a list of review strings.
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    schedule = []
    for i, review in enumerate(reviews):
        day = days[i % len(days)]
        schedule.append(f"{day}: {review}")
    return "\n".join(schedule)
