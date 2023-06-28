import requests
import pytest

base_url = "http://127.0.0.1:8000"  

def test_create_dishes():
    dishes = ["orange", "spaghetti", "apple pie"]
    ids = set()
    for dish in dishes:
        response = requests.post(f"{base_url}/dishes", json={"name": dish})
        assert response.status_code == 201
        dish_id = response.json()
        assert dish_id not in ids
        ids.add(dish_id)

def test_get_dish():
    dish_id = 1 #orange was insertted first, thus will have id == 1 
    response = requests.get(f"{base_url}/dishes/{dish_id}")
    assert response.status_code == 200
    dish_data = response.json()
    sodium = dish_data["sodium"]
    assert 0.9 <= sodium <= 1.1

def test_get_all_dishes():
    response = requests.get(f"{base_url}/dishes")
    assert response.status_code == 200
    dishes_data = response.json()
    assert len(dishes_data) == 3

def test_create_invalid_dish():
    response = requests.post(f"{base_url}/dishes", json={"name": "blah"})
    assert response.status_code in [400, 404, 422]
    assert response.json() == -3

def test_same_dish_name():
    dish_name = "orange"
    response = requests.post(f"{base_url}/dishes", json={"name": dish_name})
    assert response.status_code in [400, 404, 422]
    assert response.json() == -2

def test_create_meal():
    appetizer_id = 1  # ID of the "orange" dish
    main_id = 2  # ID of the "spaghetti" dish
    dessert_id = 3  # ID of the "apple pie" dish
    response = requests.post(
        f"{base_url}/meals",
        json={
            "name": "delicious",
            "appetizer": appetizer_id,
            "main": main_id,
            "dessert": dessert_id,
        },
    )
    assert response.status_code == 201
    dish_id = response.json()
    assert dish_id > 0

def test_get_meals():
    response = requests.get(f"{base_url}/meals")
    assert response.status_code == 200
    assert len(response.json()) == 1
    meal = response.json()[0]
    assert 400 <= meal["calories"] <= 500

def test_same_meal_name():
    appetizer_id = 1  # ID of the "orange" dish
    main_id = 2  # ID of the "spaghetti" dish
    dessert_id = 3  # ID of the "apple pie" dish
    response = requests.post(
        f"{base_url}/meals",
        json={
            "name": "delicious",
            "appetizer": appetizer_id,
            "main": main_id,
            "dessert": dessert_id,
        },
    )
    assert response.status_code in [400, 422]
    assert response.json()["code"] == -2