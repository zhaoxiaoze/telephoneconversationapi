import time

from . import State, StatusCode, get_state


class InitState(State):

    def run(self, context):
        response = self.utter_is_ok
        next_state = StateConfirm()
        context.package['ask-stamp'].append(time.strftime('%Y-%m-%d %H:%M:%S'))

        return response, next_state


class StateConfirm(State):

    def run(self, context):
        msg = context.latest_msg()

        # if len(msg.entities) != 0:
        #     if 'car_number' in msg.entities:
        #         return get_state("StateCarNumber").run(context)
        #
        #     if 'colour' in msg.entities:
        #         return get_state("StatePlateColor").run(context)


        if msg.intent == 'confirm':
            next_state = get_state("StateAsk")
            context.package['answer-stamp'].append(
                time.strftime('%Y-%m-%d %H:%M:%S'))
            context.entities['is_ok'] = "是的"
            return next_state(context)

        elif msg.intent == 'deny':
            next_state = get_state("StateFinish", StatusCode.STATUS_TRANSFER_TO_MANUAL_ON_START) 
            response = self.utter_not_move_car
            context.set_status_code(
                StatusCode.STATUS_TRANSFER_TO_MANUAL_ON_START)
            context.entities['is_ok'] = "不是"
            context.package['answer-stamp'].append(
                time.strftime('%Y-%m-%d %H:%M:%S'))

        else:
            next_state = self
            response = "我不明白您的意思，您是否方便，请您回答是的或不是。"

        return response, next_state

    def hang_up(self, context):
        """用户在开始时挂断
        """
        context.statues_code = StatusCode.STATUS_HUANG_UP_ON_START

    # def on_process_message(self, msg):
    #     super(StateConfirm, self).on_process_message(msg)
    #     for i in  ['订票', '挂号', '进度', '查']:
    #         if i in msg.text:
    #             msg.intent = 'deny'

    @property
    def utter_not_move_car(self):
        return "好的，我会在1个小时之后再次联系您进行电话汇报，请提前安排好时间。"

    def on_finish_state(self, context):
        context.package["count"].append(self.repeat_times)

    def turn_to_manual_custom_service(self, context):
        # TODO add specific operation here
        context.set_status_code(StatusCode.STATUS_TRANSFER_TO_MANUAL_ON_START)
        return self.utter_transfer_artificial
