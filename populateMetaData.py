import re
import sqlite3

def findDate(fileName):
    date = 210905
    try:
        i = fileName.find('0')
        if i > 2 or i < 0:
            i = fileName.find('1')
        date = fileName[i:i+6]
        date = int(date[4:6] + date[0:4])
    except:
        date = 210905
    print(date, " (yymmdd) If this is the correct date, press enter.")
    userInput = input("Else, enter date (yymmdd): ")
    if userInput: # is not null
        return int(userInput)
    else:
        return date

def suggest(str, connection, **kwargs):
    cursor = connection.cursor()
    sortKey = kwargs.get("sortKey", None)
    if sortKey:
        cursor.execute(
            """SELECT DISTINCT
            {0}
            FROM audio
            WHERE {0} LIKE '{0}%'
            ORDER BY date DESC;""".format(str)
        )
        cursor2 = connection.cursor()
        cursor2.execute(
            """SELECT DISTINCT
            {0}
            FROM audio
            WHERE {0} NOT LIKE '{0}%'
            ORDER BY date DESC;""".format(str)
        )
        results = cursor.fetchall() + cursor2.fetchall()
    else:
        cursor.execute(
            """SELECT DISTINCT
            {}
            FROM audio
            ORDER BY date DESC;""".format(str)
        )
        results = cursor.fetchall()
    for i in range(0, len(results)):
        print(i + 1, ":", results[i][0])
    userInput = input("Enter a number (default '1') to select a " + str + " or enter a new one: ")
    try:
        selectedOption = int(userInput) - 1
        return results[selectedOption][0]
    except:
        if userInput: # is not null
            return userInput
        else: # return the first option
            return results[0][0]

def addDBEntry(fileName):
    metaDataDB = sqlite3.connect("./MetaData.db")
    title = input("Enter Title: ")
    book = suggest("book", metaDataDB)
    verse = input("Enter Verses: ")
    series = suggest("series", metaDataDB)
    speaker = suggest(
        "speaker",
        metaDataDB,
        sortKey=fileName[re.search(r'[a-zA-Z]', fileName).start()]
    )
    date = findDate(fileName)
    addingCursor = metaDataDB.cursor()
    addingCursor.execute("""
        INSERT INTO audio (
            file_name,
            title,
            book,
            verse,
            series,
            speaker,
            date
        ) VALUES(
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        );
        """, (fileName, title, book, verse, series, speaker, date)
    )
    metaDataDB.commit()
