from datetime import datetime

from own_chat.db import db


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    llm_model_id = db.Column(db.Integer, db.ForeignKey("llm_model.id"), nullable=False)
    title = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("chats", lazy=True))
    llm_model = db.relationship("LLMModel", backref=db.backref("chats", lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "llm_model_id": self.llm_model_id,
            "title": self.title,
            "created_at": self.created_at,
        }


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    chat = db.relationship(
        "Chat", backref=db.backref("messages", lazy=True, order_by="Message.timestamp")
    )

    def serialize(self):
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "sender": self.sender,
            "content": self.content,
            "timestamp": self.timestamp,
        }
