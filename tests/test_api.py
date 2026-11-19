import pytest
from courtroom.api import api_file_case, api_challenge, health, FileCaseRequest, ChallengeRequest
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
