from tsww_api import *

client = TaskSystem('yourToken')

tg = client.get_users()

print(tg)
