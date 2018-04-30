import requests

class Recipe:
    self.headers ={
    "X-Mashape-Key" : self.api_key,
    "Accept" : "application/json"
    }
    self.endpoint = \
      'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/'
    self.api_key = api_key

    def getJoke(self):
        url = self.endpoint + "food/jokes/random"
        return requests.get(url,headers=self.headers).json()

    def findByIngredients(self, ingredients):
        url = self.endpoint + 'recipes/findByIngredients'
        params = {
        'fillIngredients': False, #Add information about the used and missing ingredients in each recipe.
        'ingredients': ingredients, #string csv ingredient list
        'limitLicense': False,
        'number': 5, #how many recipies to return
        'ranking': 1 #maximize used ingredient
        }

      headers={
      "X-Mashape-Key": self.api_key,
      "Accept": "application/json"
      }

      return requests.get(url, params=params, headers=headers).json()

    def getRandomRecipe(self,preference):#suprise me son!
        url = self.endpoint + "recipes/random"

        params = {
        'limitLicense':false,
        'number':1,
        'tags':pref #csv
        }
        return requests.get(url,params=params,headers=self.headers).json()['recipes']


    def simpleSearch(self,query):
        url = self.endpoint + "recipes/autocomplete"
        params = {
        'number' : 5,
        'query':query
        }
        return requests.get(url,params=params,headers=self.headers).json()

    def getWinePairing(self,food,price):
        url = self.endpoint + "food/wine/pairing"

        params = {
        'food':wine
        'maxPrice': price #int
        }
        #returns a pairing text reply rather than list of wines. SMART!
        return requests.get(url,params=params,headers=self.headers).json()["pairingText"]

    def findByCuisine(self, cuisine):
        url = self.endpoint + "recipes/search"

        params = {
        'number': 5,
        'query': ' ',
        'cuisine': cuisine
        }
        return requests.get(url, params=params, headers=self.headers).json()['results']

    #TODO
    def complexRecipeSerach(self,cuisine,diet,exclude,include,maxkcal,query,type):
        url = self.endpoint + "recipes/searchComplex"

        params = {

        }
        return requests.get(url,params=params,headers=headers).json()['results']

    def getRecipeInfo(self, id):
        url = self.endpoint + "recipes/" + str(id) + "/information"
        params = {'includeNutrition': False } # false for now

        return requests.get(url, params=params, headers=self.headers).json()

    def getRecipeSteps(self, id):
        url = self.endpoint + "recipes/" + str(id) + "/analyzedInstructions"
        params = {'stepBreakdown': True}

        return requests.get(url, params=params, headers=self.headers).json()

    #TODO add some ingredients extraction from text features!
    #TODO possibly add visual flare to steps?
    #TODO convo suggests!
