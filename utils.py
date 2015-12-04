# -*- coding: utf-8 -*-
import re
import jieba

chinese_character_pattern = re.compile(ur"([\u4e00-\u9fa5]+)")
# abbr.
CCP = chinese_character_pattern

def extract_chinese(buf):
    """
      extract chinese characters without  
    """
    buffer = buf
    if isinstance(buffer, str):
        buffer = buffer.decode('utf-8')
       
    segment_list = []
    m = CCP.search(buffer)
    while m is not None:
        segment = m.group(1)
        segment_list.append(segment)
        idx = m.start() + len(segment)
        buffer = buffer[idx:]
        m = CCP.search(buffer)
       
    return segment_list

def ClearAndSegment(mes):

    query = mes
    seg_list = ''
    if query is not None:
        query = extract_chinese(query)
        query = ''.join(query)
        seg_list = jieba.cut(query, False)
        seg_list = list(set(seg_list))
        return seg_list
    return seg_list

if __name__ == '__main__':

    liststr = ClearAndSegment(u"赚钱test宝妈tes日赚学生兼职*.@打字员")
    print liststr