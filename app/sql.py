#coding=utf-8
import sqlite3

class Intro(object):
    def __init__(self, id, name, intro, song):
        self.id = id
        self.name = name
        self.intro = intro
        self.song = song

    def insert(self):
        conn = sqlite3.connect("intro.db")
        conn.text_factory = str
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Birds_Intro
              (id INTEGER PRIMARY KEY,
               name char,
               intro text,
               song text)''')
        c.execute('''INSERT INTO Birds_Intro(name, intro, song) VALUES(?,?,?)''',(self.name, self.intro, self.song))
        conn.commit()
        conn.close()
        return 0

    @staticmethod
    def query(name):
        conn = sqlite3.connect("intro.db")
        conn.text_factory = str
        c = conn.cursor()
        c.execute('select name, intro from Birds_Intro where name=?', (name,))
        values = c.fetchone()
        conn.commit()
        conn.close()
        return values

if __name__ == '__main__':
    name, intro_text = Intro.query(u'麻雀')
    print name
    print intro_text