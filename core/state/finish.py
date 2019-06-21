from . import State, StatusCode

class StateFinish(State):

    def __init__(self, statue_code=StatusCode.STATUS_NORMAL):
        super(StateFinish, self).__init__()
        self.statues_code = statue_code

    def run(self, context):
        """Finish conversation. Doing nothing.
        """
        return self.utter_finish, StateFinish()

    def set_status_finish(self, context):
        context.set_status_code(self.statues_code)

    def hang_up(self, context):
        
        # 所有槽被填充，设置状态为正常挂机
        if self._is_slots_filled(context):
            self.set_status_finish(context)

        # 如果上个状态有传递状态码， 设为传递的状态吗
        elif self.statues_code is not None:
            context.set_status_code(self.statues_code)

        # 异常挂机
        else:
            super(StateFinish, self).hang_up(context)

    def _is_slots_filled(self, context):
        """Select first empty slot, ask corresponding question.

        Args:
            entities (OrderedDict)
        """
        empty_slots = list(
            filter(lambda x: context.entities[x] is None, context.entities))
        if len(empty_slots) > 0:

            return False
        else:
            return True

    @property
    def utter_finish(self):
        return "电话已经挂断"