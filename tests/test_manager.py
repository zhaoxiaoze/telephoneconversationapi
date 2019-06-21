import pytest

# 你可以在列表中添加自己的测试用例，每个用例的测试日志将会记录在 log/tests/ 文件夹中, 编号顺序与测试用例顺序相同
test_cases = [[
    "你好",
    "是的",
    "粤A-12345",
    "字母",
    "对蓝牌车",
    "长沙市神农大酒店",
    "挡住我了",
    "是本机",
    "对没错"
]]

def test_dialogue(dialogue_manager):
    for i, case in enumerate(test_cases):
        user_id = str(i)
        for text in case:
            dialogue_manager.chat(text, uid=user_id)
        
        dialogue_manager.get_pack(user_id, user_id)


    