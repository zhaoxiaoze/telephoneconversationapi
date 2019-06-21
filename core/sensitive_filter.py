import os
import re

here = os.path.abspath(os.path.dirname(__file__))

re_modal = re.compile(r"(喂|呃|嗯|啦|呀|吗|啊|嘛|呢|哦|喔|嘅|噶|吧|喇|哇|咯|咳|哎|嗯哎|吓|到底是哪个啊|喈|随便你吧|那些鬼野|什么鬼|你听不懂吗|不是这个啊|这个都不懂|你那边很小声|，|。| )")
sensitive_words = []
with open(os.path.join(here, 'sensitive.txt'), encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        sensitive_words.append(line)

sensitive_words = "(" + '|'.join(sensitive_words) + ")"

re_sensitive = re.compile(sensitive_words)


def filter_sensitive_words(text):
    """Filter sensitive words in given text.
    
    Args:
        text (str): 
    """
    text = re.sub(re_modal, '', text)
    text = re.sub(re_sensitive, '***', text)

    return text


