"""Opt-in live smoke tests. Run: set RUN_LIVE=1 with NEBIUS_API_KEY and TAVILY_API_KEY, then `python -m pytest -q tests/test_live.py`."""
import os
import pytest
from dotenv import load_dotenv

load_dotenv()
live = pytest.mark.skipif(not (os.getenv('RUN_LIVE') and os.getenv('NEBIUS_API_KEY') and os.getenv('TAVILY_API_KEY')),
                          reason='live tests are opt-in: set RUN_LIVE=1 and both API keys')


@live
def test_live_end_to_end_case():
    from courtroom.core import Courtroom, TavilySearch, NebiusReasoner
    court = Courtroom(TavilySearch(os.environ['TAVILY_API_KEY']), NebiusReasoner(
        os.environ['NEBIUS_API_KEY'], os.getenv('NEBIUS_MODEL', 'meta-llama/Llama-3.3-70B-Instruct'),
        os.getenv('NEBIUS_BASE_URL', 'https://api.studio.nebius.com/v1')))
    case = court.file_case('Does intermittent fasting improve long-term weight loss compared with calorie restriction?')
    ids = {e.id for e in case.evidence}
    assert case.evidence and case.verdict.get('decision')
    for part in (case.prosecution, case.defense, case.verdict):
        for claim in part['claims']:
            assert set(claim['sources']) <= ids and 'verification' in claim
    assert case.calls_used <= 16
