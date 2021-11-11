import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb', password='adb2020');


def film_in_category(category: Union[int, str]) -> pd.DataFrame:
    """ Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli categry jest int
        - name: jeżeli category jest str, dokładnie taki jak podana wartość
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|

    Tabela wynikowa ma być posortowana po tylule filmu i języku.

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.

    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)  dla którego wykonujemy zapytanie

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    if not isinstance(category, (int, str)):
        return None

    else:
        if isinstance(category, int):
            query = f"""SELECT f.title, lang.name as languge, cat.name as category 
                        FROM film f 
                        INNER JOIN language lang ON f.language_id = lang.language_id 
                        INNER JOIN film_category fcat ON f.film_id = fcat.film_id 
                        INNER JOIN category cat ON fcat.category_id = cat.category_id 
                        WHERE fcat.category_id = {category}"""

        if isinstance(category, str):
            query = f"""SELECT f.title, lang.name as languge, cat.name as category 
                        FROM film f 
                        INNER JOIN language lang ON f.language_id = lang.language_id 
                        INNER JOIN film_category fcat ON f.film_id = fcat.film_id 
                        INNER JOIN category cat ON fcat.category_id = cat.category_id 
                        WHERE cat.name = '{category}'"""

        df = pd.read_sql(query, con=connection)

        if df.empty:
            return pd.DataFrame(columns=['title', 'languge', 'category'])
        else:
            return df

    
def film_in_category_case_insensitive(category: Union[int, str]) -> pd.DataFrame:
    """
    Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli categry jest int
        - name: jeżeli category jest str
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|

    Tabela wynikowa ma być posortowana po tylule filmu i języku.

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.

    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)  dla którego wykonujemy zapytanie

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    if not isinstance(category, (int, str)):
        return None

    else:
        if isinstance(category, int):
            query = f"""SELECT f.title, lang.name as languge, cat.name as category 
                        FROM film f 
                        INNER JOIN language lang ON f.language_id = lang.language_id 
                        INNER JOIN film_category fcat ON f.film_id = fcat.film_id 
                        INNER JOIN category cat ON fcat.category_id = cat.category_id 
                        WHERE fcat.category_id = {category}"""

        if isinstance(category, str):
            query = f"""SELECT f.title, lang.name as languge, cat.name as category 
                        FROM film f 
                        INNER JOIN language lang ON f.language_id = lang.language_id 
                        INNER JOIN film_category fcat ON f.film_id = fcat.film_id 
                        INNER JOIN category cat ON fcat.category_id = cat.category_id 
                        WHERE cat.name ILIKE '{category}'"""

        df = pd.read_sql(query, con=connection)

        if df.empty:
            return pd.DataFrame(columns=['title', 'languge', 'category'])
        else:
            return df


def film_cast(title: str) -> pd.DataFrame:
    """ Funkcja zwracająca wynik zapytania do bazy o obsadę filmu o dokładnie zadanym tytule.
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |
    |0	|Greg       |Chaplin    |

    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.

    Parameters:
    title (int): wartość id kategorii dla którego wykonujemy zapytanie

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    if not isinstance(title, str):
        return None

    else:
        query = f"""SELECT a.first_name, a.last_name
                    FROM film f 
                    INNER JOIN film_actor fa ON f.film_id = fa.film_id 
                    INNER JOIN actor a ON fa.actor_id = a.actor_id
                    WHERE f.title = '{title}'
                    GROUP BY a.first_name, a.last_name
                    ORDER BY a.last_name"""

        df = pd.read_sql(query, con=connection)

        if df.empty:
            return pd.DataFrame(columns=['first_name', 'last_name', 'category'])
        else:
            return df
    

def film_title_case_insensitive(words: list):
    """ Funkcja zwracająca wynik zapytania do bazy o tytuły filmów zawierających conajmniej jedno z podanych słów z listy words.
    Przykład wynikowej tabeli:
    |   |title              |
    |0	|Crystal Breaking 	|

    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.

    Parameters:
    words(list): wartość minimalnej długości filmu

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    if not isinstance(words, list):
        return None

    else:
        words_str = '|'.join(words)
        query = f"""SELECT title
                    FROM film
                    WHERE title ~* '(?:^| )({words_str})""" + """{1,}(?:$| )'
                    ORDER BY title"""

        df = pd.read_sql(query, con=connection)

        if df.empty:
            return pd.DataFrame(columns=['title'])
        else:
            return df
