import os
import mysql.connector
from dotenv import load_dotenv


def Connection():
    load_dotenv()
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )


def Disconnect(cursor, connection):
    cursor.close()
    connection.close()


def Cursor(connection):
    return connection.cursor()


# sender: (llm->false, user->true)
def send_message(message, user_id, chat_id, sender, cursor, connection):
    insert_query = """
    INSERT INTO messages (message, user_id, chat_id, date, sender)
    VALUES (%s, %s, %s, NOW(), %s)"""
    cursor.execute(insert_query, (message, user_id, chat_id, sender))
    connection.commit()


def get_message(user_id, chat_id, cursor):
    query = """
    SELECT * FROM messages
    WHERE user_id = %s AND chat_id = %s
    """

    cursor.execute(query, (user_id, chat_id))
    results = cursor.fetchall()

    return results


def delete_older_rows(user_id, chat_id, cursor, connection):
    delete_query = """
        DELETE FROM messages
        WHERE (user_id, chat_id, date) NOT IN (
        SELECT user_id, chat_id, date
        FROM (
            SELECT user_id, chat_id, date
            FROM messages
            WHERE user_id = %s AND chat_id = %s
            ORDER BY date DESC
            LIMIT 6
        ) AS subquery
        )
        AND user_id = %s
        AND chat_id = %s;
        """

    cursor.execute(delete_query, (user_id, chat_id, user_id, chat_id))
    connection.commit()
