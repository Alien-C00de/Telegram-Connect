import argparse
import asyncio
import os
from time import perf_counter
from configparser import ConfigParser
from colorama import Fore, Style
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# This class is used to get the authorization from Telegram
class get_authorization():
    def __init__(self) -> None:
        pass
    
    # Create client connection
    async def get_client(self):

        try:
             # Reading Configs
            config = ConfigParser()
            current_directory =  os.getcwd()
            config_path =  os.path.join(current_directory, "config/config.ini")
            # config_path = pathlib.Path(__file__).parent.absolute() / "config/config.ini"
            config.read(config_path)

            'Telegram' in config
            api_id = config['Telegram']['api_id'] 
            api_hash =  config['Telegram']['api_hash'] 
            api_hash = str(api_hash)
            phone = config['Telegram']['phone'] 

            client = TelegramClient(phone, api_id, api_hash)
            await client.connect()

            if not await client.is_user_authorized():
                await tclient.send_code_request(phone)
                os.system('clear')
                await client.sign_in(phone, input(Fore.GREEN + Style.BRIGHT  + "[+] Enter the verification code: " + Fore.RESET + Style.RESET_ALL))

            return client
        
        except KeyError:
            msg = "[-] " + "Authorization Error: Please check required details are correct.\n" 
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
        except Exception as EX:
            await client.sign_in(password=input('Password: '))
            msg = "[-] " + "Authorization Error:" + str(EX)
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)

# This class is used to connect to the Telegram & Join the Channel
class Connect():
    
    def __init__(self) -> None:
        pass
    
    # Check if the user is authorized
    async def __authorized(self):
        auth = get_authorization()
        client = await auth.get_client()
        return client
    
    # Retrieve the entity from the channel & check if the channel is valid
    async def __retrieve_entity(self, client, _target):
        entity = None
        try:
            entity = await client.get_entity(_target)
            return entity
        except Exception as exx:
            try:
                group  = int(_target)
                entity = await client.get_entity(group)
                return entity
            except:
                pass
            pass
        if not entity:
            try:
                entity = await client.get_entity(PeerChannel(_target))
                return entity
            except Exception as exx:
                pass
        if not entity:
            try:
                entity = await client.get_entity(PeerChat(_target))
                return entity
            except Exception as exx:
                pass
        return entity
    
    # This function is used to join the channel
    async def __Join_Channel(self, client, entity):
        result = await client(JoinChannelRequest(channel = entity.id))

        # print(result.stringify())
        if result == "ChannelInvalidError":
            print (Fore.RED + Style.BRIGHT + "Invalid Channel" + Fore.RESET + Style.RESET_ALL)
        
        # Check if you have joined the channel
        participants = await client(GetParticipantsRequest(entity.id, ChannelParticipantsSearch(''), 0, 100, hash=0))
        me = await client.get_me()
        if any(user.id == me.id for user in participants.users):
            msg = f"[+] Successfully Joined {Fore.YELLOW}{Style.BRIGHT}{entity.title}{Fore.GREEN}{Style.BRIGHT} Channel!"
            print(Fore.GREEN + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
        else:
            msg = "[-] " + "Failed to join the channel.\n, "
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)

    # This function is used to connect to the single group
    async def __Connect_Me(self, client, channel):
        entity  = await self.__retrieve_entity(client, channel)
        
        if entity is None:
            msg = f"[-] Error: Cannot Find {Fore.YELLOW}{Style.BRIGHT}{channel}{Fore.RED}{Style.BRIGHT} Channel"
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            pass
        else:
            await self.__Join_Channel(client, entity)

    # Public function to connect to the single group
    async def connect_to_single_groups(self, channel):
        client = await self.__authorized()
        await self.__Connect_Me(client, channel)
        
    # Public function to connect to the multiple groups
    async def connect_to_multi_group(self, group_list):
        client = await self.__authorized()

        with open(group_list, "r") as group_file:
            for group in group_file.readlines():
                await self.__Connect_Me(client, group.strip())

