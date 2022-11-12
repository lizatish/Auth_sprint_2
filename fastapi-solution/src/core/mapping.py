from api.v1 import films, genres, persons

mapping = {
    'ANONYMOUS': [
        films.router.url_path_for('films_scope'),
        films.router.url_path_for('film_details', film_id=None),

        genres.router.url_path_for('genres_list'),
        genres.router.url_path_for('genre_details', genre_id=None),

        persons.router.url_path_for('films_by_person', person_id=None),
        persons.router.url_path_for('person_details', person_id=None),
    ],
    'STANDARD': [
        films.router.url_path_for('films_scope'),
        films.router.url_path_for('film_search'),
        films.router.url_path_for('film_details', film_id=None),

        genres.router.url_path_for('genres_list'),
        genres.router.url_path_for('genre_details', genre_id=None),

        persons.router.url_path_for('films_by_person', person_id=None),
        persons.router.url_path_for('person_details', person_id=None),
        persons.router.url_path_for('search_persons'),
    ],
    'PRIVILEGED': [
        films.router.url_path_for('films_scope'),
        films.router.url_path_for('film_search'),
        films.router.url_path_for('film_details', film_id=None),

        genres.router.url_path_for('genres_list'),
        genres.router.url_path_for('genre_details', genre_id=None),

        persons.router.url_path_for('films_by_person', person_id=None),
        persons.router.url_path_for('person_details', person_id=None),
        persons.router.url_path_for('search_persons'),
    ],
    'ADMIN': [
        films.router.url_path_for('films_scope'),
        films.router.url_path_for('film_search'),
        films.router.url_path_for('film_details', film_id=None),

        genres.router.url_path_for('genres_list'),
        genres.router.url_path_for('genre_details', genre_id=None),

        persons.router.url_path_for('films_by_person', person_id=None),
        persons.router.url_path_for('person_details', person_id=None),
        persons.router.url_path_for('search_persons'),
    ],
}
