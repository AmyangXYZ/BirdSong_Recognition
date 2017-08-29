#coding=utf-8
import sqlite3

class Query(object):
    def __init__(self, id, name, sci_name, intro, song):
        self.id = id
        self.name = name.decode('utf-8')
        self.sci_name = sci_name.decode('utf-8')
        self.intro = intro.decode('utf-8')
        self.song = song

    def insert(self):
        conn = sqlite3.connect("intro.db")
        conn.text_factory = str
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Birds_Intro
              (id INTEGER PRIMARY KEY,
               name char,
               sci_name char,
               intro text,
               song text)''')
        c.execute('''INSERT INTO Birds_Intro(name, sci_name, intro, song) VALUES(?,?,?,?)''',(self.name, self.sci_name, self.intro, self.song))
        conn.commit()
        conn.close()
        return 0

    @staticmethod
    def query_all():
        conn = sqlite3.connect("/srv/flask/BirdSong_Recognition/app/intro.db")
        conn.text_factory = str
        c = conn.cursor()
        c.execute('select * from Birds_Intro')
        rows = c.fetchall()
        birds = []
        for r in rows:
            bird = Query(r[0], r[1], r[2], r[3], r[4])
            birds.append(bird)
        conn.commit()
        conn.close()
        return birds

    @staticmethod
    def query_bird_sciname(sci_name):
        conn = sqlite3.connect("/srv/flask/BirdSong_Recognition/app/intro.db")
        conn.text_factory = str
        c = conn.cursor()
        c.execute('select * from Birds_Intro where sci_name=?', (sci_name,))
        r = c.fetchone()
        bird = Query(r[0], r[1], r[2], r[3], r[4])
        conn.commit()
        conn.close()
        return bird

    @staticmethod
    def query_bird_name(name):
        conn = sqlite3.connect("/srv/flask/BirdSong_Recognition/app/intro.db")
        conn.text_factory = str
        c = conn.cursor()
        c.execute('select * from Birds_Intro where name=?', (name,))
        r = c.fetchone()
        bird = Query(r[0], r[1], r[2], r[3], r[4])
        conn.commit()
        conn.close()
        return bird

if __name__ == '__main__':
    name = u'麻雀'
    sci_name = ''
    intro = ''
    song = ''
    #Query(1, name, sci_name, intro, song).insert()
    birds = Query.query_all()
    for bird in birds:
        print bird.name