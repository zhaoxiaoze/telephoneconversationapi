from . import State, get_state

class WorkingState(State):


    def run(self, context):

        msg = context.latest_msg()

        if 'state' in msg.entities:
            context.entities['working_state'] = msg.entities['state']
            return get_state("StateAsk").run(context)
        else:
            context.entities['working_state'] = msg.text
            return get_state("StateAsk").run(context)
        return self.utter_default, self