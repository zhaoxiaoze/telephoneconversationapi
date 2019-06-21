import time
import random

from . import StatusCode, State, get_state


class StateAsk(State):

    def __init__(self):
        super(StateAsk, self).__init__()
        self.previous_slot = None

    def run(self, context):

        # 获取下一个要填充的槽
        slot = self._get_next_question(context.entities)


        # all slots has been filled, return None
        if slot is None:
            context.package['ask-stamp'].append(
                time.strftime('%Y-%m-%d %H:%M:%S'))
            return self.confirm_info(context), StateConfirmInfo()

        if slot != self.previous_slot:
            self.clear_repeat_times()
            self.previous_slot = slot

            # add ask time stamp
            context.package['ask-stamp'].append(
                time.strftime('%Y-%m-%d %H:%M:%S'))

        # ask next
        action = getattr(self, "utter_ask_" + slot)
        state = self

        # 如果是电话号，进入 StateContact


        # 如果下个问题是车牌颜色，直接判断车牌颜色，或者进入 StatePlateColor




        # 下个问题是车辆位置
        if slot == 'guangzhou':
            state = get_state("LocationPath")

        elif slot =='location':
            state = get_state("StateLocation")

        elif slot =='requestsleave':
            state = get_state("Requestsleave")
        #
        elif slot == 'reason':
            state = get_state("StateReason")

        elif slot == 'job':
            state = get_state("JobState")

        elif slot == 'change_reason':
            state = get_state("JobChanged")

        elif slot == 'working_state':
            state = get_state("WorkingState")

        elif slot == 'health':
            state = get_state('HealthState')

        elif slot == 'hospital_state':
            state = get_state("HospitalState")

        elif slot == 'unhospital_reason':
            state = get_state("UnhospitalReason")

        return action, state



    def _get_next_question(self, entities):
        """Select first empty slot, ask corresponding question.

        Args:
            entities (OrderedDict)
        """
        empty_slots = list(filter(lambda x: entities[x] is None, entities))
        if len(empty_slots) > 0:

            return empty_slots[0]
        else:
            return None

    def confirm_info(self, context):
        """Confirm information to the user

        Args:
            context (StateTracker): StateTracker object of current user
        """
        entities = context.entities
        # car_number = self._get_response_carnumber(entities.get('car_number'))
        # response = "请确认您所告知的信息。您想通知车牌号为%s的%s车牌车辆车主移车。车辆位置是在%s。如果信息正确请您回答是的进行确认，如果信息有误，回答不是将为您转接人工客服解决您的问题。" % (
        #     car_number, entities.get('colour'), entities.get('location'))
        response = '本次电话汇报已经完成，祝您工作顺利、生活愉快。'
        return response




    @property
    def utter_ask_guangzhou(self):
        return '请问您是否在广州市区'

    @property
    def utter_ask_location(self):
        template = [
            "请您提供详细地址"
        ]
        return random.choice(template)

    @property
    def utter_ask_guangzhou(self):
        return "请问您是否在广州市区"

    @property
    def utter_ask_requestsleave(self):
        return "请问您是否有申请外出并获得批准？"

    @property
    def utter_ask_reason(self):
        return "如果未申请获批私自外出，会在本考核周期内被记录扣分并进入档案，请说明外出的原因。"

    @property
    def utter_ask_reason(self):
        template = [
            "如果未申请获批私自外出，会在本考核周期内被记录扣分并进入档案，请说明外出的原因？"
        ]
        return random.choice(template)

    @property
    def utter_ask_job(self):

        return "请问近期工作是否有变动？"

    @property
    def utter_ask_change_reason(self):
        return "请描述工作变动到哪里及变动原因。"

    @property
    def utter_ask_working_state(self):
        return "请描述近期的工作情况。"

    @property
    def utter_ask_health(self):
        return "请问近期个人健康状况是否良好，并且没有就诊、住院、手术、怀孕等情况？"

    @property
    def utter_ask_unhospital_reason(self):
        return "请描述没有及时就诊的原因。"

    @property
    def utter_ask_hospital_state(self):
        return "请描述健康状况及相应的就诊情况。"



class StateConfirmInfo(State):

    def run(self, context):
        """Confirm information to the user
        """
        msg = context.latest_msg()

        # 信息被确认，告诉用户移车请求将被处理
        if msg.intent == "confirm":
            action = self.utter_will_be_deal
            state = get_state("StateFinish", StatusCode.STATUS_NORMAL)
            context.package['answer-stamp'].append(
                time.strftime('%Y-%m-%d %H:%M:%S'))
            context.entities['is_confirm'] = "是"
            context.set_status_code(StatusCode.STATUS_NORMAL)

        # 信息有误，转人工
        elif msg.intent == "deny":
            state = get_state(
                "StateFinish", StatusCode.STATUS_TRANSFER_TO_MANUAL)
            self.turn_to_manual_custom_service(context)
            action = self.utter_info_error
            context.package['answer-stamp'].append(
                time.strftime('%Y-%m-%d %H:%M:%S'))
            context.entities['is_confirm'] = "否"

        else:
            state = self
            action = self.utter_default

        return action, state

    @property
    def utter_will_be_deal(self):
        return "感谢您的来电，再见"

    @property
    def utter_info_error(self):
        return "很抱歉，智能客服未能准确获取您的信息，将为您转接人工客服，请稍等。"

    @property
    def utter_default(self):
        return "我不明白您的意思，如果信息无误请回答是的进行确认，如果信息有误，回答不是将为您转接人工客服处理。"

    def on_finish_state(self, context):
        context.package["count"].append(self.repeat_times)
