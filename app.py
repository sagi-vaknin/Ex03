import requests, json
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)  # initialize Flask
api = Api(app)  # create API

class DishCollection():
    def __init__(self):
        self.dishes = []
        self.id = 1

    def insert(self, dishDict):
        self.dishes.append(dishDict)
        dishes.id += 1

    def findDish(self, key):
        for dish in self.dishes:
            if isinstance(key,int):
                if dish["ID"] == key:
                    return dish,True
            elif isinstance(key,str):
                if dish["name"] == key:
                    return dish,True
                
        return None,False
    
    def removeDish(self,key):
        for dish in self.dishes:
            if isinstance(key,int):
                if dish["ID"] == key:
                    self.dishes.remove(dish)
                    return key
            elif isinstance(key,str):
                if dish["name"] == key:
                   self.dishes.remove(dish)
                   return dish["ID"]
                
        return -9


class Dishes(Resource):

    def post(self): 
        try:
            json_data = request.get_json()
        except:
            return 0,415

        try:
            name = json_data["name"]
        except:
            return -1,422

        for dish in dishes.dishes:
            if dish["name"] == name:
                return -2,422 
            
        dish, status_code = self.api_get_dish_data(name)

        if status_code == 999:
            return -3,422
        
        if status_code != requests.codes.ok:
            return -4,504
                
        dishes.insert(dish)
        
        return dish["ID"],201
        
    def get(self):
        return ({dish["ID"]: dish for dish in dishes.dishes})
    
    def api_get_dish_data(self,name):

        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(name)
        response = requests.get(api_url, headers={'X-Api-Key': 'uYzrvNZEBqKRW1KiDfqHfw==MYbwSlCABmpIQ1iT'})
        temp = json.loads(response.text)
        features = ["name","calories","serving_size_g","sodium_mg","sugar_g"]
        
        if len(temp) > 0:
            dish = {}
            
            if len(temp) == 1:
                dish["name"] = name
                dish["ID"] = dishes.id
                dish["cal"] = temp[0]["calories"]
                dish["size"] = temp[0]["serving_size_g"]
                dish["sodium"] = temp[0]["sodium_mg"]
                dish["sugar"] = temp[0]["sugar_g"]
            elif len(temp) == 2:
                dish["name"] = name
                dish["ID"] = dishes.id
                dish["cal"] = temp[0]["calories"] + temp[1]["calories"]
                dish["size"] = temp[0]["serving_size_g"] + temp[1]["serving_size_g"]
                dish["sodium"] = temp[0]["sodium_mg"] + temp[1]["sodium_mg"]
                dish["sugar"] = temp[0]["sugar_g"] + temp[1]["sugar_g"]

        else:
            return None,999
        
        return dish, response.status_code
    

class Dish(Resource):
    global dishes

    def get(self, id=None, name=None):
        if id:
            dish,b = dishes.findDish(id)
            if dish != None:
                return dish,200
        if name:
            dish,b = dishes.findDish(name)
            if dish != None:
                return dish,200
        if dish == None:
            return -5,404
    
    
    def delete(self,id=None, name=None):
        if id:
            b = dishes.removeDish(id)
            if b != -9:
                meals.updateMeals(id)
                return b,200
        if name:
            b = dishes.removeDish(name)
            if b != -9:
                id,_ = dishes.findDish(name)
                meals.updateMeals(id)
                return b,200
        
        return -5,404


class MealCollection:

    def __init__(self):
        self.meals = []
        self.id = 1

    def insert(self, mealDict):
        self.meals.append(mealDict)
        meals.id += 1

    def findMeal(self,key):
        for meal in self.meals:
            if isinstance(key,int):
                if meal["ID"] == key:
                    return meal,True
            elif isinstance(key,str):
                if meal["name"] == key:
                    return meal,True
                
        return None,False

    def removeMeal(self,key):
        for meal in self.meals:
            if isinstance(key,int):
                if meal["ID"] == key:
                    self.meals.remove(meal)
                    return key
            elif isinstance(key,str):
                if meal["name"] == key:
                   self.meals.remove(meal)
                   return meal["ID"]
                
        return -9
    
    def updateMeals(self, id=None):
        if id:
            for meal in meals.meals:
                if meal["appetizer"] == id or meal["main"] == id or meal["dessert"] == id:
                    meal["sugar"] = None
                    meal["cal"] = None
                    meal["sodium"] = None
                    if meal["appetizer"] == id:
                        meal["appetizer"] = None
                    if meal["main"] == id:
                        meal["main"] = None
                    if meal["dessert"] == id:
                        meal["dessert"] = None
    
        
