import asyncio
import aiohttp
import json

API_KEY = 'AIzaSyDH3oZ0SGs-4MkxRn37hdgGG6Cx9xR2AwQ'




async def getplace(url,bound):
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            ssl=False,
        ),
    ) as session:
        async with session.get(url) as resp:
            response = await resp.json()
            if(len(response['results']) > bound):
                response['results'] = response['results'][0:bound]
            return json.dumps(response, sort_keys=True, indent=4)
                



async def find(lat, long, rad, num):
    latitude = lat
    longitude = long
    loc = "{0},{1}".format(latitude, longitude)
    bound = num
    #print(lat,long,rad,num)
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={0}&location={1}&radius={2}&'.format(API_KEY,loc, rad)
    return await getplace(url,bound)





    

    
    
    