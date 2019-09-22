#!/usr/local/bin/python3

from common import logger
from settings import *


def __send_response(sc, text, channel, thread_ts="",  icon_url='ru', emoji='null'):
    # Required slackclient, channel, thread_ts
    # thread_ts if this is a thread response
    # icon_url to override default, set this to 'emoji' override with an emoji
    # emoji set this to a valid emoji and ensure icon_url='emoji'
    try:
        if "emoji" in icon_url:
            res = sc.api_call('chat.postMessage',
                              username=BOT_NAME,
                              icon_emoji=emoji,
                              as_user='false',
                              channel=channel,
                              text=text,
                              thread_ts=thread_ts)
            if res['ok'] != "True":
                logger("warn", "Error: __send_response API Error: %s" % res['error'])
            logger('info', res)
        else:
            res = sc.api_call('chat.postMessage',
                              username=BOT_NAME,
                              icon_url=icon_url,
                              as_user='false',
                              channel=channel,
                              text=text,
                              thread_ts=thread_ts)
            if res['ok'] != "True":
                logger("warn", "Error: __send_response API Error: %s" % res['error'])
            logger('info', res)

    # KeyError is not going through logger, debug it
    except KeyError as e:
        logger("ignore", str(e) + " error in __send_response.")
    except Exception as e:
        logger("warn", "Unknown error in __send_response: " + str(e))


def __impersonator(sc, text, channel, userpic, username, thread_ts=""):
    try:
        res = sc.api_call('chat.postMessage',
                          username=username,
                          icon_url=userpic,
                          as_user='false',
                          channel=channel,
                          text=text,
                          thread_ts=thread_ts)
        if res['ok'] != "True":
            logger("warn", "Error: __impersonator API Error: %s" % res['error'])
        logger('info', res)
    except KeyError as e:
        logger("ignore", str(e) + " error in __impersonator")
    except Exception as e:
        logger("warn", "Unknown error in __impersonator: " + str(e))


def __send_ephemeral(sc, text, channel, caller):
    try:
        res = sc.api_call('chat.postEphemeral',
                          as_user="true",
                          channel=channel,
                          user=caller,
                          text=text)
        if res['ok'] != "True":
            logger("warn", "Error: __send_ephemeral API Error: %s" % res['error'])
        logger('info', res)
    except KeyError as e:
        logger("ignore", str(e) + " error in __send_ephemeral.")
    except Exception as e:
        logger("warn", "Unknown error in __send_ephemeral: " + str(e))


def __set_topic(sc, new_topic, channel):
    try:
        if channel.startswith("G"):
            res = sc.api_call('groups.setTopic',
                              channel=channel,
                              topic=new_topic)
            if res['ok'] != "True":
                logger("warn", "Error: __send_topic API Error: %s" % res['error'])
            logger('info', res)
        else:
            res = sc.api_call('channels.setTopic',
                              channel=channel,
                              topic=new_topic)
            if res['ok'] != "True":
                logger("warn", "Error: __send_topic API Error: %s" % res['error'])
            logger('info', res)
    except Exception as e:
        logger("warn", "Unknown error in __set_topic: %s" % e)


def __channel_id(sc, channel):
    data = sc.api_call('channels.info',
                       channel=channel,
                       include_locale="true")
    return "#"+data["channel"]["name_normalized"]


def __user_id(sc, user):
    data = sc.api_call('users.info',
                       user=user)
    if not data["user"]["profile"]["display_name"]:
        return data["user"]["profile"]["real_name"]
    else:
        return data["user"]["profile"]["display_name"]


def __reaction(sc, channel, ts, emoji):
    try:
        res = sc.api_call('reactions.add',
                          channel=channel,
                          timestamp=ts,
                          name=emoji)
        if res['ok'] != "True":
            logger("warn", "Error: __reaction API Error: %s" % res['error'])
        logger('info', res)
    except Exception as e:
        logger("warn", "Unknown error in __set_topic: %s" % e)