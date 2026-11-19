export type ClaimStatus = 'supported' | 'contested' | 'unsupported';

export interface Evidence {
  id: string;
  title: string;
  url: string;
  domain: string;
  excerpt: string;
  query: string;
  retrievedAt: string;
  origin: 'search' | 'user_url_fetch' | 'search_hint' | 'blocked';
  kind: string;
  untrusted: boolean;
  admitted: boolean;
  metadata?: Record<string, any>;
}

export interface Verification {
  assessment: ClaimStatus;
  verified: boolean;
  method: 'sample_assessment' | 'llm';
  note: string;
}

export interface Claim {
  id: string;
  text: string;
  status: ClaimStatus;
  evidenceIds: string[];
  verification: Verification;
}

export interface Revision {
  id: number;
  timestamp: string;
  challenge: string;
  target: string;
  beforeDecision: string;
  afterDecision: string;
  beforeVerified: number;
  afterVerified: number;
  evidenceAdded: string[];
  explanation: string;
  status: 'sample' | 'admitted' | 'pending';
  urlStatus?: string;
  sourceUrl?: string;
}

export interface Exchange {
  side: 'Prosecution' | 'Defense';
  question: string;
  answer: string;
  ids: string[];
  verified?: boolean;
}

export interface Case {
  id: string;
  question: string;
  decision: string;
  verdict: string;
  prosecution: Claim[];
  defense: Claim[];
  verdictClaims?: Claim[];
  prosecutionSummary?: string;
  defenseSummary?: string;
  prosecutionLimitations?: string[];
  defenseLimitations?: string[];
  unresolved?: string[];
  exchanges?: Exchange[];
  evidence: Evidence[];
  revisions: Revision[];
  warnings?: string[];
  evidenceWarning?: string;
  callsUsed?: number;
  mode: 'sample' | 'live';
  _raw?: any;
}
