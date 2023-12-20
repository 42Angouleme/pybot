# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alclauze <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/08/16 16:20:16 by alclauze          #+#    #+#              #
#    Updated: 2023/08/17 14:53:59 by alclauze         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sqlite3

def initDatabase():
    try:
        connection = sqlite3.connect('database_ia.db')
    except Error as e:
        print(e)

    if connection:
        query = connection.cursor()
        query.execute('''
            CREATE TABLE IF NOT EXISTS data_resume(
                user_id CHAR(20) NOT NULL PRIMARY KEY,
                resume text,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            )'''
        )

        query.execute('''
            CREATE TABLE IF NOT EXISTS data_history(
                user_id CHAR(20) NOT NULL PRIMARY KEY,
                history text
            )'''
        )
        return connection, query
    return None, None

def setPrompt( user_id, prompt ):
    connection, query = initDatabase()
    if connection:
        query.execute("REPLACE INTO data_resume( user_id, resume ) VALUES (?, ?);", (user_id, prompt))
        connection.commit()
        connection.close()

def getPrompt( user_id ):
    connection, query = initDatabase()
    if connection:
        query.execute("SELECT resume FROM data_resume WHERE user_id = ?;", [user_id])
        myresult = query.fetchall()
        connection.close()
        if myresult and myresult[0] and myresult[0][0]:
            return myresult[0][0]
    return None

def newHistory( user_id, history ):
    connection, query = initDatabase()
    if connection:
        query.execute("REPLACE INTO data_history( user_id, history ) VALUES (?, ?);", (user_id, history))
        connection.commit()
        connection.close()

def addHistory( user_id, history ):
    strHistory = ""
    connection, query = initDatabase()
    if connection:
        query.execute("SELECT history FROM data_history WHERE user_id = ?;", [user_id])
        myresult = query.fetchall()
        if myresult and myresult[0] and myresult[0][0]:
            strHistory = myresult[0][0]
        strHistory += history
        query.execute("REPLACE INTO data_history( user_id, history ) VALUES (?, ?);", (user_id, strHistory))
        connection.commit()
        connection.close()

def clearHistory( user_id ):
    connection, query = initDatabase()
    if connection:
        query.execute("DELETE FROM data_history WHERE user_id = ?;", [user_id])
        connection.commit()
        connection.close()

def getHistory( user_id ):
    connection, query = initDatabase()
    if connection:
        query.execute("SELECT history FROM data_history WHERE user_id = ?;", [user_id])
        myresult = query.fetchall()
        connection.close()
        if myresult and myresult[0] and myresult[0][0]:
            return myresult[0][0]
    return None