#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import re


class Messages:
    def __init__(self):
        self.clear()
        self.messages = []
        self.keys = []

    def clear(self):
        self.current_date = None
        self.current_time = None
        self.current_author = None
        self.current_text = None

    def push(self):
        if self.current_text:
            self.messages.append({
                'date': self.current_date,
                'time': self.current_time,
                'author': self.current_author,
                'text': self.current_text
            })
            self.keys = list(set(self.keys + [self.current_author]))

    def parse_lines(self, lines):
        for line in lines:
            # skip void lines
            if re.match('^\s+$', line):
                continue
                
            # parse date of the day
            m = re.match('(\d+\/\d+\/\d+)\(.+\)$', line)
            if m:
                self.current_date = m.group(1).encode('utf-8')
                continue

            # parse each talk
            m = re.match('(\d+:\d+)\s+([^\s]+)\s+([^$]+)$', line)
            if m:
                assert self.current_date
                self.push()

                self.current_time = m.group(1).encode('utf-8')
                self.current_author = m.group(2).encode('utf-8')
                self.current_text = m.group(3).encode('utf-8')
            else:
                # concatenate multi-line talks
                assert self.current_time
                assert self.current_author
                assert self.current_text

                self.current_text += line.replace('\n', '').encode('utf-8')

        # for EOF
        self.push()
        
        return self.messages

    def analyze(self):
        daily_result = []
        current_date = None
        current_messages = []

        for message in self.messages:
            date = message['date']
            if current_date and not current_date == date:
                daily_result.append([current_date, current_messages])
                current_messages = []

            current_date = date
            current_messages.append(message)

        row = ''
        for key in self.keys:
            row += ',%s_count,%s_size' % (key, key)
        print row

        for current_date, current_messages in daily_result:
            count = { key : 0 for key in self.keys }
            size = { key : 0 for key in self.keys }

            for message in current_messages:
                text = message['text']
                author = message['author']

                if (text.find('[スタンプ]') >= 0 or
                    text.find('[画像]') >= 0 or
                    text.find('不在着信') >= 0 or
                    text.find('通話に応答がありませんでした') >= 0 or
                    text.find('通話時間') >= 0):
                    continue

                count[author] += 1
                size[author] += len(text)

            row = current_date
            for key in self.keys:
                row += ',%d,%d' % (count[key], size[key])
            print row

def main():
    messages = Messages()

    with io.open('log.txt', encoding = 'utf-8') as f:
        messages.parse_lines(f)
        messages.analyze()

if __name__ == '__main__':
    main()
