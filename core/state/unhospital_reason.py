from . import State, get_state

class UnhospitalReason(State):

    def run(self, context):

        msg = context.latest_msg()

        if msg.intent =='inform_reason':
            context.entities['unhospital_reason'] = msg.entities['reason']
            return get_state("StateAsk").run(context)
        else:
            context.entities['unhospital_reason'] = msg.text
            return get_state("StateAsk").run(context)

        return self.utter_default, self