import sqlite3
import os
from collections import Counter

def loweredText(text):
    loweredText = ''.join(char for char in text if char.isalnum() or char.isspace())
    return loweredText.lower()

def createTable():
    conn = sqlite3.connect('.venv/texts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS texts
                 (id INTEGER PRIMARY KEY, text TEXT)''')
    conn.commit()
    conn.close()

def insertText(text):
    conn = sqlite3.connect('.venv/texts.db')
    c = conn.cursor()
    c.execute("INSERT INTO texts (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

def textInput():
    metin1 = input("Birinci metni girin: ")
    metin2 = input("İkinci metni girin: ")
    return metin1, metin2


def showItems():
    conn = sqlite3.connect('.venv/texts.db')
    c = conn.cursor()
    print("\nVeritabanındaki Metinler:")
    c.execute("SELECT * FROM texts")
    for row in c.fetchall():
        print(row)

def jaccardSimilarity(text1, text2):
    set1 = set(text1.split())
    set2 = set(text2.split())
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    similarity = intersection / union if union != 0 else 0
    return similarity

def cleanTable(tableName):
    conn = sqlite3.connect('.venv/texts.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {tableName}")
    conn.commit()
    print(f"{tableName} tablosunun içeriği temizlendi.")
    conn.close()

def letterFrequencySimilarity(text1, text2):

    freq1 = Counter(text1.lower())
    freq2 = Counter(text2.lower())

    total1 = sum(freq1.values())
    total2 = sum(freq2.values())

    similarity = sum(min(freq1[char], freq2[char]) for char in set(freq1) & set(freq2)) / max(total1, total2) if max(total1, total2) != 0 else 0

    return similarity

def writeFile(filename,text):
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode) as file:
        file.write(text + '\n')
    os.system(f"open {filename}")

createTable()
metin1, metin2 = textInput()
metin1 = loweredText(metin1)
metin2 = loweredText(metin2)
insertText(metin1)
insertText(metin2)

conn = sqlite3.connect('.venv/texts.db')
c = conn.cursor()
c.execute("SELECT * FROM texts")
rows = c.fetchall()
print(rows)
if len(rows) >= 2:
    metin1, metin2 = rows[-2][1], rows[-1][1]  # Son iki metni alma işlemi
    jaccardBenzerlik = jaccardSimilarity(metin1, metin2)
    frekansBenzerlik = letterFrequencySimilarity(metin1,metin2)
    print(f"Jaccard Benzerliği: {jaccardBenzerlik}")
    print(f"Frekans Benzerliği: {frekansBenzerlik}")
    writeFile(".venv/benzerlikSonuclari.txt", f"Jaccard Benzerliği: {jaccardBenzerlik}")
    writeFile(".venv/benzerlikSonuclari.txt", f"Frekans Benzerliği: {frekansBenzerlik}")


cleanTable("texts")
conn.close()
