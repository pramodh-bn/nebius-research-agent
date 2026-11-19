import asyncio
import json
import pytest
from courtroom.api import (
    api_file_case,
    api_challenge,
    api_file_case_stream,
    api_challenge_stream,
    generate_case_stream,
    generate_challenge_stream,
    deserialize_case,
    health,
    FileCaseRequest,
    ChallengeRequest,
)
from courtroom.core import Courtroom
from test_core import FakeSearch, FakeReasoner
from test_reconsideration import Fetcher, NEW_PAGE


def get_mock_courtroom():
    return Courtroom(FakeSearch(), FakeReasoner(), fetcher=Fetcher(NEW_PAGE))


def test_health_endpoint():
    res = health()
    assert res["status"] == "ok"


def test_file_case_and_challenge_api(monkeypatch):
    from courtroom import api
    monkeypatch.setattr(api, "get_courtroom", get_mock_courtroom)

    # 1. File case
    data = api_file_case(FileCaseRequest(question="Does intermittent fasting work?"))
    assert data["mode"] == "live"
    assert len(data["prosecution"]) > 0
    assert len(data["defense"]) > 0
    assert len(data["evidence"]) > 0
    assert data["decision"] == "Inconclusive"
    assert "_raw" in data

    # 2. Challenge case using returned _raw
    ch_data = api_challenge(ChallengeRequest(
        case_raw=data["_raw"],
        challenge="What about trials longer than 12 months?",
        source_url="",
        target_claim="P1"
    ))
    assert len(ch_data["revisions"]) == 1
    rev = ch_data["revisions"][0]
    assert rev["challenge"] == "What about trials longer than 12 months?"
    assert rev["target"] == "P1"


def test_empty_question_rejected(monkeypatch):
    from fastapi import HTTPException
    from courtroom import api
    monkeypatch.setattr(api, "get_courtroom", get_mock_courtroom)

    with pytest.raises(HTTPException) as exc:
        api_file_case(FileCaseRequest(question="   "))
    assert exc.value.status_code == 400


def test_file_case_and_challenge_stream_api(monkeypatch):
    court = get_mock_courtroom()

    # 1. Test case stream generator directly
    events = []
    for chunk in generate_case_stream(court, "Does intermittent fasting work?"):
        text = chunk.strip()
        if text.startswith("data: "):
            events.append(json.loads(text[6:]))

    event_types = [e["type"] for e in events]
    assert "phase" in event_types
    assert "evidence" in event_types
    assert "prosecution" in event_types
    assert "defense" in event_types
    assert "cross_exam" in event_types
    assert "verdict" in event_types
    assert "complete" in event_types

    final_case = next(e["case"] for e in events if e["type"] == "complete")
    assert final_case["decision"] == "Inconclusive"
    assert "_raw" in final_case

    # 2. Test challenge stream generator directly
    case_obj = deserialize_case(final_case["_raw"])
    ch_events = []
    for chunk in generate_challenge_stream(
        court,
        case_obj,
        challenge="What about trials longer than 12 months?",
        source_url="",
        target_claim="P1"
    ):
        text = chunk.strip()
        if text.startswith("data: "):
            ch_events.append(json.loads(text[6:]))

    ch_types = [e["type"] for e in ch_events]
    assert "evidence" in ch_types
    assert "arguments_updated" in ch_types
    assert "verdict" in ch_types
    assert "complete" in ch_types

    # 3. Verify endpoint wrapper returns StreamingResponse
    from courtroom import api
    monkeypatch.setattr(api, "get_courtroom", get_mock_courtroom)
    res = api_file_case_stream(FileCaseRequest(question="Does intermittent fasting work?"))
    assert res.media_type == "text/event-stream"
