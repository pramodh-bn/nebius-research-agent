import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))
import streamlit as st
from dotenv import load_dotenv
from courtroom.core import Courtroom, TavilySearch, NebiusReasoner

load_dotenv()
st.set_page_config(page_title='Research Courtroom', page_icon='⚖️', layout='wide')
st.title('⚖️ Research Courtroom')
st.caption('Two sides argue. Evidence decides. You can challenge the verdict.')

@st.cache_resource
def get_courtroom():
    nebius = os.getenv('NEBIUS_API_KEY')
    tavily = os.getenv('TAVILY_API_KEY')
    if not nebius or not tavily:
        return None
    return Courtroom(TavilySearch(tavily), NebiusReasoner(
        nebius, os.getenv('NEBIUS_MODEL', 'meta-llama/Llama-3.3-70B-Instruct'),
        os.getenv('NEBIUS_BASE_URL', 'https://api.studio.nebius.com/v1')))

def show_claim(claim):
    v = claim.get('verification', {})
    badge = 'VERIFIED' if claim.get('verified') else 'NOT VERIFIED'
    st.markdown(f"**{claim.get('status','unresolved').upper()}** — {claim.get('text','')}")
    st.caption(f"{badge} · assessment: {v.get('status','n/a')} (LLM verifier opinion, not proof) — {v.get('explanation','')}")
    links = [f'[{i}]({ledger[i].url})' for i in claim.get('sources', []) if i in ledger]
    st.caption('Sources: ' + (', '.join(links) or 'none'))
    if claim.get('rejected_sources'):
        st.caption('Rejected unknown citations: ' + ', '.join(claim['rejected_sources']))

court = get_courtroom()
if not court:
    st.error('Set NEBIUS_API_KEY and TAVILY_API_KEY in .env, then restart Streamlit.')
    st.stop()

with st.form('file'):
    question = st.text_input('File a case', placeholder='Should companies replace junior developers with AI agents?')
    filed = st.form_submit_button('Open trial', type='primary')
if filed:
    try:
        with st.spinner('Researching both sides and deliberating...'):
            st.session_state.case = court.file_case(question)
    except Exception as exc:
        st.error(f'Trial could not start: {exc}')

case = st.session_state.get('case')
ledger = {}
if case:
    ledger = {e.id: e for e in case.evidence}
    for w in case.warnings:
        st.warning(w)
    st.subheader('Opening arguments')
    left, right = st.columns(2)
    for column, label, argument in [(left, 'Prosecution', case.prosecution), (right, 'Defense', case.defense)]:
        with column:
            st.markdown(f'### {label}')
            st.write(argument.get('summary', ''))
            for claim in argument.get('claims', []):
                show_claim(claim)
            for limit in argument.get('limitations', []):
                st.caption(f'Limitation: {limit}')

    if case.cross_exam.get('exchanges'):
        st.subheader('Cross-examination')
        for x in case.cross_exam['exchanges']:
            st.markdown(f"**{x['asker'].title()} asks:** {x['question']}")
            show_claim({'text': x['answer'], 'status': 'answer', 'sources': x['sources'],
                        'verification': x['verification'], 'verified': x['verified']})

    st.subheader('⚖️ Judicial verdict')
    st.markdown(f"**{case.verdict.get('decision', 'Inconclusive')}**")
    st.write(case.verdict.get('reasoning', ''))
    for claim in case.verdict.get('claims', []):
        show_claim(claim)
    if case.verdict.get('evidence_warning'):
        st.warning(case.verdict['evidence_warning'])
    for item in case.verdict.get('unresolved', []):
        st.info(f'Unresolved: {item}')
    if case.revisions:
        last = case.revisions[-1]
        (st.success if last['decision_changed'] else st.info)(
            ('Verdict changed: ' if last['decision_changed'] else 'Verdict unchanged: ') + last['reason'])

    st.subheader('Cross-examine the court')
    with st.form('challenge'):
        claims = [c.get('text', '') for c in case.verdict.get('claims', [])]
        target = st.selectbox('Claim to challenge (optional)', [''] + claims, format_func=lambda t: t or '— whole verdict —')
        challenge = st.text_area('Challenge an argument or ask a follow-up')
        source = st.text_input('Optional source URL (fetched with safety limits; any page is still verified, never auto-trusted)')
        submitted = st.form_submit_button('Challenge verdict')
    if submitted:
        try:
            with st.spinner('Reviewing new evidence and reconsidering the verdict...'):
                court.challenge(case, challenge, source, target)
            st.rerun()
        except Exception as exc:
            st.error(f'Challenge failed: {exc}')

    with st.expander(f'Evidence ledger ({len(case.evidence)} sources)', expanded=True):
        for e in case.evidence:
            st.markdown(f'**{e.id}: [{e.title}]({e.url})**  `{e.metadata.get("origin", "search")}`')
            if e.suspicious:
                st.warning('Excerpt resembles a prompt-injection attempt; treated as data only.')
            st.caption(f'Retrieved {e.retrieved_at} via query: {e.query}')
            st.caption(e.excerpt)
    if case.revisions:
        with st.expander('Verdict revision history'):
            for i, revision in enumerate(case.revisions, 1):
                st.markdown(f"**Revision {i}** — {revision['challenge']}")
                if revision.get('target_claim'):
                    st.caption(f"Challenged claim: {revision['target_claim']}")
                if revision.get('source_url'):
                    labels = {'fetched': 'fetched and added to ledger', 'fetched_duplicate': 'fetched; already in ledger',
                              'search_hint': 'could not be fetched; related results are UNVERIFIED search hints',
                              'blocked': 'blocked by safety checks; not fetched'}
                    st.caption(f"Submitted URL {revision['source_url']}: {labels.get(revision['url_status'], revision['url_status'])}")
                st.write('Before:', revision['before_decision'], '→ After:', revision['after_decision'],
                         '(changed)' if revision['decision_changed'] else '(unchanged)')
                st.write(f"Verified claims: {revision['verified_claims_before']} → {revision['verified_claims_after']}")
                st.write('Reason:', revision['reason'])
                if revision['evidence_added']:
                    st.write('New evidence:')
                    for ev in revision['evidence_added']:
                        st.markdown(f"- {ev['id']} [{ev['title']}]({ev['url']}) — {ev['origin']}")
                else:
                    st.write('New evidence: none')
