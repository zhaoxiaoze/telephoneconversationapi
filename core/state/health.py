from . import State, get_state


class HealthState(State):
    def run(self, context):
        msg = context.latest_msg()

        if msg.intent == 'health':
            unhospital_reason = '不需要理由'
            context.set_entity('health',msg.intent)
            context.set_entity('unhospital_reason',unhospital_reason)
            context.set_entity('hospital_state',"不需要")
            return get_state("StateAsk").run(context)

        elif msg.intent =='unhealth':
            context.set_entity('health',msg.intent)

            return get_state("StateAsk").run(context)

        return self.utter_ask_health, self


    def utter_ask_health(self):
        return "我不懂您的意思，如果您最近没有就诊、住院、手术、怀孕等情况，请您回答健康，否则回答身体有状况。"