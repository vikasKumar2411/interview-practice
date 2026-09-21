from typing import Literal

from pydantic import EmailStr

from app.db import get_connection
from app.models import ReviewResponse


class DocRepository:
    def save(
        self,
        document_name: str,
        submitted_by: EmailStr,
        priority: Literal["normal", "high"],
        status: str,
    ) -> ReviewResponse:

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO reviews (
                        document_name,
                        submitted_by,
                        priority,
                        status
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        document_name,
                        str(submitted_by),
                        priority,
                        status,
                    ),
                )

                review_id = cur.fetchone()[0]

        return ReviewResponse(
            id=review_id,
            document_name=document_name,
            submitted_by=submitted_by,
            priority=priority,
            status=status,
        )

    def get(self, review_id: int) -> ReviewResponse | None:

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        document_name,
                        submitted_by,
                        priority,
                        status
                    FROM reviews
                    WHERE id = %s
                    """,
                    (review_id,),
                )

                row = cur.fetchone()

        if row is None:
            return None

        return ReviewResponse(
            id=row[0],
            document_name=row[1],
            submitted_by=row[2],
            priority=row[3],
            status=row[4],
        )