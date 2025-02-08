# LLM APP

Description: 
 - Create a Flask App that will allow users to chat with a Language Model.
 - User Login (Admin will register the user)
 - LLM Model
 - Chat should be persistent
Models
------

1. User
2. Chats
3. LLM Model
4. Message


GET /chat

POST /chat 
{
    "model": "id",
}

GET /chat/id

POST /chat/id
{
    "message": "Hello"
}