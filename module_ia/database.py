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

def    initDatabase():
    try:
        connection = sqlite3.connect('database_ia.db')
    except Error as e:
        print(e)

    if connection:
        query = connection.cursor()
        query.execute('''
            CREATE TABLE IF NOT EXISTS prompt(
                user_id CHAR(20) NOT NULL PRIMARY KEY,
                last_prompt text,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            )'''
        )
        return connection, query
    return None, None

def setPrompt( user_id, prompt ):
    connection, query = initDatabase()
    if connection:
        query.execute("REPLACE INTO prompt( user_id, last_prompt ) VALUES (?, ?);", (user_id, prompt))
        connection.commit()
        connection.close()

def    getPrompt( user_id ):
    connection, query = initDatabase()
    if connection:
        query.execute("SELECT last_prompt FROM prompt WHERE user_id = ?;", [user_id])
        myresult = query.fetchall()
        connection.close()
        if myresult and myresult[0] and myresult[0][0]:
            return myresult[0][0]
    return None

setPrompt("Troudball", "Ceci est le dernier prompte")
print(getPrompt("Troudball"))
