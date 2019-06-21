from . import State, StatusCode, get_state

class JobState(State):

    def run(self,context):
        msg = context.latest_msg()

        if msg.intent == 'job_unchanged':

            job_state = 'unchange'
            context.set_entity('job', job_state)
            context.set_entity('change_reason','不需要理由')

            return get_state("StateAsk").run(context)

        elif msg.intent == 'job_changed':

            job_state ='change'
            context.set_entity('job',job_state)

            return  get_state("StateAsk").run(context)

        else:
            return self.utter_default, self