# Main function to execute the code
async def Main():
    
    # Parser to take the arguments
    parser = argparse.ArgumentParser(description="Python Tool: Telegram Group Connect")
    parser.add_argument("-s", "--Group_Single_Connect", help="Option To Join Single Group e.g. python tele_connect.py -s group_name")
    parser.add_argument("-m", "--Group_Multi_Connect", help="Option To Join Multi Group e.g. python tele_connect.py -m group_list.txt")
    parser.add_argument("-v", "--version", help="show tool version", action="store_true")
    args = parser.parse_args()

    start_time = perf_counter()

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print(Fore.CYAN + Style.BRIGHT + f"""\n
 _____     _                                    ___                            _   
/__   \___| | ___  __ _ _ __ __ _ _ __ ___     / __\___  _ __  _ __   ___  ___| |_ 
  / /\/ _ \ |/ _ \/ _` | '__/ _` | '_ ` _ \   / /  / _ \| '_ \| '_ \ / _ \/ __| __|
 / / |  __/ |  __/ (_| | | | (_| | | | | | | / /__| (_) | | | | | | |  __/ (__| |_ 
 \/   \___|_|\___|\__, |_|  \__,_|_| |_| |_| \____/\___/|_| |_|_| |_|\___|\___|\__|
                  |___/                                                            
        \n""" + Fore.RESET + Style.RESET_ALL)

    try:
        if args.Group_Single_Connect:
            print(f"[!] Single Channel Connect : Channel Name -> {args.Group_Single_Connect.strip()}", flush=True)
            connect = Connect()
            await connect.connect_to_single_groups(args.Group_Single_Connect.strip())

        elif args.Group_Multi_Connect:
            print(f"[!] Multi Channel Connect : File Name -> {args.Group_Multi_Connect.strip()}", flush=True)
            connect = Connect()
            await connect.connect_to_multi_group(args.Group_Multi_Connect.strip())
            
        elif args.help:
            print(Fore.GREEN + Style.BRIGHT + f"[*] Usage: Telegram_Connect.py [-S For_Single_Group -m Multi_Group] [-v VERSION] [-h HELP]")
            print(Fore.GREEN + Style.BRIGHT + f"[*] Options:")
            print(Fore.GREEN + Style.BRIGHT + f"        -s, --Please provide the name of the group to connect.")
            print(Fore.GREEN + Style.BRIGHT + f"        -m, --Please provide the list of groups in txt file to connect.")
            print(Fore.GREEN + Style.BRIGHT + f"        -v, --version  Show program version")
            print(Fore.GREEN + Style.BRIGHT + f"        -h, --help Show this help message and exit")
            print(Fore.GREEN + Style.BRIGHT + f"[*] To execute code using the Python interpreter - python Telegram_Connect.py -s <group name> -m <list of groups in txt file>")
            print(Fore.GREEN + Style.BRIGHT + f"[*] To execute code using the Telegram_Connect.exe - Report_Generator -s <group name> -m <list of groups in txt file>")
            print(Fore.GREEN + Style.BRIGHT + f"[*] Check the version - python Telegram_Connect.py -v\n")
            
        elif args.version:
            print(Fore.BLUE + Style.BRIGHT + f"[*] A Python tool For Generating Automated Assessment Report.\n[*] Version: 1.0\n")
            print(Fore.YELLOW + Style.BRIGHT + f"[#] Author - Alien.C00de\n")
        else:
            print("usage: python Telegram_Connect.py [-s Group Name] [-m List of Groups in txt File] [-v VERSION] [-h HELP]") 
    except Exception as ex:
        error_msg = str(ex)
        msg = "[-] " + "Main Error: Reading Error, " + error_msg
        print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
        
    print(Fore.BLUE + Style.BRIGHT + f"\n[+] Total Time Taken: {round(perf_counter() - start_time, 2)} Seconds.", flush=True)
    print(Style.RESET_ALL)

if __name__ == '__main__':
    asyncio.run(Main())
