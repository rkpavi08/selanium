import asyncio, os
import uvicorn
from quart import Quart





app = Quart(__name__)



port = int(os.environ.get("PORT", 8080))






@app.route('/')
async def hello_world():
   return 'Hello World'




   


  
 
 
