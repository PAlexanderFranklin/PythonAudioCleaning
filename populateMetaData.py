import sqlite3

def findDate(str):
    date = 210905
    try:
        i = str.find('0')
        if i > 2 or i < 0:
            i = str.find('1')
        date = str[i:i+6]
        date = int(date[4:6] + date[0:4])
    except:
        date = 210905
    print(date, " If this is the correct date, press enter.")
    userInput = input("Else, enter date (mmddyy): ")
    if userInput: # is not null
        return int(userInput[4:6] + userInput[0:4])
    else:
        return date

def suggest(str, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT " + str + " FROM audio ORDER BY date DESC;")
    results = cursor.fetchall()
    for i in range(0, len(results)):
        print(i, ":", results[i][0])
    userInput = input("Enter a number to select a " + str + " or enter a new one: ")
    try:
        selectedOption = int(userInput)
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
    speaker = suggest("speaker", metaDataDB)
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
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            {}
        );
        """.format(fileName, title, book, verse, series, speaker, date)
    )
    metaDataDB.commit()
