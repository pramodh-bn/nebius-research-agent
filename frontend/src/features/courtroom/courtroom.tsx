import { useState, type FormEvent } from 'react';
import {
  ArrowDownToLine,
  ArrowRight,
  BookOpen,
  Check,
  CheckCheck,
  ChevronDown,
  ChevronRight,
  CircleCheck,
  Clock3,
  FileJson,
  FileText,
  Gavel,
  History,
  Info,
  Link2,
  LoaderCircle,
  MessageSquare,
  Scale,
  Search,
  Shield,
  ShieldCheck,
  TriangleAlert,
  Sparkles,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetDescription, SheetTitle } from '@/components/ui/sheet';
import { Dialog, DialogContent, DialogDescription, DialogTitle } from '@/components/ui/dialog';
import scales from '@/assets/courtroom-scales.png.asset.json';
import { sampleCase, sampleQuestion } from './sample-case';
import { screenSourceUrl } from './safety';
import { fileCaseStreamApi, challengeCaseStreamApi, type StreamEvent } from './api-client';
import type { Claim, Evidence, Revision, Case, Exchange } from './types';

const stages = ['Evidence search', 'Prosecution', 'Defense', 'Cross-examination', 'Verification', 'Judicial verdict'];

const presets: [string, string][] = [
  ['Intermittent fasting', sampleQuestion],
  ['Remote work productivity', 'Does remote work improve productivity compared with working in an office?'],
  ['AI vs. junior developers', 'Can AI coding assistants replace junior software developers?'],
];

const defaultExchanges: Exchange[] = [
  { side: 'Prosecution', question: 'Do equivalent average outcomes rule out an advantage for specific fasting protocols?', answer: 'No. The 4:3 trial suggests a modest advantage with comprehensive behavioral support. That does not establish superiority across all fasting regimens.', ids: ['E9', 'E10'] },
  { side: 'Defense', question: 'Can short-term pooled improvements establish a long-term weight-loss advantage?', answer: 'Not alone. The time-restricted eating meta-analysis supports a small pooled benefit, but durations and protocols vary. Longer controlled trials deserve greater weight.', ids: ['E5', 'E3'] },
  { side: 'Prosecution', question: 'Does the 12-month trial prove that fasting and calorie restriction are equivalent?', answer: 'A non-significant difference is not proof of equivalence. It means this trial did not demonstrate superiority; its confidence interval still allows uncertainty.', ids: ['E3'] },
  { side: 'Defense', question: 'Is the Harvard commentary independent confirmation of the 4:3 trial?', answer: 'No. It describes the same underlying trial. The ledger contains two sources, but the court counts one independent study for that finding.', ids: ['E9', 'E10'] },
];

function Status({ claim }: { claim: Claim }) {
  return (
    <span className={`status ${claim.status}`}>
      {claim.status === 'supported' ? <Check size={9} /> : <TriangleAlert size={9} />}
      {claim.status.toUpperCase()}
    </span>
  );
}

function VerificationPill({ claim, isLive }: { claim: Claim; isLive: boolean }) {
  return (
    <span className="verification" title={claim.verification?.note || 'Assessed against evidence ledger'}>
      <ShieldCheck size={10} />
      {claim.verification?.verified ? 'VERIFIED' : 'NOT VERIFIED'} · {claim.verification?.assessment || claim.status} · {isLive ? 'Nebius LLM verifier' : 'sample'}
    </span>
  );
}

function Citations({ ids, onSelect }: { ids: string[]; onSelect: (id: string) => void }) {
  return (
    <span className="citations">
      {ids.map(id => (
        <Button
          key={id}
          variant="ghost"
          className="citation"
          aria-label={`View evidence ${id}`}
          onClick={() => onSelect(id)}
        >
          {id}
        </Button>
      ))}
    </span>
  );
}

