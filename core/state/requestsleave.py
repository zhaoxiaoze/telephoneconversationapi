from . import State, StatusCode, get_state

class Requestsleave(State):

    def run(self, context):
        msg = context.latest_msg()
        if msg.intent == 'confirm':
            permitting = msg.text
            context.set_entity('requestsleave', permitting)
            reason = '不需要理由'
            context.set_entity('reason', reason)
            return get_state("StateAsk").run(context)

        elif msg.intent == 'deny':
            unpermitting = msg.text
            context.set_entity('requestsleave',unpermitting)
            return get_state("StateAsk").run(context)

