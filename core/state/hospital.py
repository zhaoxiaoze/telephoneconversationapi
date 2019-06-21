from .import State,get_state


class HospitalState(State):

    def run(self, context):
        msg = context.latest_msg()

        if 'unhospital' in msg.entities:
            context.set_entity('hospital_state',"没去就医")
            return get_state("StateAsk").run(context)

        else:
            context.entities['hospital_state']=msg.intent['state']
            context.set_entity('unhospital_reason',"不需要")
            return get_state("StateAsk").run(context)

        return self.utter_default, self

