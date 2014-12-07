#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import re

def main():
    with io.open('log.txt', encoding = 'utf-8') as f:
        msg_date = None
        row_count = 0
        concat_line = ''

        for line in f:
            m = re.match('^\s+$', line)
            if m:
                continue

            m1 = re.match('\d+\/\d+\/\d+\(.+\)$', line)
            m2 = re.match('\d+:\d+\s+[^\s]+\s+[^$]+$', line)
            if not (m1 or m2):
                concat_line += line.replace('\n', '')
#                print '---->'
#                print line.encode('utf-8')
#                print '<----'
                continue
#            else:
#                print '---->>'
#                print line.encode('utf-8')
#                print '<<----'

            m = re.match('(\d+:\d+)\s+([^\s]+)\s+([^$]+)$', concat_line)
            if m:
#                print concat_line.encode('utf-8')
                concat_line = ''

                msg_time = m.group(1).encode('utf-8')
                msg_author = m.group(2).encode('utf-8')
                msg_text = m.group(3).encode('utf-8')

                if msg_text.find('[スタンプ]') + msg_text.find('不在着信') + msg_text.find('通話に応答がありませんでした') +  msg_text.find('通話時間') < 0:
                    if not msg_author in msg_count:
                        msg_count[msg_author] = 0
                    if not msg_author in msg_size:
                        msg_size[msg_author] = 0

                    msg_count[msg_author] += 1
                    msg_size[msg_author] += len(msg_text)

            m = re.match('\d+:\d+\s+[^\s]+\s+[^$]+$', line)
            if m:
                concat_line = line.replace('\n', '')
                continue

            m = re.match('(\d+\/\d+\/\d+)\(.+\)$', line)
            if m:
#                print line.encode('utf-8')
                if msg_date:
                    if row_count == 0:
                        row = ''
                        for key, value in msg_count.iteritems():
                            row += ',%s_count,%s_size' % (key.decode('utf-8'), key.decode('utf-8'))
                        print row.encode('utf-8')

                    row = msg_date
                    for key, value in msg_count.iteritems():
                        row += ',%d,%d' % (msg_count[key], msg_size[key])
                    print row

                    row_count += 1

                msg_date = m.group(1).encode('utf-8')
                msg_count = {}
                msg_size = {}
                continue



#                print msg_date + msg_time + ' ' + msg_author + ' '+ msg_text

if __name__ == '__main__':
    main()
