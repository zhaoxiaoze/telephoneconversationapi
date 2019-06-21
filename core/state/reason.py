import time

from . import State, get_state


class StateReason(State):

    def run(self, context):
        msg = context.latest_msg()

        if 'reason' in msg.entities:
            context.entities['reason'] = msg.entities['reason']
            # add 'car_number time stamp'
            context.package['answer-stamp'].append(
                time.strftime('%Y-%m-%d %H:%M:%S'))
            return get_state("StateAsk").run(context)
        else:
            context.entities['reason'] = msg.text
            # add 'car_number time stamp'
            context.package['answer-stamp'].append(
                time.strftime('%Y-%m-%d %H:%M:%S'))
            return get_state("StateAsk").run(context)

        return self.utter_default, self

    def on_finish_state(self, context):
        context.package["count"].append(self.repeat_times)