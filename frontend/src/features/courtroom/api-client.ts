import type { Case } from './types';

const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  (typeof window !== 'undefined' && window.location.port === '8000' ? '' : 'http://localhost:8000');

export async function checkApiHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/api/health`, { method: 'GET' });
    return res.ok;
  } catch {
    return false;
  }
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
