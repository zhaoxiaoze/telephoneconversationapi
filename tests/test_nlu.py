import pytest

intent_test_case = [
    ("是的", 'confirm'),
    ("不是", 'deny'),
    ("绿色", 'inform_colour'),
    ("那个车在神农大酒店", "inform_location"),
    ("粤A-23456", 'inform_car_number'),
    ("那个车挡住我了", 'inform_reason'),
    ("15637899910", 'inform_contact')
]

@pytest.mark.parametrize("user_request, intent",intent_test_case)
def test_intent(nlu_interpreter, message, user_request, intent):
    nlu_result = nlu_interpreter.parse(user_request)
    msg = message(nlu_result)
    assert msg.intent == intent


entity_test_case = [
    ("绿色车牌", {"colour": "绿色"}),
    ("车牌号是粤A-SDK23", {"car_number": "粤A-SDK23"}),
    ("那个车在神农大酒店", {"location": "神农大酒店"}),
    ("电话号码是13460636838", {"contact": "13460636838"})
]

@pytest.mark.parametrize("user_request, entities", entity_test_case)
def test_entities_recog(nlu_interpreter, message, user_request, entities):
    nlu_result = nlu_interpreter.parse(user_request)
    msg = message(nlu_result)

    for (k_, v_), (k, v) in zip(msg.entities.items(), entities.items()):
        assert k_ == k
        assert v_ == v
