import time

from . import State, StatusCode, get_state


class LocationPath(State):

    def run(self, context):
        msg = context.latest_msg()

        if msg.intent == 'confirm':

            guangzhou = msg.text
            context.set_entity('guangzhou',guangzhou )
            context.set_entity('requestsleave','不需要请假')
            context.set_entity('reason','不需要理由')

            return get_state("StateAsk").run(context)

        elif msg.intent =='deny':

            guangzhou = msg.text
            context.set_entity('guangzhou',guangzhou)

            return get_state("StateAsk").run(context)

        return self.utter_get_response, self


    @property
    def utter_get_response(self):
        return "我不明白您的意思，您是否在广州，请您回答是或者不是"