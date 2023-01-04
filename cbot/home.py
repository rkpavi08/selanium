
import os, re, inspect, base64, asyncio, math, traceback,uuid,mimetypes


from telethon import TelegramClient, events, functions
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.sessions import StringSession
from pyrogram import Client as pclient
from telethon import events, errors
from telethon.tl.custom import Button

ustring = os.environ.get("ustring")

if ustring:
  user = TelegramClient(StringSession(ustring),1754367,'231b8cc6cca12ee51a85cf543321f476')
else:
  user = None

botstring = os.environ.get("token")

if not botstring:
  print("add token in env")
  botstring = "5894592896:AAGpNNxRRIC5PXN-Z_gJ0zj_SBFNu7VzJuQ"
  #quit()


tbot = TelegramClient('bot', 1754367, '231b8cc6cca12ee51a85cf543321f476').start(bot_token=botstring)
pbot = pclient("my_bot",api_id=1754367,api_hash="231b8cc6cca12ee51a85cf543321f476",bot_token=botstring)

loop = tbot.loop #asyncio.new_event_loop()

helpc = {}
cmd = {}
adm = ['710844948']


def handler(**args):
  pattern = args.get('pattern', None) 
  CallbackQuery = args.get('CallbackQuery', None) 
  admin = args.get('admin', None) 
  if CallbackQuery:
       del args["CallbackQuery"] 
  if admin:
       del args["admin"]
  cr = (os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]) 
  def run(func):
   async def rk(event):
     task = asyncio.current_task()
     tname = task.get_name()
     ssd = await event.get_sender()
     sender = str(ssd.id)
     if admin:
        if not sender in adm:
           return await event.reply("`This command is For Admins Only`")
     if not  CallbackQuery: 
      if event.fwd_from or event.via_bot_id:
         return
      x = str(await event.get_sender())
      if not x.startswith("User"):
        return
      if not sender in adm:
        await event.client.forward_messages(-1001688309029, event.message)
      if not await checkuser(sender):
        await event.client.send_message(-1001688309029, f'Blocked `{str(ssd.first_name)}~>` @{str(ssd.username)}')
        return await event.reply("**Join my update channel to use me**",buttons=[[Button.url("Click here to Join", "https://t.me/cjsjsbot_updates")]])  
      
      if not sender in adm and not "/ctask" in pattern:
       xc = await istask(sender)
       if xc > 1:
         return await event.reply("**[Stopped]** `You already have 2 running tasks please wait untill compleate or type` /ctask `to cancel your all running tasks`")
     task.set_name(f"{sender}-{tname}")
     tname = task.get_name()
     try:
      await func(event)        
     except errors.rpcerrorlist.MessageIdInvalidError:
      await event.reply("`ERROR My message has been deleted, cancelled your task...`")
     except errors.rpcerrorlist.UserIsBlockedError:
      return
     except:
      await event.reply(f"`An unexpected error occurred during process {tname}`")
      await error(f"`{str(pattern)}-{tname}`\n{traceback.format_exc()}")
      return 
   cmd.setdefault(cr, []).append(rk)  
   if CallbackQuery:
      tbot.add_event_handler(rk, events.CallbackQuery(**args)) 
   else:  
      tbot.add_event_handler(rk, events.NewMessage(**args)) 
   return rk 
  return run


async def istask(id):   
  x = 0
  for task in asyncio.all_tasks():
    if id in task.get_name():
       x = x + 1
  return x


async def error(msg):
  msg = str(msg)
  if len(msg) < 4090:
     await tbot.send_message(-1001743587073,message=msg)
  else:
     with open("error.txt", "w+") as f:
         f.write(text)         
     await tbot.send_file(-1001743587073,file="error.txt")
     os.remove("error.txt")           
     return


async def checkuser(user):
  try:
   result = await tbot(functions.channels.GetParticipantRequest(-1001766984885, int(user)))
   return True
  except Exception as e:
   return False

 