class Meals(Resource):

    def post(self):
        try:
            json_data = request.get_json()
        except:
            return 0,415

        try:
            name = json_data["name"]  
            appetizerId = json_data["appetizer"]
            mainId = json_data["main"]
            dessertId = json_data["dessert"]
        except:
            return -1,422
        
        for meal in meals.meals:
            if meal["name"] == name:
                return -2,422 
            
        meal, status = self.calc_meal_dict(name,appetizerId,mainId,dessertId)

        if status == -6:
            return -6,422
        
        meals.insert(meal)
        
        return meal["ID"],201
        
    def get(self):
         return ({meal["ID"]: meal for meal in meals.meals})

    def calc_meal_dict(self,name,appetizer,main,dessert):
        
        ids = [appetizer,main,dessert]
        counter = 0
        for id in ids:
            for dish in dishes.dishes:
                if dish["ID"] == id:
                    counter += 1

        if counter != 3:
            return None,-6
        
        mealDict = {}
        mealDict["name"] = name
        mealDict["ID"] = meals.id
        mealDict["appetizer"] = appetizer
        mealDict["main"] = main
        mealDict["dessert"] = dessert
        mealDict["cal"] = sum([dish["cal"] for dish in dishes.dishes for id in ids if dish["ID"] == id])
        mealDict["sodium"] = sum([dish["sodium"] for dish in dishes.dishes for id in ids if dish["ID"] == id])
        mealDict["sugar"] = sum([dish["sugar"] for dish in dishes.dishes for id in ids if dish["ID"] == id])
        
        return mealDict,-1
    

class Meal(Resource):
    global meals

    def get(self, id=None, name=None):
        if id:
            meal,b = meals.findMeal(id)
            if meal != None:
                return meal,200
        if name:
            meal,b = meals.findMeal(name)
            if meal != None:
                return meal,200
        if meal == None:
            return -5,404

    def delete(self,id=None, name=None):
        if id:
            b = meals.removeMeal(id)
            if b != -9:
                return b,200
        if name:
            b = meals.removeMeal(name)
            if b != -9:
                return b,200
        
        return -5,404

    def put(self, id=None):
        for meal in meals.meals:
            if meal["ID"] == id:
                    json_data = request.get_json()

                    if not isinstance(json_data,dict):
                        return -5,404

                    try:
                        name = json_data["name"]  
                        appetizerId = json_data["appetizer"]
                        mainId = json_data["main"]
                        dessertId = json_data["dessert"]
                    except:
                        return -5,404

                    meal["name"] = name
                    meal["appetizer"] = appetizerId
                    meal["main"] = mainId
                    meal["dessert"] = dessertId
                    ids = [appetizerId,mainId,dessertId]
                    meal["cal"] = sum([dish["cal"] for dish in dishes.dishes for id in ids if dish["ID"] == id])
                    meal["sodium"] = sum([dish["sodium"] for dish in dishes.dishes for id in ids if dish["ID"] == id])
                    meal["sugar"] = sum([dish["sugar"] for dish in dishes.dishes for id in ids if dish["ID"] == id])
                    return id,200
            
        return -5,404
        
dishes = DishCollection()       #creating a dishes object
meals = MealCollection()        #creating a meals object

api.add_resource(Dishes, "/dishes")
api.add_resource(Dish, '/dishes/<int:id>', '/dishes/<string:name>')
api.add_resource(Meals, "/meals")
api.add_resource(Meal,'/meals/<int:id>', '/meals/<string:name>')
    

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000, debug=True)
