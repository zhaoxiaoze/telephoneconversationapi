"""Define some conversation util data structure
"""
import re

class StatusCode(object):

    STATUS_IN_PROCESS = -1
    STATUS_NORMAL = 1  # 正常结束，提交工单挂机
    STATUS_HANG_UP_ABNORMALY = 2  # 异常挂机
    STATUS_TRANSFER_TO_MANUAL = 3  #  回答未完成，转人工
    STATUS_HANG_UP_NOT_GUANGDONG = 4  #  不是本地车牌
    STATUS_TRANSFER_TO_MANUAL_ON_START = 5  #  未进入对话流程，直接转人工
    STATUS_HUANG_UP_ON_START = 6  #  未进入对话流程，直接挂机 
    STATUS_HANG_UP_COLOR = 7 # 车牌颜色挂机


class Message(object):
    """Wrapper for message yield from nlu interpreter
    """

    def __init__(
        self,
        raw_message
    ):
        self.intent = raw_message['intent']['name']
        self.entities = {i['entity']: i['value']
                         for i in raw_message['entities']}
        self.text = raw_message['text']
        
        self.state_storage = None

    def get_intent(self):
        return self.intent

    def get_entities(self):
        return self.entities

    def __str__(self):
        return "Raw Test: %s\nIntent: %s\nEntitys:%s\n" % (self.text, self.intent, self.entities)

