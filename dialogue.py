import os
import openai
import time
from datetime import datetime
import requests
import re
try:
    import gnureadline as readline
except ImportError:
    import readline

now = datetime.now()

# Arguments
import argparse
parser = argparse.ArgumentParser(description = 'A simple ChatGPT dialogue console app.')
parser.add_argument('--noClear', '-NC', action = 'store_true',
                    help = 'The app will not clear the console.')
parser.add_argument('--debug', '-D', action = 'store_true',
                    help = 'Debug mode. Dialogues will not be saved. Output full log after conversation.')
parser.add_argument('--DomesticCheck', '-DC', action = 'store_true',
                    help = 'Call Domestic IP Checker. Only available in debug mode.')
parser.add_argument('--IntlCheck', '-IC', action = 'store_true',
                    help = 'Call International IP Checker. Only available in dubug mode.')
parser.add_argument('--no-check-api-usage', '-NU', action = 'store_false', dest = 'check_api_usage', default = True,
                    help = 'Skip checking API Usage. Only available in debug mode.')
parser.add_argument('--dialogue-path', '-DP', action = 'store', dest = 'dialogue_path', default = "dialogues",
                    help='Relative path to save dialogue. Default value is \"dialogues\"')
parser.add_argument('--model', '-M', action = 'store', dest = 'model_selection', default = "gpt-3.5-turbo",
                    help='The model you would like to use. Default value is \'gpt-3.5-turbo\'.')
args = parser.parse_args()
vargs = vars(args)

# API key and model
openai.api_key = os.getenv("OPENAI_API_KEY") or input("input your openai api key.\n")
openai.api_base= os.getenv("OPENAI_API_ADDRESS") or "https://opai.ous50.moe/v1"
model_selection = os.getenv("CHATGPT_MODEL") or args.model_selection

def check_or_create_folder(folder_path):
    CHECK_FOLDER = os.path.isdir(folder_path)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(folder_path)
        print("created folder : ", folder_path)

def get_current_domestic_country():
    url = 'https://myip.ipip.net'
    # payload = open("request.json")
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.get(url, headers=headers)
    x = re.findall("来自.*", r.text)
    # print("From domestic ip checker:")
    print(x)

def get_current_proxy_country():

    url = 'http://ip.bi'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'User-Agent': 'curl/7.88.1'}
    r = requests.get(url, headers=headers)
    x = re.findall("Country.*", r.text)
    # print("From international ip checker:")
    print(x)

# Clear console 
if args.noClear==False:
    os.system("clear")

# Check API usage
def check_api_usage():
    r = openai.api_requestor.APIRequestor()
    resp = r.request("GET", '/usage?date=' + now.strftime('%F'))
    # resp_object = resp[0]
    print("Your API Usage: " + str(resp[0].data["current_usage_usd"]) + " USD.")

# Check if API endpoint can be reached or not.
def check_api_availability():
    r = requests()

# Debug actions
if args.debug == True:
    for x in vargs:
        print(x + ": " + str(vargs[x]))
    if args.DomesticCheck == True:
        get_current_domestic_country()
    if args.IntlCheck == True:
        get_current_proxy_country()
    if args.check_api_usage == True:
        check_api_usage()
    



# Multiline input
def multi_input(user_message):
    try:
        #This list will hold all inputs made during the loop
        lst_words = []
        # We will store the final string results on this variable
        final_str ='' 
        #Let's ask first the user to enter the amount of fruits
        print(user_message)
        
        #Loop to get as many words as needed in that list
        while True:
            #Capture each word o'er here, pals!
            wrd = input()
            lst_words.append(wrd)

    finally:
        #If the list has at least one element, let us print it on the screen
        if(len(lst_words)>0):
            #Before printing this list, let's create the final string based on the elements of the list
            final_str = '\n'.join(lst_words)
            return final_str
        else:
            print("Nothing is entered.")



# Opening a dialogue file
if args.debug == False:
    dialogue_path = os.getenv("CHAT_LOGPATH") or args.dialogue_path
    check_or_create_folder(dialogue_path)
    dialogue_starting_time = now.strftime("%F_%H-%M-%S")
    log = open(dialogue_path + "/" + dialogue_starting_time + ".md","w")



# main 
sys_prompt = os.getenv("CHATGPT_SYS_PROMPT") or "You’re a kind helpful assistant"
messages = [
 {"role": "system", "content" : sys_prompt}
]

print("Enter/Paste your content. Press enter and then Ctrl-D or Ctrl-Z ( windows ) to submit. \n")


while True:
    content = multi_input("User: ")
    if content=="":
        print("Nothing is entered. Retype your prompt.")
        continue
    if content=="exit()":
         break 
    if args.debug == False:
        log.write("**User:"+ content + "**\n")
    messages.append({"role": "user", "content": content})

    print("Waiting for the response...")

    start_time = time.time()

    completion = openai.ChatCompletion.create(
        model=model_selection,
        messages=messages
    )
    if args.debug == True:
        print("Execution time is: " + str(time.time() - start_time))

    chat_response = completion.choices[0].message.content
    print(f'ChatGPT: {chat_response}')
    if args.debug == False:
        log.write("ChatGPT:"+ chat_response + "\n")
    messages.append({"role": "assistant", "content": chat_response})

if args.debug:
    print(messages)
else:
    log.close()