# -*- coding: utf-8 -*-

import jieba

s=u'周冬雨真帅'
        
seg=jieba.cut(s)
print '/'.join(seg)