import random
import re

class State(object):
    """Base class of bot state
    """
    
    RE_DENEY = re.compile('(不不|不是|不对|错)')
    RE_CONFIRM = re.compile('(恩|对|要|是的|确认|没问题|没错)')
    RE_PUNCTUATION = re.compile("[.!//_,$&%^*()<>+\"'?@#:~{}——！\\\\，。=？、：“”‘’《》【】￥……（）]")

    def __init__(self):
        self.repeat_times = 1

    def __call__(self, context):
        """Yield next state for bot

        Args:
            context (StateTracker): a conversation state manager
        """
        msg = context.latest_msg()
        # deal with some common cases

        # 调侃
        if msg.intent == 'tune':
            return self.utter_default, self

        self.on_process_message(msg)

        self.on_enter_state(context)

        ac, st = self.run(context)

        if st == self:
            self.repeat_times += 1
        else:
            self.on_finish_state(context)

        if self.repeat_times > 2:
            ac, st = self.turn_to_manual_custom_service(context), StateFinish()

        return ac, st

    def run(self, context):
        raise NotImplementedError(
            "You must implement __call__ method in sub class")

    def clear_repeat_times(self):
        self.repeat_times = 0

    def hang_up(self, context):
        context.statues_code = StatusCode.STATUS_HANG_UP_ABNORMALY

    @property
    def utter_default(self):
        template = [
            "很抱歉，我没听清楚，您能再说一遍吗？"
        ]
        return random.choice(template)

    def turn_to_manual_custom_service(self, context):
        # TODO add specific operation here
        context.set_status_code(StatusCode.STATUS_TRANSFER_TO_MANUAL)
        return self.utter_transfer_artificial

    @property
    def utter_is_ok(self):
        return "XXX（姓名）您好，我是XXX司法局社区矫正电话客服小智，现在依据社区矫正监管要求对您发起电话汇报业务，请问现在是否方便进行电话汇报？"

    @property
    def utter_transfer_artificial(self):
        return "很抱歉，智能客服未能准确获取您的信息，将为您转接人工客服，请稍等。"

    def on_enter_state(self, context):
        pass

    def on_finish_state(self, context):
        pass

    def on_process_message(self, msg):
        """Define rules to process msg. Implement in subclass if neccessery.
        """
        # 过滤标点符号
        msg.text = re.sub(self.RE_PUNCTUATION, '', msg.text)

        # deny
        deny = self.RE_DENEY.findall(msg.text)
        if len(deny) != 0:
            msg.intent = 'deny'
        
        # confirm
        confirm = self.RE_CONFIRM.findall(msg.text)
        if len(confirm) != 0:
            msg.intent = 'confirm'

import sys
thismodule = sys.modules[__name__]


def get_state(state_name, *args, **kwargs):
    return getattr(thismodule, state_name)(*args, **kwargs)


from ..status import StatusCode
from .start import InitState
from .ask_info import StateAsk
from .location import StateLocation
from .reason import StateReason
from .finish import StateFinish
from .locationpath import LocationPath
from .requestsleave import Requestsleave
from .job import JobState
from .job_change_reason import JobChanged
from .working_state import WorkingState
from .health import HealthState
from .unhospital_reason import UnhospitalReason
from .hospital import HospitalState


def get_init_state():
    return InitState()



