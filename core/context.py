import json


from .state import get_init_state
from .status import Message, StatusCode
from .sensitive_filter import filter_sensitive_words
from collections import OrderedDict

class StateTracker(object):
    """A container for saving conversation state 
    """

    def __init__(
        self,
        user_id
    ):
        self.entities = OrderedDict(
            is_ok=None,
            guangzhou=None,
            requestsleave=None,
            location=None,
            reason=None,
            job=None,
            change_reason=None,
            working_state=None,
            health=None,
            hospital_state = None,
            unhospital_reason=None


        )
        self.user_id = user_id

        # Current state of bot
        self.current_state = get_init_state()

        # record state history
        self.state_recorder = list()

        # record user msg
        self.msg_recorder = list()

        self.response_recorder = list()

        self.is_number_plate_confirm = False

        self.statues_code = -1

        # packge for State record infomation (include question, answer, time_stamp)
        self.package = {
            "build": self.user_id,
            "ask-stamp": [],
            "answer-stamp": [],
            "ask-content": [],
            "answer-content": [],
            "count": [],
            "status": StatusCode.STATUS_IN_PROCESS
        }

    def set_entity(self, name, value, apply_filter=False):
        value = filter_sensitive_words(value)
        self.entities[name] = value


    def handle_message(self, message):

        # update slots
        msg = Message(message)
        self.msg_recorder.append(msg)
        self.state_recorder.append(self.current_state.__class__.__name__)

        response, self.current_state = self.current_state(self)

        self.response_recorder.append(response)

        return response

    def latest_msg(self):
        return self.msg_recorder[-1]

    def get_empty_slot(self):
        # get slots not been filled
        empty_slots = list(
            filter(lambda x: self.entities[x] is None, self.entities))
        return empty_slots

    def get_status_code(self):
        return self.statues_code

    def get_logger_dict(self):
        result = dict()
        result['entities'] = self.entities

        states = list()
        # states = [msg.__class__.__name__ for msg in self.msg_recorder]
        for _, msg, response in zip(self.state_recorder, self.msg_recorder, self.response_recorder):
            states.append(OrderedDict(
                user_response=msg.text,
                user_intent=msg.intent,
                entities=msg.entities,
                bot_response=response,
            ))
        result['state_tracker'] = states

        return result

    def get_logger(self):
        log_dict = self.get_logger_dict()
        str_builder = ""
        
        # build entities
        str_builder += "Entities:\n"
        for k, v in log_dict['entities'].items():
            str_builder += '\t%s: %s\n' % (k, v)

        # build state tracker
        str_builder += "\n\nStateTracker:\n\n"
        for i, item in enumerate(log_dict['state_tracker']):
            str_builder += "Round %d: \n" % i
            str_builder += "User_Response: %s. \n" % item.get('user_response')
            str_builder += "User_Intent: %s. \n" % item.get('user_intent')
            str_builder += "Entities: \n"
            for k, v in item.get('entities').items():
                str_builder += '\t%s: %s.\n' % (k,v)
            str_builder += "Bot_Response: %s. \n" % item.get('bot_response')
            str_builder += '\n'

        return str_builder

    def set_status_code(self, code):
        self.statues_code = code

    def pack(self, tel_number):
        """
        Pack current conversation. Include question, answer, time_stamp
        """
        self.package['ask-content'] = []
        self.package['answer-content'] = []
        for key, value in self.entities.items():
            if value is not None:
                # TODO patch here
                if key == 'contact' and value == '本机':
                    value = tel_number
                self.package['ask-content'].append(key)
                value = filter_sensitive_words(value)
                self.package['answer-content'].append(value)

        self.package["status"] = self.statues_code
        return self.package

    def get_ask_answer_content(self):
        ret = dict()
        ret['ask-content'] = []
        ret['answer-content'] = []

        for key, value in self.entities.items():
            if value is not None:
                ret['ask-content'].append(key)
                value = filter_sensitive_words(value)
                ret['answer-content'].append(value)

        return ret

    def hang_up(self):
        self.current_state.hang_up(self)
