from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String, DateTime, create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import datetime

# -----------------------
# Database Setup
# -----------------------
DATABASE_URL = "sqlite:///email_logs.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # Updated for SQLAlchemy 2.0

# -----------------------
# Email Logs Table
# -----------------------
class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Create table if it doesn't exist
Base.metadata.create_all(bind=engine)

# -----------------------
# FastAPI Setup
# -----------------------
app = FastAPI(title="Email Logging API")

# -----------------------
# Routes
# -----------------------
@app.get("/emails")
def get_emails():
    try:
        with SessionLocal() as session:
            results = session.execute(
                select(EmailLog).order_by(EmailLog.timestamp.desc())
            )
            emails = [
                {
                    "id": email.id,
                    "sender": email.sender,
                    "recipient": email.recipient,
                    "subject": email.subject,
                    "body": email.body,
                    "timestamp": email.timestamp,
                }
                for email in results.scalars()
            ]
            return {"emails": emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/emails")
def create_email(sender: str, recipient: str, subject: str, body: str = None):
    try:
        with SessionLocal() as session:
            new_email = EmailLog(
                sender=sender,
                recipient=recipient,
                subject=subject,
                body=body
            )
            session.add(new_email)
            session.commit()
            session.refresh(new_email)

            return {
                "message": "Email logged successfully",
                "email": {
                    "id": new_email.id,
                    "sender": new_email.sender,
                    "recipient": new_email.recipient,
                    "subject": new_email.subject,
                    "body": new_email.body,
                    "timestamp": new_email.timestamp,
                },
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
