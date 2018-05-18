from botocore.vendored import requests
import json



HEADERS={
"X-Mashape-Key" : '8yTX11t4Mfmshwa9o1sbifmmmE5jp1lWBZejsnkTReTtyXV4Ow',
"Accept" : "application/json"
}
ENDPOINT = \
'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/'
API_KEY = '8yTX11t4Mfmshwa9o1sbifmmmE5jp1lWBZejsnkTReTtyXV4Ow'

def getJoke():
  url = ENDPOINT + "food/jokes/random"
  return requests.get(url,headers=HEADERS).json()

def findByIngredients(ingredients):
  url = ENDPOINT + 'recipes/findByIngredients'
  params = {
  'fillIngredients': False, #Add information about the used and missing ingredients in each recipe.
  'ingredients': ingredients, #string csv ingredient list
  'limitLicense': False,
  'number': 5, #how many recipies to return
  'ranking': 1 #maximize used ingredient
  }
  headers={
  "X-Mashape-Key": API_KEY,
  "Accept": "application/json"
  }
  return requests.get(url, params=params, headers=headers).json()

def getRandomRecipe(pref=""):#suprise me son!
  url = ENDPOINT + "recipes/random"

  params = {
  'limitLicense':'false',
  'number':1,
  'tags':pref #csv
  }
  return requests.get(url,params=params,headers=HEADERS).json()['recipes']

def info(id):
  url = ENDPOINT + "recipes/{}/information".format(id)
  params = {'includeNutrition': False }
  return requests.get(url,params=params,headers=HEADERS).json()

def steps(id):
    url = ENDPOINT + "recipes/{}/analyzedInstructions".format(id)
    params = {'stepBreakdown': True}
    return requests.get(url, params=params, headers=HEADERS).json()
    
def simpleSearch(query):
  url = ENDPOINT + "recipes/search"
  params = {
  'number': 1,
  'query': query,
  }
  return requests.get(url,params=params,headers=HEADERS).json()['results']

def getWinePairing(food,price):
  url = ENDPOINT + "food/wine/pairing"

  params = {
  'food':wine,
  'maxPrice': price #int
  }
  #returns a pairing text reply rather than list of wines. SMART!
  return requests.get(url,params=params,headers=HEADERS).json()["pairingText"]

def findByCuisine(cuisine):
  url = ENDPOINT + "recipes/search"
  params = {
  'number': 1,
  'query': '',
  'cuisine': cuisine
  }
  return requests.get(url, params=params, headers=HEADERS).json()['results']

#TODO
def complexRecipeSerach(cuisine,diet,exclude,include,maxkcal,query,type):
  url = ENDPOINT + "recipes/searchComplex"

  params = {

  }
  return requests.get(url,params=params,headers=HEADERS).json()['results'





    #TODO add some ingredients extraction from text features!
    #TODO possibly add visual flare to steps?
    #TODO convo suggests!