function Argument({
  side,
  claims,
  summary,
  limitations,
  isLive,
  isLoading,
  onSelect,
}: {
  side: 'prosecution' | 'defense';
  claims: Claim[];
  summary?: string;
  limitations?: string[];
  isLive: boolean;
  isLoading?: boolean;
  onSelect: (id: string) => void;
}) {
  const isPro = side === 'prosecution';
  const defaultSummary = isPro
    ? 'Intermittent fasting may offer meaningful benefits beyond conventional calorie restriction, particularly with specific protocols and structured support.'
    : 'The strongest long-term evidence suggests that total energy intake—not the timing of meals—is the primary driver of sustained weight loss.';
  const defaultLimits = isPro
    ? 'Protocol heterogeneity; limited evidence beyond 12 months. Adherence benefits are not universal.'
    : 'Average outcomes can obscure individual responses. Newer 4:3 evidence shows a protocol-specific benefit.';

  const isDrafting = isLoading && claims.length === 0;

  const displaySummary = summary && summary.trim().length > 0
    ? summary
    : (isDrafting
        ? (isPro ? 'Reviewing admitted evidence and formulating affirmative claims...' : 'Evaluating evidence boundaries and formulating counterarguments...')
        : (isLive
            ? (isPro ? 'Affirmative position grounded in retrieved ledger evidence.' : 'Counterarguments and critical boundaries grounded in retrieved ledger evidence.')
            : defaultSummary));

  const displayLimits = limitations && limitations.length > 0
    ? limitations.join(' · ')
    : (isDrafting
        ? 'Awaiting argument completion'
        : (isLive ? 'Heterogeneity across studies; sample sizes; potential confounding factors.' : defaultLimits));

  return (
    <article className={`argument ${side}`}>
      <div className="argument-head">
        <span className="role-icon">{isPro ? <Gavel size={19} /> : <Shield size={19} />}</span>
        <div>
          <h3>{isPro ? 'Prosecution' : 'Defense'}</h3>
          <p>{isPro ? 'The affirmative case' : 'Counterarguments & limitations'}</p>
        </div>
        <span className="role-label">
          {isDrafting ? 'DRAFTING CLAIMS' : (isPro ? 'ARGUING FOR' : 'ARGUING AGAINST')}
        </span>
      </div>
      <p className="argument-summary">{displaySummary}</p>
      <div className="claim-list">
        {isDrafting ? (
          <div className="p-5 border border-dashed border-border/80 rounded-md bg-secondary/30 text-center my-3">
            <LoaderCircle className="animate-spin mx-auto mb-2 text-gold" size={18} />
            <p className="text-xs text-muted-foreground font-mono">
              {isPro
                ? 'Prosecution reviewing evidence ledger and drafting claims...'
                : 'Defense awaiting evidence analysis to formulate counterarguments...'}
            </p>
          </div>
        ) : claims.length === 0 ? (
          <div className="p-4 border border-dashed border-border/50 rounded-md bg-secondary/10 text-center my-2 text-xs text-muted-foreground font-mono">
            No claims filed yet.
          </div>
        ) : (
          claims.map((claim, index) => (
            <div className="claim-item" key={claim.id || index}>
              <div className="claim-top">
                <span className="claim-number">CLAIM 0{index + 1}</span>
                <Status claim={claim} />
              </div>
              <p>{claim.text}</p>
              <div className="claim-bottom">
                <VerificationPill claim={claim} isLive={isLive} />
                <Citations ids={claim.evidenceIds} onSelect={onSelect} />
              </div>
            </div>
          ))
        )}
      </div>
      <div className="limitations">
        <strong><Info size={11} /> Limitations</strong>
        {displayLimits}
      </div>
    </article>
  );
}

function EvidenceItem({ item }: { item: Evidence }) {
  const formattedDate = item.retrievedAt
    ? new Date(item.retrievedAt).toLocaleString('en-US', { timeZone: 'UTC' }) + ' UTC'
    : 'Live retrieval';

  return (
    <article className="evidence-item" id={`source-${item.id}`}>
      <div className="flex items-center justify-between gap-3">
        <span className="count text-prosecution">{item.id}</span>
        <span className="status supported">
          {item.kind || (item.origin === 'user_url_fetch' ? 'User source' : 'Live search')}
        </span>
      </div>
      <h3>{item.title}</h3>
      <a href={item.url} target="_blank" rel="noopener noreferrer">
        {item.domain || item.url}
        <ArrowRight size={11} />
      </a>
      <div className="evidence-meta">
        <div>Origin: {item.origin} · {item.admitted ? 'Admitted in ledger' : 'Not admitted'}</div>
        <div>Query: {item.query}</div>
        <div>Retrieved: {formattedDate}</div>
      </div>
      {item.untrusted && (
        <div className="notice">
          <ShieldCheck size={12} />Treated as untrusted data · potential prompt injection
        </div>
      )}
      <details>
        <summary>Read exact excerpt</summary>
        <blockquote>{item.excerpt}</blockquote>
      </details>
    </article>
  );
}

interface LiveFeedEvent {
  id: string;
  timestamp: string;
  stage: string;
  message: string;
  type: string;
}

