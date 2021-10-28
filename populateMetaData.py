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

def suggest(indexTable, mainIndex, connection, **kwargs):
    cursor = connection.cursor()
    sortKey = kwargs.get("sortKey", None)
    if sortKey:
        cursor.execute(
            """
            SELECT
            name
            FROM {0}
            WHERE name LIKE '{1}%';
            """.format(indexTable, sortKey)
        )
        cursor2 = connection.cursor()
        cursor2.execute(
            """
            SELECT
            name
            FROM {0}
            WHERE name NOT LIKE '{1}%';
            """.format(indexTable, sortKey)
        )
        results = cursor.fetchall() + cursor2.fetchall()
    else:
        cursor.execute(
            """
            SELECT
            name
            FROM {};
            """.format(indexTable)
        )
        results = cursor.fetchall()
    for i in range(0, len(results)):
        print(i + 1, ":", results[i][0])
    userInput = input("Enter a number (default '1') to select a "
    + mainIndex[:-3]
    + " or enter a new one: ")
    try:
        selectedOptionIndex = int(userInput) - 1
        selectedOption = results[selectedOptionIndex][0]
    except:
        if userInput: # is not null
            selectedOption = userInput
        else: # return the first option
            selectedOption = results[0][0]
    for i in range(0, 2):
        print("starting loop")
        cursor.execute(
            """
            SELECT
            id
            FROM {0}
            WHERE name = ?;
            """.format(indexTable), (selectedOption,)
        )
        results = cursor.fetchall()
        print(results)
        try:
            optionId = results[0][0]
            return optionId
        except:
            print("excepted")
            cursor.execute(
                """
                INSERT INTO {0} (
                    name
                ) VALUES(
                    ?
                );
                """.format(indexTable), (selectedOption,)
            )
            print("committing")
            connection.commit()
            print("committed")

def addDBEntry(fileName):
    metaDataDB = sqlite3.connect("./MetaData.db")
    title = input("Enter Title: ")
    book_id = suggest("books", "book_id", metaDataDB)
    verse = input("Enter Verses: ")
    series_id = suggest("series", "series_id", metaDataDB)
    speaker_id = suggest(
        "speakers", "speaker_id", metaDataDB,
        sortKey=fileName[re.search(r'[a-zA-Z]', fileName).start()]
    )
    date = findDate(fileName)
    addingCursor = metaDataDB.cursor()
    addingCursor.execute(
        """
        INSERT INTO audio (
            file_name,
            title,
            book_id,
            verse,
            series_id,
            speaker_id,
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
        """, (fileName, title, book_id, verse, series_id, speaker_id, date)
    )
    metaDataDB.commit()