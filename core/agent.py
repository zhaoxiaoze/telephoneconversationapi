from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from rasa_nlu.model import Interpreter
from .context import StateTracker


class Agent(object):
    """
    A context manager for MoveCar chat bot.
    """
    DEFAULT_SENDER_ID = "default"

    def __init__(
        self,
        interpreter
    ):
        """
        Args:
            interpreter (Union[str, Interpreter]): rasa nlu interpreter object
        """
        if type(interpreter) is str:
            self.interpreter = Interpreter.load(Interpreter)
        else:
            self.interpreter = interpreter

        # save the user states in memory
        self.user_store = dict()

    def handle_message(
        self,
        message,
        sender_id='default'
    ):
        """Recieve message from user, change the state of current   
            sender_id ([type], optional): Defaults to Agent.DEFAULT_SENDER_ID. Unique label for a user.
        """
        state_tracker = self._get_user_state_tracker(sender_id)
        message = self._preprocessing(message)
        raw_message = self.interpreter.parse(message)
        response = state_tracker.handle_message(raw_message)

        return response

    def _preprocessing(self, text):
        return text.strip('。')

    def _get_user_state_tracker(self, sender_id):
        if sender_id not in self.user_store:
            tracker = StateTracker(sender_id)
            self.user_store.update({sender_id: tracker})

        return self.user_store.get(sender_id)

    def finish_conversation(self, sender_id):
        """
        Close a conversation, and remove its state_tracker
        """
        if sender_id in self.user_store:
            self.user_store.pop(sender_id)

    def get_user_info(self, uid):
        """Get slots in StateTracker
        """

        if uid not in self.user_store:
            return None

        return self.user_store.get(uid).entities

    def get_logger(self, uid):
        if uid not in self.user_store:
            return None
        return self.user_store.get(uid).get_logger()

    def get_status_code(self, uid):
        if uid not in self.user_store:
            return None
        return self.user_store.get(uid).get_status_code()

    def hang_up(self, uid):
        if uid not in self.user_store:
            return
        self.user_store.get(uid).hang_up()

    def pack_info(self, uid, tel_number):
        if uid not in self.user_store:
            return None
        return self.user_store.get(uid).pack(tel_number)
