#!/usr/bin/env python3
# Simple Discord SelfBot
# Created By Viloid ( github.com/vsec7 )
# Use At Your Own Risk

import requests, sys, yaml

class Discord:

    def __init__(self, t):
        self.base = "https://discord.com/api/v9"
        self.auth = { 'authorization': t }
    
    def getMe(self):
        u = requests.get(self.base + "/users/@me", headers=self.auth).json()
        return u
    
    def joinGuild(self, c):
        u = requests.post(self.base + "/invites/" + str(c), headers=self.auth, json={}).json()
        return u

    def leaveGuild(self, i):
        u = requests.delete(self.base + "/users/@me/guilds/" + str(i), headers=self.auth)
        return u

def main():
    with open('config.yaml') as cfg:
        conf = yaml.load(cfg, Loader=yaml.FullLoader)

    if not conf['MODE']:
        print("[!] Please provide MODE : join / leave at config.yaml!")
        sys.exit()

    if not conf['BOT_TOKEN']:
        print("[!] Please provide discord token lists at config.yaml!")
        sys.exit()

    if conf['MODE'] == "join":
        if not conf['JOIN_CODE']:
            print("[!] Please provide JOIN_CODE / INVITE CODE at config.yaml!")
            sys.exit()

        for token in conf['BOT_TOKEN']:
            try:
                Bot = Discord(token)
                me = Bot.getMe()['username'] + "#" + Bot.getMe()['discriminator']
                join = Bot.joinGuild(conf['JOIN_CODE'])

                if not join:
                    print("[Error] Invalid Invite Code")
                    sys.exit()
                else:
                    inv = join['inviter']['username'] + '#' + join['inviter']['discriminator']
                    server = join['guild']['name']
                    print("[{}][INVITER: {}][JOINED: {}]".format(me, inv, server))
                    
            except:
                    print(f"[Error] {token} : INVALID TOKEN / KICKED FROM GUILD!")
    
    elif conf['MODE'] == "leave":
        if not conf['LEAVE_GUILD_ID']:
            print("[!] Please provide LEAVE_GUILD_ID / SERVER ID at config.yaml!")
            sys.exit()

        for token in conf['BOT_TOKEN']:
            try:
                Bot = Discord(token)
                me = Bot.getMe()['username'] + "#" + Bot.getMe()['discriminator']
                leave = Bot.leaveGuild(conf['LEAVE_GUILD_ID'])
                print("[{}][LEAVE: {}]".format(me, conf['LEAVE_GUILD_ID']))

            except:
                    print(f"[Error] {token} : INVALID TOKEN / KICKED FROM GUILD!")

    else:
        print("[!] Please provide MODE : join / leave at config.yaml!")
        sys.exit()

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(f"{type(err).__name__} : {err}")
        