import db


def generate_prompt(user_id, chat_id, cursor):
    db_messages = db.get_message(user_id, chat_id, cursor)

    chat = ""
    for i in range(int(len(db_messages) / 2)):
        chat += f"          User: {db_messages[2 * i][1]}\n"
        chat += f"          You: {db_messages[2 * i + 1][1]}\n"

    return f"""
        <s>[INST]
            You are an airline customer support bot. Your name is AIRBOT. I am the passenger.
            Answer questions only based on given context.
            If there is no information in context, just say that you are unable to answer.
        [/INST]</s>
        <chat_history>
{chat}
        </chat_history>
        
        [INST] {{input}}
            Context: {{context}}
            Answer:
        [/INST]
        """
