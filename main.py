import telebot
import time
import threading
from config import API_TOKEN
from DML import add_customer_black_list, came_customer_black_list, add_customer
from DQL import get_black_list_list, get_customer_black, check_black_list

telebot.apihelper.API_URL = 'http://tapi.bale.ai/bot{0}/{1}'
bot = telebot.TeleBot(API_TOKEN)

# add your message in line 27,31

find_spam_data = dict()     # {customer_id:[len,time],...}


def find_spam(customer_id, maximum_time=1, maximum_watch=5):
    global find_spam_data
    now = time.time()
    if customer_id not in find_spam_data:
        find_spam_data[customer_id] = [0, time.time()]
    
    if now - find_spam_data[customer_id][1] < maximum_time:
        find_spam_data[customer_id][0] += 1
    else:
        # Reset counter when time window has passed
        find_spam_data[customer_id][0] = 1
        find_spam_data[customer_id][1] = time.time()
    
    if find_spam_data[customer_id][0] >= maximum_watch:
        data = get_customer_black(customer_id)

        if customer_id not in get_black_list_list():
            add_customer_black_list(customer_id, time.time())
            bot.send_message(customer_id, 'level one 1')

        elif data['STAGE'] == 1 and data['DON'] == 'true':
            # BUG FIX: Changed stage from 2 to 3 (next stage after stage 1)
            add_customer_black_list(customer_id, time.time(), 3)
            bot.send_message(customer_id, 'level 2')

        elif data['STAGE'] == 2 and data['DON'] == 'true':
            # BUG FIX: Changed stage from 2 to 3 (next stage after stage 2)
            add_customer_black_list(customer_id, time.time(), 3)
    
    find_spam_data[customer_id][1] = time.time()


def listener(messages):
    for m in messages:
        # print(m)
        try:
            find_spam(m.chat.id)
            if m.content_type == 'text':
                print(f"{m.chat.first_name} [{str(m.chat.id)}]: {m.text}")
            elif m.content_type == 'photo':
                print(f"{m.chat.first_name} [{str(m.chat.id)}]: New photo received")
            elif m.content_type == 'document':
                print(f"{m.chat.first_name} [{str(m.chat.id)}]: New document received")
            elif m.content_type == 'voice':
                print(f"{m.chat.first_name} [{str(m.chat.id)}]: New voice received")
        except Exception as e:
            print(f"Error in listener: {e}")


bot.set_update_listener(listener)


@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        cid = message.chat.id
        name = message.chat.first_name
        add_customer(cid, name)
    except Exception as e:
        print(f"Error in start_handler: {e}")


@bot.message_handler(func=lambda message: True)
def all_message_handler(message):
    try:
        customer_id = message.chat.id
        if check_black_list(customer_id) == False:
            bot.send_message(customer_id, message.text)
        else:
            # it better do not answer
            pass
    except Exception as e:
        print(f"Error in all_message_handler: {e}")


last_clear_time = time.time()


def check_find_spam_status(warning_1=60 * 3, warning_2=36 * 5, sleep_time=60):
    # warning_1=3 minutes, warning_2=3 minutes, sleep_time=one minute
    global last_clear_time
    while True:
        try:
            now = time.time()
            for customer_id in get_black_list_list():
                print('customer_id', customer_id)
                data = get_customer_black(customer_id)  # get customer data from black list table
                print('data', data)

                if data['STAGE'] == 1 and data['DON'] == 'false':
                    if int(now - data['TIME']) >= warning_1:
                        print('came1')
                        came_customer_black_list(customer_id)
                        find_spam_data.pop(customer_id, None)

                elif data['STAGE'] == 2 and data['DON'] == 'false':
                    if int(now - data['TIME']) >= warning_2:
                        came_customer_black_list(customer_id)
                        find_spam_data.pop(customer_id, None)
                        print('came 2')

            
            if now - last_clear_time >= 3600 * 24:
                find_spam_data.clear()
                last_clear_time = time.time()
            
            time.sleep(sleep_time)
        except Exception as e:
            print(f"Error in check_find_spam_status: {e}")
            time.sleep(sleep_time)


t2 = threading.Thread(target=check_find_spam_status, args=())
t2.daemon = True  # Make thread daemon so it stops when main program exits
t2.start()

print('bot_running')
bot.infinity_polling()