import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://review_user:review_pass@localhost:5433/document_review",
)