export function Courtroom() {
  const [currentCase, setCurrentCase] = useState<Case>(sampleCase);
  const [question, setQuestion] = useState(sampleQuestion);
  const [ledgerOpen, setLedgerOpen] = useState(false);
  const [selectedSource, setSelectedSource] = useState<Evidence>();
  const [filter, setFilter] = useState('All');
  const [exportOpen, setExportOpen] = useState(false);
  const [crossOpen, setCrossOpen] = useState(true);
  const [historyOpen, setHistoryOpen] = useState(false);
  const [challenge, setChallenge] = useState('');
  const [sourceUrl, setSourceUrl] = useState('');
  const [target, setTarget] = useState('Whole verdict');
  const [notice, setNotice] = useState('');
  const [error, setError] = useState('');
  const [stage, setStage] = useState<number | null>(null);
  const [revisions, setRevisions] = useState<Revision[]>(sampleCase.revisions);
  const [blockedSources, setBlockedSources] = useState<Evidence[]>([]);
  const [filingNotice, setFilingNotice] = useState('');
  const [showRevisionDiff, setShowRevisionDiff] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [liveEvents, setLiveEvents] = useState<LiveFeedEvent[]>([]);
  const [currentStageName, setCurrentStageName] = useState<string>('');

  const isLive = currentCase.mode === 'live';
  const allClaims = [...currentCase.prosecution, ...currentCase.defense];
  const allEvidence = [...currentCase.evidence, ...blockedSources];
  const exchanges: Exchange[] =
    currentCase.exchanges && currentCase.exchanges.length > 0
      ? currentCase.exchanges
      : (isLive ? [] : defaultExchanges);

  const selectSource = (id: string) => setSelectedSource(allEvidence.find(e => e.id === id));

  const openTrial = async (event: FormEvent) => {
    event.preventDefault();
    if (!question.trim()) return;
    setError('');
    setNotice('');
    setFilingNotice('Court is now in session. Deliberation stream initiated...');
    setIsLoading(true);
    setLiveEvents([]);
    setCurrentStageName('Initiating Trial');
    setStage(0);

    const logEvent = (stageKey: string, message: string, type: string) => {
      const timeStr = new Date().toTimeString().split(' ')[0];
      setLiveEvents(prev => [
        ...prev,
        { id: `${Date.now()}-${Math.random()}`, timestamp: timeStr, stage: stageKey, message, type }
      ]);
    };

    // Blank dynamic case draft for live document drafting
    const liveCaseDraft: Case = {
      id: 'RC-' + String(Math.floor(1000 + Math.random() * 9000)),
      question: question.trim(),
      mode: 'live',
      decision: 'Deliberating...',
      verdict: '',
      prosecution: [],
      defense: [],
      verdictClaims: [],
      prosecutionSummary: '',
      defenseSummary: '',
      prosecutionLimitations: [],
      defenseLimitations: [],
      unresolved: [],
      exchanges: [],
      evidence: [],
      revisions: [],
      warnings: [],
      evidenceWarning: '',
      callsUsed: 0,
    };
    setCurrentCase(liveCaseDraft);
    logEvent('search', `Filing research case: "${question.trim()}"`, 'phase');

    try {
      const finalCase = await fileCaseStreamApi(question.trim(), (ev: StreamEvent) => {
        if (ev.type === 'phase') {
          setCurrentStageName(ev.message || ev.stage || '');
          logEvent(ev.stage || 'phase', ev.message || 'Processing...', 'phase');
          if (ev.stage === 'search') setStage(0);
          else if (ev.stage === 'prosecution') setStage(1);
          else if (ev.stage === 'defense') setStage(2);
          else if (ev.stage === 'cross_exam') setStage(3);
          else if (ev.stage === 'verdict') setStage(4);
        } else if (ev.type === 'evidence') {
          if (ev.evidence) {
            setCurrentCase(prev => ({
              ...prev,
              evidence: ev.evidence || [],
            }));
          }
          logEvent('evidence', ev.message || `Admitted ${ev.count} sources into evidence ledger.`, 'evidence');
        } else if (ev.type === 'prosecution') {
          setStage(1);
          setCurrentCase(prev => ({
            ...prev,
            prosecution: ev.claims || [],
            prosecutionSummary: ev.summary || '',
            prosecutionLimitations: ev.limitations || [],
          }));
          logEvent('prosecution', ev.message || 'Prosecution opening arguments submitted.', 'prosecution');
        } else if (ev.type === 'defense') {
          setStage(2);
          setCurrentCase(prev => ({
            ...prev,
            defense: ev.claims || [],
            defenseSummary: ev.summary || '',
            defenseLimitations: ev.limitations || [],
          }));
          logEvent('defense', ev.message || 'Defense opening arguments submitted.', 'defense');
        } else if (ev.type === 'cross_exam') {
          setStage(3);
          setCurrentCase(prev => ({
            ...prev,
            exchanges: ev.exchanges || [],
          }));
          logEvent('cross_exam', ev.message || 'Cross-examination completed.', 'cross_exam');
        } else if (ev.type === 'verdict') {
          setStage(5);
          setCurrentCase(prev => ({
            ...prev,
            decision: ev.decision || 'Inconclusive',
            verdict: ev.reasoning || '',
            verdictClaims: ev.verdictClaims || [],
            unresolved: ev.unresolved || [],
          }));
          logEvent('verdict', ev.message || `Judicial verdict rendered: ${ev.decision}`, 'verdict');
        } else if (ev.type === 'complete' && ev.case) {
          setCurrentCase(ev.case);
          setRevisions(ev.case.revisions || []);
          logEvent('complete', ev.message || 'Trial concluded. Case ledger sealed.', 'complete');
        }
      });

      setStage(null);
      setIsLoading(false);
      setCurrentStageName('Trial Concluded');
      setFilingNotice(`Trial concluded · ${finalCase.evidence.length} sources retrieved, claims verified by Nebius.`);
    } catch (err: any) {
      setStage(null);
      setIsLoading(false);
      setError(`Live deliberation stream failed (${err.message}). Loaded sample case.`);
      setCurrentCase(sampleCase);
      setRevisions(sampleCase.revisions);
    }
  };

  const submitChallenge = async (event: FormEvent) => {
    event.preventDefault();
    setError('');
    setNotice('');

    const result = screenSourceUrl(sourceUrl);
    if (result === 'blocked') {
      setError('Submitted URL was blocked by SSRF safety checks and was not fetched.');
      const id = `B${blockedSources.length + 1}`;
      setBlockedSources(prev => [
        ...prev,
        {
          id,
          title: 'Blocked source submission',
          url: sourceUrl,
          domain: new URL(sourceUrl).hostname,
          excerpt: 'No content retrieved. Preliminary URL safety screening rejected this address.',
          query: challenge,
          retrievedAt: new Date().toISOString(),
          origin: 'blocked',
          kind: 'Security block',
          untrusted: true,
          admitted: false,
        },
      ]);
      return;
    }
    if (result === 'invalid') {
      setError('Enter a valid source URL beginning with https://.');
      return;
    }
    if (!challenge.trim() && !sourceUrl.trim()) {
      setError('Add an argument or follow-up question before submitting.');
      return;
    }

    setIsLoading(true);
    setCurrentStageName('Reviewing Challenge');
    setNotice('Reviewing challenge, re-examining arguments with new evidence...');

    const logEvent = (stageKey: string, message: string, type: string) => {
      const timeStr = new Date().toTimeString().split(' ')[0];
      setLiveEvents(prev => [
        ...prev,
        { id: `${Date.now()}-${Math.random()}`, timestamp: timeStr, stage: stageKey, message, type }
      ]);
    };

    try {
      if (currentCase._raw) {
        logEvent('challenge', `Challenge filed: "${challenge || sourceUrl}" targeting ${target}`, 'phase');
        const updated = await challengeCaseStreamApi(
          currentCase._raw,
          challenge.trim(),
          sourceUrl.trim(),
          target === 'Whole verdict' ? '' : target,
          (ev: StreamEvent) => {
            if (ev.type === 'phase') {
              setCurrentStageName(ev.message || ev.stage || '');
              logEvent(ev.stage || 'phase', ev.message || 'Processing...', 'phase');
            } else if (ev.type === 'url_admitted') {
              logEvent('url_check', ev.message || `URL admission: ${ev.url_status}`, 'evidence');
            } else if (ev.type === 'evidence') {
              if (ev.evidence) {
                setCurrentCase(prev => ({
                  ...prev,
                  evidence: ev.evidence || [],
                }));
              }
              logEvent('evidence', ev.message || `${ev.count} sources in ledger.`, 'evidence');
            } else if (ev.type === 'arguments_updated') {
              setCurrentCase(prev => ({
                ...prev,
                prosecution: ev.prosecutionClaims || prev.prosecution,
                defense: ev.defenseClaims || prev.defense,
                prosecutionSummary: ev.prosecutionSummary || prev.prosecutionSummary,
                defenseSummary: ev.defenseSummary || prev.defenseSummary,
              }));
              logEvent('re_argue', ev.message || 'Opening arguments re-evaluated with new evidence.', 'arguments');
            } else if (ev.type === 'verdict') {
              setCurrentCase(prev => ({
                ...prev,
                decision: ev.decision || prev.decision,
                verdict: ev.reasoning || prev.verdict,
                verdictClaims: ev.verdictClaims || prev.verdictClaims,
                unresolved: ev.unresolved || prev.unresolved,
              }));
              if (ev.revisions) {
                setRevisions(ev.revisions);
              }
              logEvent('verdict', ev.message || `Judicial verdict review complete: ${ev.decision}`, 'verdict');
            } else if (ev.type === 'complete' && ev.case) {
              setCurrentCase(ev.case);
              setRevisions(ev.case.revisions || []);
              logEvent('complete', ev.message || 'Reconsideration concluded.', 'complete');
            }
          }
        );
        setIsLoading(false);
        setCurrentStageName('Review Concluded');
        setCurrentCase(updated);
        setRevisions(updated.revisions || []);
        setHistoryOpen(true);
        setShowRevisionDiff(true);
        const lastRev = updated.revisions?.[updated.revisions.length - 1];
        setNotice(lastRev?.explanation || 'Verdict and arguments reconsidered with new evidence.');
        setChallenge('');
        setSourceUrl('');
      } else {
        // Fallback sample mode simulation
        setIsLoading(false);
        const count = allClaims.filter(c => c.verification?.verified).length;
        const revision: Revision = {
          id: revisions.length + 1,
          timestamp: new Date().toISOString(),
          challenge: challenge.trim(),
          target,
          beforeDecision: currentCase.decision,
          afterDecision: currentCase.decision,
          beforeVerified: count,
          afterVerified: count,
          evidenceAdded: [],
          explanation: `Challenge recorded for ${target.toLowerCase()}. A connected research service is required to evaluate new evidence; the sample verdict is unchanged.`,
          status: 'pending',
        };
        setRevisions(prev => [...prev, revision]);
        setHistoryOpen(true);
        setShowRevisionDiff(true);
        setNotice('Challenge recorded · verdict unchanged.');
        setChallenge('');
        setSourceUrl('');
      }
    } catch (err: any) {
      setIsLoading(false);
      setError(`Challenge failed: ${err.message}`);
    }
  };

  const download = (format: 'md' | 'json') => {
    const exported = { ...currentCase, evidence: allEvidence, revisions };
    const content =
      format === 'json'
        ? JSON.stringify(exported, null, 2)
        : `# Research Courtroom — ${currentCase.id}\n\n## Question\n${currentCase.question}\n\n## Verdict: ${currentCase.decision}\n${currentCase.verdict}\n\n## Claims\n${allClaims
            .map(c => `- **${c.id} · ${c.status}**: ${c.text} (${c.evidenceIds.join(', ')})`)
            .join('\n')}\n\n## Evidence ledger\n${allEvidence
            .map(e => `### ${e.id}: ${e.title}\n${e.url}\n\n> ${e.excerpt}\n\nOrigin: ${e.origin}; retrieved: ${e.retrievedAt}; admitted: ${e.admitted}\nQuery: ${e.query}`)
            .join('\n\n')}\n\n## Revision history\n${revisions
            .map(
              r =>
                `### Revision ${r.id} · ${r.status}\nChallenge: ${r.challenge}\nTarget: ${r.target}\nDecision: ${r.beforeDecision} → ${r.afterDecision}\nVerified claims: ${r.beforeVerified} → ${r.afterVerified}\nEvidence added: ${r.evidenceAdded.join(', ') || 'None'}\n${r.explanation}`
            )
            .join('\n\n')}`;
    const url = URL.createObjectURL(
      new Blob([content], { type: format === 'json' ? 'application/json' : 'text/markdown' })
    );
    const link = document.createElement('a');
    link.href = url;
    link.download = `research-courtroom-${currentCase.id}.${format}`;
    link.click();
    URL.revokeObjectURL(url);
    setExportOpen(false);
  };

  const filteredEvidence = allEvidence.filter(
    item =>
      filter === 'All' ||
      (filter === 'Search' && ['search', 'search_hint'].includes(item.origin)) ||
      (filter === 'User-submitted' && item.origin === 'user_url_fetch') ||
      (filter === 'Blocked' && item.origin === 'blocked')
  );

  return (
    <>
      <header className="site-header">
        <div className="shell header-inner">
          <div className="brand">
            <span className="brand-icon">
              <Scale size={24} strokeWidth={1.5} />
            </span>
            <div>
              <div className="brand-name">Research Courtroom</div>
              <div className="brand-subtitle">Two sides argue. Evidence decides. Traceable verdicts.</div>
            </div>
          </div>
          <div className="header-actions">
            <Button variant="outline" onClick={() => setLedgerOpen(true)} aria-label="Open evidence ledger">
              <BookOpen />
              <span className="header-action-label">Evidence ledger</span>
              <span className="count">{allEvidence.length} sources</span>
            </Button>
            <Button variant="ghost" onClick={() => setExportOpen(true)} aria-label="Export case summary">
              <ArrowDownToLine />
              <span className="header-action-label">Export case</span>
            </Button>
          </div>
        </div>
      </header>

      <main className="shell">
        <section className="filing">
          <img className="filing-image" src={scales.url} alt="Balanced bronze scales of justice" />
          <div className="eyebrow">
            <span className="status-dot" /> THE COURT IS IN SESSION
          </div>
          <h1>Put your question on trial.</h1>
          <p>Not another AI summary. A case built on evidence, tested by opposing sides.</p>
          <form className="filing-form" onSubmit={openTrial}>
            <Search size={18} />
            <input
              aria-label="Research question"
              value={question}
              onChange={e => setQuestion(e.target.value)}
              placeholder="e.g., Does intermittent fasting improve long-term weight loss compared with calorie restriction?"
              required
            />
            <Button disabled={isLoading} type="submit">
              {isLoading ? <LoaderCircle className="animate-spin" /> : <Gavel size={15} />}
              {isLoading ? 'Trial in session' : 'Open trial'}
              {!isLoading && <ArrowRight />}
            </Button>
          </form>
          <div className="presets">
            <span>Try a case</span>
            {presets.map(([label, value]) => (
              <Button
                key={label}
                variant="outline"
                size="sm"
                onClick={() => {
                  setQuestion(value);
                  setFilingNotice('');
                }}
              >
                {label}
                <ChevronRight size={10} />
              </Button>
            ))}
          </div>
          {filingNotice && (
            <div className="notice" role="status">
              <Info size={14} />
              {filingNotice}
            </div>
          )}
        </section>

        <div className="case-meta">
          <div className="meta-left">
            <span className="case-id">{currentCase.id}</span>
            <span>Adversarial research</span>
            <span>
              <span className={`status-dot ${isLoading ? 'bg-gold animate-ping' : ''}`} />
              {isLoading ? 'Deliberation in progress' : 'Trial concluded'}
            </span>
            <span className="count flex items-center gap-1">
              {isLive ? <Sparkles size={11} className="text-gold" /> : null}
              {isLive ? 'LIVE NEBIUS TRIAL' : 'SAMPLE CASE'}
            </span>
          </div>
          <div className="meta-right">
            <Clock3 size={12} />
            <span>{allClaims.length} claims examined</span>
            <span>{allEvidence.length} sources</span>
          </div>
        </div>

        {(isLoading || liveEvents.length > 0) && (
          <section className="live-stream-box" aria-live="polite">
            <div className="live-stream-header">
              <div className="live-stream-title">
                <span className={isLoading ? "live-pulse" : "status-dot"} />
                {isLoading ? "LIVE DELIBERATION STREAM" : "DELIBERATION STREAM TRANSCRIPT"}
              </div>
              <div className="flex items-center gap-2">
                <span className="live-stream-stage">
                  {isLoading ? (currentStageName || 'DELIBERATING') : 'CASE SEALED'}
                </span>
                <span className="count">{liveEvents.length} events</span>
              </div>
            </div>
            <div className="live-stream-events">
              {liveEvents.slice().reverse().map((ev) => (
                <div className="live-stream-event" key={ev.id}>
                  <span className="live-stream-time">[{ev.timestamp}]</span>
                  <span className="flex-1 font-mono text-[11px] leading-relaxed">
                    {ev.type === 'phase' && <Sparkles size={11} className="inline mr-1.5 text-gold" />}
                    {ev.type === 'evidence' && <BookOpen size={11} className="inline mr-1.5 text-judicial" />}
                    {ev.type === 'prosecution' && <Gavel size={11} className="inline mr-1.5 text-prosecution" />}
                    {ev.type === 'defense' && <Shield size={11} className="inline mr-1.5 text-defense" />}
                    {ev.type === 'cross_exam' && <MessageSquare size={11} className="inline mr-1.5 text-gold" />}
                    {ev.type === 'verdict' && <Scale size={11} className="inline mr-1.5 text-judicial" />}
                    {ev.type === 'complete' && <CheckCheck size={11} className="inline mr-1.5 text-green-400" />}
                    {ev.message}
                  </span>
                </div>
              ))}
            </div>
          </section>
        )}

        {isLoading && (
          <div className="workflow" aria-live="polite">
            {stages.map((name, index) => (
              <div key={name} className="contents">
                <div className={`workflow-item ${stage === index ? 'active' : ''}`}>
                  {stage === index ? (
                    <LoaderCircle size={14} className="animate-spin" />
                  ) : (
                    <CircleCheck size={14} />
                  )}
                  <span>{name}</span>
                </div>
                {index < stages.length - 1 && (
                  <ChevronRight size={12} className="text-muted-foreground workflow-arrow" />
                )}
              </div>
            ))}
          </div>
        )}

        {currentCase.warnings && currentCase.warnings.length > 0 && (
          <div className="space-y-2 mb-4">
            {currentCase.warnings.map((w, idx) => (
              <div key={idx} className="notice error" role="alert">
                <TriangleAlert size={14} />
                {w}
              </div>
            ))}
          </div>
        )}

        <div className="section-heading">
          <h2>
            <span className="number">01</span>Opening arguments
          </h2>
          <span>Two perspectives. One evidence standard.</span>
          {revisions.length > 0 && isLive && (
            <span className="count text-gold ml-auto flex items-center gap-1">
              <Sparkles size={11} /> Re-evaluated with Challenge #{revisions.length} Evidence
            </span>
          )}
        </div>
        <div className="arguments">
          <Argument
            side="prosecution"
            claims={currentCase.prosecution}
            summary={currentCase.prosecutionSummary}
            limitations={currentCase.prosecutionLimitations}
            isLive={isLive}
            isLoading={isLoading}
            onSelect={selectSource}
          />
          <Argument
            side="defense"
            claims={currentCase.defense}
            summary={currentCase.defenseSummary}
            limitations={currentCase.defenseLimitations}
            isLive={isLive}
            isLoading={isLoading}
            onSelect={selectSource}
          />
        </div>

        <section className="cross-exam">
          <Button
            variant="ghost"
            className="disclosure-button"
            aria-expanded={crossOpen}
            onClick={() => setCrossOpen(!crossOpen)}
          >
            <span className="disclosure-title">
              <MessageSquare size={16} />Cross-examination
            </span>
            <span className="disclosure-end">
              <span className="count">{exchanges.length} exchanges</span>
              {crossOpen ? <ChevronDown /> : <ChevronRight />}
            </span>
          </Button>
          {crossOpen && (
            <div className="thread">
              {isLoading && exchanges.length === 0 ? (
                <div className="p-5 border border-dashed border-border/70 rounded-md bg-secondary/30 text-center my-2">
                  <LoaderCircle className="animate-spin mx-auto mb-1 text-gold" size={16} />
                  <p className="text-xs text-muted-foreground font-mono">
                    Counsel preparing cross-examination questions on evidence veracity...
                  </p>
                </div>
              ) : exchanges.length === 0 ? (
                <div className="notice text-xs text-muted-foreground">
                  Cross-examination will appear once counsel presents their preliminary examination.
                </div>
              ) : (
                exchanges.map((exchange, index) => (
                  <div className="exchange" key={index}>
                    <span className="claim-number">EXCHANGE 0{index + 1}</span>
                    <p>
                      <strong className={exchange.side === 'Prosecution' ? 'text-prosecution' : 'text-defense'}>
                        {exchange.side} asks
                      </strong>{' '}
                      · {exchange.question}
                    </p>
                    <p>
                      <strong className={exchange.side === 'Prosecution' ? 'text-defense' : 'text-prosecution'}>
                        {exchange.side === 'Prosecution' ? 'Defense' : 'Prosecution'} responds
                      </strong>{' '}
                      · {exchange.answer}
                    </p>
                    <Citations ids={exchange.ids} onSelect={selectSource} />
                  </div>
                ))
              )}
            </div>
          )}
        </section>

        <div className="section-heading">
          <h2>
            <span className="number">02</span>The court's decision
          </h2>
          <span>Evidence weighed. Not rhetoric.</span>
        </div>
        <section className="verdict">
          <div className="verdict-header">
            <div className="verdict-heading">
              <span className="judge-icon">
                <Scale size={23} strokeWidth={1.5} />
              </span>
              <div>
                <h3>Judicial verdict</h3>
                <p>Independent assessment of the evidence ledger</p>
              </div>
            </div>
            <span className="verdict-badge">
              <ShieldCheck size={12} />EVIDENCE-GROUNDED
            </span>
          </div>

          {showRevisionDiff && revisions.length > 0 && (
            <div className="notice">
              <History size={14} />
              Revision #{revisions.length}: {revisions[revisions.length - 1].explanation}
            </div>
          )}

          {isLoading && !currentCase.verdict ? (
            <div className="p-8 border border-dashed border-border/80 rounded-md bg-secondary/30 text-center my-4">
              <Scale className="animate-pulse mx-auto mb-3 text-gold" size={28} />
              <h4 className="font-serif text-base mb-1">Deliberation in progress</h4>
              <p className="text-xs text-muted-foreground font-mono">
                The court is weighing affirmative and opposing arguments against verified ledger citations...
              </p>
            </div>
          ) : (
            <>
              <div className="decision">
                <div className="decision-label">THE RULING · {currentCase.decision.toUpperCase()}</div>
                <h4>{currentCase.decision}</h4>
                <p>{currentCase.verdict}</p>
              </div>

              <div className="reasoning-title">Judicial reasoning</div>
              <p className="reasoning">{currentCase.verdict}</p>
            </>
          )}

          {currentCase.verdictClaims && currentCase.verdictClaims.length > 0 && (
            <table className="verdict-table">
              <thead>
                <tr>
                  <th>Finding</th>
                  <th>Assessment</th>
                  <th>Evidence</th>
                </tr>
              </thead>
              <tbody>
                {currentCase.verdictClaims.map(claim => (
                  <tr key={claim.id}>
                    <td>{claim.text}</td>
                    <td>
                      <Status claim={claim} />
                    </td>
                    <td>
                      <Citations ids={claim.evidenceIds} onSelect={selectSource} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {currentCase.unresolved && currentCase.unresolved.length > 0 && (
            <div className="unresolved">
              <TriangleAlert size={15} />
              <div>
                <strong>Questions the evidence cannot yet settle</strong>
                {currentCase.unresolved.join(' · ')}
              </div>
            </div>
          )}

          <div className="flex justify-between items-center gap-3 mt-4 text-muted-foreground text-[9px]">
            <span className="flex items-center gap-1">
              <CheckCheck size={12} />
              {allClaims.filter(c => c.verification?.verified).length} verified claims
            </span>
            {revisions.length > 0 && (
              <Button
                variant="ghost"
                size="sm"
                className="text-[9px] h-6"
                onClick={() => {
                  setHistoryOpen(true);
                  document.getElementById('revision-history')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }}
              >
                Revision {revisions.length}
                <History size={11} />
              </Button>
            )}
          </div>
        </section>

        <section className="challenge-section">
          <div className="challenge-heading">
            <h2>
              <MessageSquare size={17} className="text-gold" />Cross-examine the court
            </h2>
            <span>A verdict is only as strong as the evidence behind it.</span>
          </div>
          <form className="challenge-form" onSubmit={submitChallenge}>
            <div className="field">
              <label htmlFor="target-claim">Target of challenge</label>
              <select id="target-claim" value={target} onChange={e => setTarget(e.target.value)}>
                <option value="Whole verdict">Whole verdict</option>
                {allClaims.map(c => (
                  <option key={c.id} value={c.id}>
                    {c.id} · {c.text.slice(0, 48)}…
                  </option>
                ))}
              </select>
            </div>
            <div className="field">
              <label htmlFor="challenge">Your argument or question</label>
              <textarea
                id="challenge"
                value={challenge}
                onChange={e => setChallenge(e.target.value)}
                placeholder="Challenge an argument or ask a follow-up…"
              />
            </div>
            <div className="challenge-bottom">
              <div className="field">
                <label htmlFor="source-url" className="flex items-center gap-1">
                  <Link2 size={11} />Additional source URL{' '}
                  <span className="text-muted-foreground">(fetched under strict SSRF & verification limits)</span>
                </label>
                <input
                  id="source-url"
                  value={sourceUrl}
                  onChange={e => setSourceUrl(e.target.value)}
                  placeholder="https://journal.org/research-paper"
                />
              </div>
              <Button type="submit" variant="outline" disabled={isLoading}>
                {isLoading ? <LoaderCircle className="animate-spin" /> : <Gavel size={14} />}
                Challenge verdict
                <ArrowRight size={14} />
              </Button>
            </div>
          </form>
          {error && (
            <div className="notice error" role="alert">
              <Shield size={15} />
              {error}
            </div>
          )}
          {notice && (
            <div className="notice" role="status">
              <Info size={15} />
              {notice}
            </div>
          )}
        </section>

        <section className="history" id="revision-history">
          <Button
            variant="ghost"
            className="disclosure-button"
            aria-expanded={historyOpen}
            onClick={() => setHistoryOpen(!historyOpen)}
          >
            <span className="disclosure-title">
              <History size={16} />Verdict revision history
              <span className="count">{revisions.length}</span>
            </span>
            <span className="disclosure-end">{historyOpen ? <ChevronDown /> : <ChevronRight />}</span>
          </Button>
          {historyOpen &&
            revisions.map(revision => (
              <div className="revision" key={revision.id}>
                <h4>
                  Revision {revision.id}
                  <span className="count">
                    {revision.status === 'sample' ? 'SAMPLE REVISION' : 'EVIDENCE REVISION'}
                  </span>
                </h4>
                <p>{revision.challenge}</p>
                <div className="diff-pills">
                  <span>
                    Decision: {revision.beforeDecision} → {revision.afterDecision}
                  </span>
                  <span>
                    Verified claims: {revision.beforeVerified} → {revision.afterVerified}
                  </span>
                </div>
                <p>{revision.explanation}</p>
                <div className="flex items-center gap-2 text-[10px] text-muted-foreground">
                  Evidence added:{' '}
                  {revision.evidenceAdded && revision.evidenceAdded.length ? (
                    <Citations ids={revision.evidenceAdded} onSelect={selectSource} />
                  ) : (
                    'None'
                  )}
                  {revision.urlStatus && revision.urlStatus !== 'none' && (
                    <span>· URL status: {revision.urlStatus}</span>
                  )}
                </div>
              </div>
            ))}
        </section>

        <footer className="footer">
          <span>
            <Scale size={12} />Research Courtroom<span>·</span>Evidence over eloquence.
          </span>
          <span>
            <ShieldCheck size={12} />All claims verified against evidence excerpts.
          </span>
        </footer>
      </main>

      <Sheet open={ledgerOpen} onOpenChange={setLedgerOpen}>
        <SheetContent className="ledger-sheet">
          <SheetTitle className="font-display flex items-center gap-2">
            <BookOpen size={20} className="text-gold" />Evidence ledger
          </SheetTitle>
          <SheetDescription>
            {allEvidence.length} sources preserved with exact excerpts · {blockedSources.length} blocked
          </SheetDescription>
          <div className="ledger-filters">
            {['All', 'Search', 'User-submitted', 'Blocked'].map(name => (
              <Button
                key={name}
                variant={filter === name ? 'secondary' : 'ghost'}
                size="sm"
                onClick={() => setFilter(name)}
              >
                {name}
              </Button>
            ))}
          </div>
          {filteredEvidence.length === 0 && <div className="notice">No sources in this category.</div>}
          {filteredEvidence.map(item => (
            <EvidenceItem key={item.id} item={item} />
          ))}
        </SheetContent>
      </Sheet>

      <Dialog open={!!selectedSource} onOpenChange={open => { if (!open) setSelectedSource(undefined); }}>
        <DialogContent className="max-h-[85vh] overflow-y-auto">
          <DialogTitle className="font-display">Evidence {selectedSource?.id}</DialogTitle>
          <DialogDescription>Source record · exact excerpt · evidence ledger</DialogDescription>
          {selectedSource && <EvidenceItem item={selectedSource} />}
        </DialogContent>
      </Dialog>

      <Dialog open={exportOpen} onOpenChange={setExportOpen}>
        <DialogContent>
          <DialogTitle className="font-display">Export case summary</DialogTitle>
          <DialogDescription>
            Include arguments, evidence excerpts, source metadata, and the complete revision history.
          </DialogDescription>
          <div className="export-options">
            <Button variant="outline" onClick={() => download('md')}>
              <FileText />Markdown document
              <ArrowDownToLine className="ml-auto" />
            </Button>
            <Button variant="outline" onClick={() => download('json')}>
              <FileJson />Structured JSON
              <ArrowDownToLine className="ml-auto" />
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}
