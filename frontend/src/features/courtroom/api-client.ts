import type { Case, Claim, Evidence, Exchange } from './types';

const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  (typeof window !== 'undefined' && window.location.port === '8000' ? '' : 'http://localhost:8000');

export interface StreamEvent {
  type:
    | 'phase'
    | 'evidence'
    | 'prosecution'
    | 'defense'
    | 'arguments_updated'
    | 'cross_exam'
    | 'verdict'
    | 'complete'
    | 'url_admitted'
    | 'error';
  stage?: string;
  message?: string;
  count?: number;
  evidence?: Evidence[];
  added?: Evidence[];
  claims?: Claim[];
  summary?: string;
  limitations?: string[];
  prosecutionClaims?: Claim[];
  defenseClaims?: Claim[];
  prosecutionSummary?: string;
  defenseSummary?: string;
  exchanges?: Exchange[];
  verdictClaims?: Claim[];
  decision?: string;
  reasoning?: string;
  unresolved?: string[];
  revisions?: any[];
  case?: Case;
  url_status?: string;
}

export async function checkApiHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/api/health`, { method: 'GET' });
    return res.ok;
  } catch {
    return false;
  }
}

async function readSSEStream(res: Response, onEvent: (event: StreamEvent) => void): Promise<Case> {
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: `HTTP error ${res.status}` }));
    throw new Error(err.detail || `Server returned ${res.status}`);
  }
  const reader = res.body?.getReader();
  if (!reader) throw new Error('Response body is not readable');

  const decoder = new TextDecoder();
  let buffer = '';
  let finalCase: Case | null = null;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const blocks = buffer.split('\n\n');
    buffer = blocks.pop() || '';

    for (const block of blocks) {
      const trimmed = block.trim();
      if (!trimmed) continue;
      const dataLine = trimmed.split('\n').find((l) => l.startsWith('data: '));
      if (dataLine) {
        try {
          const parsed: StreamEvent = JSON.parse(dataLine.slice(6));
          if (parsed.type === 'error') {
            throw new Error(parsed.message || 'Stream error occurred');
          }
          if (parsed.type === 'complete' && parsed.case) {
            finalCase = parsed.case;
          }
          onEvent(parsed);
        } catch (e: any) {
          if (e.message && !e.message.includes('JSON')) {
            throw e;
          }
        }
      }
    }
  }

  if (buffer.trim().startsWith('data: ')) {
    try {
      const parsed: StreamEvent = JSON.parse(buffer.trim().slice(6));
      if (parsed.type === 'complete' && parsed.case) {
        finalCase = parsed.case;
      }
      onEvent(parsed);
    } catch {}
  }

  if (!finalCase) {
    throw new Error('Stream ended without final case summary');
  }
  return finalCase;
}

export async function fileCaseStreamApi(
  question: string,
  onEvent: (event: StreamEvent) => void
): Promise<Case> {
  const res = await fetch(`${API_BASE}/api/case/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });
  return readSSEStream(res, onEvent);
}

export async function challengeCaseStreamApi(
  caseRaw: any,
  challenge: string,
  sourceUrl: string = '',
  targetClaim: string = '',
  onEvent: (event: StreamEvent) => void
): Promise<Case> {
  const res = await fetch(`${API_BASE}/api/challenge/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      case_raw: caseRaw,
      challenge,
      source_url: sourceUrl,
      target_claim: targetClaim,
    }),
  });
  return readSSEStream(res, onEvent);
}

export async function fileCaseApi(question: string): Promise<Case> {
  const res = await fetch(`${API_BASE}/api/case`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: `HTTP error ${res.status}` }));
    throw new Error(err.detail || `Server returned ${res.status}`);
  }
  return res.json();
}

export async function challengeCaseApi(
  caseRaw: any,
  challenge: string,
  sourceUrl: string = '',
  targetClaim: string = ''
): Promise<Case> {
  const res = await fetch(`${API_BASE}/api/challenge`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      case_raw: caseRaw,
      challenge,
      source_url: sourceUrl,
      target_claim: targetClaim,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: `HTTP error ${res.status}` }));
    throw new Error(err.detail || `Server returned ${res.status}`);
  }
  return res.json();
}
