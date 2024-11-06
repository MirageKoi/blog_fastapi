import datetime as dt
from datetime import datetime, timedelta

import pytest

from src.posts.models import Comment


# Helper function to insert test comments into the database
def insert_test_comments(db_session, comments_data):
    for data in comments_data:
        comment = Comment(**data)
        db_session.add(comment)
    db_session.commit()


@pytest.mark.asyncio
async def test_comments_daily_breakdown(client, api_session):
    today = datetime.now()
    comments_data = [
        {
            "id": 1,
            "content": "Test",
            "post_id": 1,
            "user_id": 1,
            "created_at": today - timedelta(days=1),
            "is_blocked": False,
        },
        {
            "id": 2,
            "content": "Test",
            "post_id": 1,
            "user_id": 1,
            "created_at": today - timedelta(days=1),
            "is_blocked": True,
        },
        {
            "id": 3,
            "content": "Test",
            "post_id": 1,
            "user_id": 1,
            "created_at": today,
            "is_blocked": False,
        },
        {
            "id": 4,
            "content": "Test",
            "post_id": 1,
            "user_id": 1,
            "created_at": today,
            "is_blocked": True,
        },
        {
            "id": 5,
            "content": "Test",
            "post_id": 1,
            "user_id": 1,
            "created_at": today,
            "is_blocked": False,
        },
    ]

    # Insert test data into the database
    insert_test_comments(api_session, comments_data)

    date_from = dt.date.today() - dt.timedelta(days=10)
    date_to = date_from + dt.timedelta(days=20)

    response = client.get(
        "/analytics/api/comments-daily-breakdown",
        params={"date_from": date_from, "date_to": date_to},
    )

    # Validate the response
    assert response.status_code == 200
    json_response = response.json()

    # Ensure the correct breakdown for two days
    assert len(json_response) == 2  # One day before and the current day

    assert json_response[0]["total_comments"] == 2  # Two comments
    assert json_response[0]["blocked_comments"] == 1  # One blocked

    assert json_response[1]["total_comments"] == 3  # Three comments
    assert json_response[1]["blocked_comments"] == 1  # One blocked
