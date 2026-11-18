from courtroom.core import Courtroom, Case, validate_claims

class FakeSearch:
    def search(self, query):
        return [{'title': 'Example', 'url': 'https://example.org/study', 'content': 'The study reports mixed results.'}]

class FakeReasoner:
    def complete(self, system, user):
        if 'impartial judge' in user:
            return {'decision': 'Inconclusive', 'reasoning': 'Evidence is mixed.',
                    'claims': [{'text': 'Evidence is mixed', 'sources': ['E1'], 'status': 'contested'}],
                    'unresolved': ['Long term effects'], 'change_explanation': 'No change'}
        return {'summary': 'Mixed evidence', 'claims': [{'text': 'Mixed', 'sources': ['E1'], 'status': 'contested'}], 'limitations': []}

def test_case_and_challenge():
    c = Courtroom(FakeSearch(), FakeReasoner())
    case = c.file_case('Is this a good idea?')
    assert len(case.evidence) == 1
    assert case.verdict['decision'] == 'Inconclusive'
    c.challenge(case, 'What about long term effects?')
    assert len(case.revisions) == 1
    assert len(case.evidence) == 1

def test_fabricated_source_removed():
    result = validate_claims({'claims': [{'text': 'x', 'sources': ['FAKE'], 'status': 'supported'}]}, {'E1'})
    assert result['claims'][0]['sources'] == []
    assert result['claims'][0]['status'] == 'unsupported'

def test_empty_case():
    import pytest
    with pytest.raises(ValueError):
        Courtroom(FakeSearch(), FakeReasoner()).file_case('  ')
