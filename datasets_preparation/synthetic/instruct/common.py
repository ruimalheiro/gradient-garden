def row(user_content, assistant_content):
    return {
        'messages': [
            {'role': 'user', 'content': user_content.strip()},
            {'role': 'assistant', 'content': assistant_content.strip()}
        ]
    }
