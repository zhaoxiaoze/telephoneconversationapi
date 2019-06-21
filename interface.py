"""
Additional interface for question match
"""
import os
import sys
import re
import requests
import json
import time

from pprint import pprint as print

from rasa_nlu.model import Interpreter


dir_path = os.path.dirname(os.path.abspath(__file__))
if dir_path not in sys.path:
    sys.path.append(dir_path)

from core import Agent as MyAgent


class User(object):

    def __init__(self, uid):
        self.uid = uid
        self.status = 0


class DialogueManager(object):

    def __init__(self, log_dir=os.path.join(dir_path, 'log')):
        self.user_dict = dict()
        tmp = os.curdir
        os.chdir(dir_path)
        interpreter = self.interpreter = Interpreter.load(
            'models/default/model_20190514-121130')
        os.chdir(tmp)
        self.agent = MyAgent(interpreter)
        self.log_dir = log_dir

    def chat(self, text, uid):
        """chat with user

        Args:
            text (str): user reply
            id (str): user id to manage dialogue

        Returns:
            str: bot response string
        """
        if uid not in self.user_dict.keys():
            user = User(uid)
            self.user_dict[uid] = user

        user = self.user_dict.get(uid)

        response = self.agent.handle_message(text, uid)
        return response

    def get_response_json(self, text, uid):

        response = self.chat(text, uid)
        ret = {
            'build': uid,
            'answer': response
        }

        # TODO patch here
        if self.agent.get_status_code(uid) == 1:
            ret.update(self.agent._get_user_state_tracker(uid).get_ask_answer_content())
        return ret

    def finish_chat(self, uid, tel_number, record_log=True):

        if record_log:

            log = self.get_log(uid)
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S')
            user_dir = os.path.join(self.log_dir, tel_number)

            if not os.path.isdir(user_dir):
                os.makedirs(user_dir)
            with open(os.path.join(user_dir, cur_time + '.txt'), 'wb') as f:
                if log is not None:
                    f.write(log.encode('utf-8'))
        # remove user from DialogueManager
        if uid in self.user_dict.keys():

            self.user_dict.pop(uid)

        self.agent.finish_conversation(uid)

    def get_info(self, uid):
        return self.agent.get_user_info(uid)

    def get_status_code(self, uid):
        return self.agent.get_status_code(uid)

    def hang_up(self, uid):
        self.agent.hang_up(uid)

    def get_log(self, uid):
        return self.agent.get_logger(uid)

    def get_pack(self, uid, tel_number):
        pack = self.agent.pack_info(uid, tel_number)
        self.finish_chat(uid, tel_number)
        return pack


def main():
    
    user_id = '123455'
    manager = DialogueManager()

    while True:
        reply = input()
        if reply == 'finish':
            print(manager.get_pack(user_id, '15637899910'))
            continue
        response = manager.chat(reply, user_id)
        print(response)


if __name__ == '__main__':
    main()
