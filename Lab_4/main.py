import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb', password='adb2020');

def film_in_category(category_id:int)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego id kategorii.
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(category_id, int):
      return None

    else:
      query = f"""SELECT f.title, lang.name as languge, cat.name as category 
                FROM film f 
                INNER JOIN language lang ON f.language_id = lang.language_id 
                INNER JOIN film_category fcat ON f.film_id = fcat.film_id 
                INNER JOIN category cat ON fcat.category_id = cat.category_id 
                WHERE fcat.category_id = {category_id}"""

      df = pd.read_sql(query, con=connection)
      return df
      
def number_films_in_category(category_id:int)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów w zadanej kategori przez id kategorii.
    Przykład wynikowej tabeli:
    |   |category   |count|
    |0	|Action 	|64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(category_id, int):
      return None

    else:
      query = f"""SELECT cat.name as category, count(fcat.film_id) 
                FROM category cat
                INNER JOIN film_category fcat ON cat.category_id = fcat.category_id 
                WHERE fcat.category_id = {category_id}
                GROUP BY cat.name"""

      df = pd.read_sql(query, con=connection)
      return df

def number_film_by_length(min_length: Union[int,float] = 0, max_length: Union[int,float] = 1e6 ) :
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów o dla poszczegulnych długości pomiędzy wartościami min_length a max_length.
    Przykład wynikowej tabeli:
    |   |length     |count|
    |0	|46 	    |64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    min_length (int,float): wartość minimalnej długości filmu
    max_length (int,float): wartość maksymalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(min_length, (int, float)):
      return None

    elif not isinstance(max_length, (int, float)):
      return None
    
    elif min_length > max_length:
      return None

    else:
      query = f"""SELECT f.length, count(f.film_id) 
                FROM film f
                WHERE f.length between {min_length} and {max_length}
                GROUP BY f.length"""

      df = pd.read_sql(query, con=connection)
      return df

def client_from_city(city:str)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o listę klientów z zadanego miasta przez wartość city.
    Przykład wynikowej tabeli:
    |   |city	    |first_name	|last_name
    |0	|Athenai	|Linda	    |Williams
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    city (str): nazwa miaste dla którego mamy sporządzić listę klientów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(city, str):
      return None

    else:
      query = f"""SELECT c.city, cust.first_name, cust.last_name 
                FROM customer cust
                INNER JOIN address a ON cust.address_id = a.address_id
                INNER JOIN city c ON a.city_id = c.city_id 
                WHERE c.city = '{city}'"""

      df = pd.read_sql(query, con=connection)
      return df

def avg_amount_by_length(length:Union[int,float])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o średnią wartość wypożyczenia filmów dla zadanej długości length.
    Przykład wynikowej tabeli:
    |   |length |avg
    |0	|48	    |4.295389
    
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    length (int,float): długość filmu dla którego mamy pożyczyć średnią wartość wypożyczonych filmów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(length, (int, float)):
      return None

    else:
      query = f"""SELECT f.length, avg(p.amount)
                FROM film f
                INNER JOIN inventory i ON f.film_id = i.film_id
                INNER JOIN rental r ON i.inventory_id = r.inventory_id 
                INNER JOIN payment p ON r.rental_id = p.rental_id
                WHERE f.length = {length}
                GROUP BY f.length"""

      df = pd.read_sql(query, con=connection)
      return df

def client_by_sum_length(sum_min:Union[int,float])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o sumaryczny czas wypożyczonych filmów przez klientów powyżej zadanej wartości .
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |sum
    |0  |Brian	    |Wyman  	|1265
    
    Tabela wynikowa powinna być posortowane według sumy, imienia i nazwiska klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    sum_min (int,float): minimalna wartość sumy długości wypożyczonych filmów którą musi spełniać klient
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(sum_min, (int, float)):
      return None

    if sum_min < 0:
      return None

    else:
      query = f"""SELECT c.first_name, c.last_name, sum(f.length)
                FROM customer c
                INNER JOIN rental r ON c.customer_id = r.customer_id
                INNER JOIN inventory i ON r.inventory_id = i.inventory_id 
                INNER JOIN film f ON i.film_id = f.film_id
                GROUP BY c.first_name, c.last_name
                HAVING sum(f.length) > {sum_min}
                ORDER BY sum(f.length), c.last_name"""

      df = pd.read_sql(query, con=connection)
      return df

def category_statistic_length(name:str)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o statystykę długości filmów w kategorii o zadanej nazwie.
    Przykład wynikowej tabeli:
    |   |category   |avg    |sum    |min    |max
    |0	|Action 	|111.60 |7143   |47 	|185
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    name (str): Nazwa kategorii dla której ma zostać wypisana statystyka
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(name, str):
      return None

    else:
      query = f"""SELECT cat.name as category, avg(f.length), sum(f.length), min(f.length), max(f.length)
                FROM category cat
                INNER JOIN film_category fcat ON cat.category_id = fcat.category_id
                INNER JOIN film f ON fcat.film_id = f.film_id 
                WHERE cat.name = '{name}'
                GROUP BY cat.name"""

      df = pd.read_sql(query, con=connection)
      return df