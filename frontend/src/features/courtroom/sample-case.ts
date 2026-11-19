import type { Case, Claim, ClaimStatus, Evidence } from './types';

export const sampleQuestion = 'Does intermittent fasting improve long-term weight loss compared with calorie restriction?';
const query = 'intermittent fasting vs continuous calorie restriction randomized trial long-term weight loss';
const timestamp = '2026-11-19T20:06:00Z';
const source = (id: string, title: string, url: string, excerpt: string, kind: string, origin: Evidence['origin'] = 'search'): Evidence => ({ id, title, url, domain: new URL(url).hostname.replace('www.', ''), excerpt, kind, origin, query, retrievedAt: timestamp, untrusted: false, admitted: true });
export const evidence: Evidence[] = [
  source('E1', 'Diet Review: Intermittent Fasting for Weight Loss', 'https://nutritionsource.hsph.harvard.edu/healthy-weight/diet-reviews/intermittent-fasting/', 'However, research does not consistently show that intermittent fasting is superior to continuous low calorie diets for weight loss efficiency.', 'Research review'),
  source('E2', 'Intermittent vs. continuous energy restriction: a 12-month trial', 'https://www.nature.com/articles/s41366-018-0247-2', 'For the 146 individuals who completed the study (124 female, 22 male, mean BMI 33 kg/m 2) mean weight loss, and body fat loss at 12 months was similar in the three intervention groups', 'Randomized trial'),
  source('E3', 'Calorie Restriction with or without Time-Restricted Eating', 'https://www.nejm.org/doi/full/10.1056/NEJMoa2114833', 'Changes in weight were not significantly different in the two groups at the 12-month assessment (net difference, −1.8 kg; 95% CI, −4.0 to 0.4; P=0.11).', 'Randomized trial'),
  source('E4', 'Effects of intermittent energy restriction on body composition', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10831889/', 'Twenty-eight trials were identified that studied TRE (k = 7), ADF (k = 10), or the 5:2 diet (k = 11) for 2–52 wk.', 'Meta-analysis'),
  source('E5', 'Time-restricted eating with calorie restriction: a meta-analysis', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10630127/', 'Eight RCTs involving 579 participants were enrolled in the present analysis.', 'Meta-analysis'),
  source('E6', 'Intermittent vs. continuous calorie restriction over 50 weeks', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6915821/', 'We conducted a randomized controlled trial to test whether ICR, operationalized as the “5:2 diet,” has stronger effects on adipose tissue gene expression, anthropometric and body composition measures, and circulating metabolic biomarkers than CCR and a control regimen.', 'Randomized trial'),
  source('E7', 'Long-term weight and cardiometabolic outcomes', 'https://www.nature.com/articles/s41366-020-0525-7', '109 overweight and obese adults, aged 18–72 years, attended a 12-month follow-up after completing a 12-month dietary intervention involving three groups', 'Follow-up study'),
  source('E8', 'Isocaloric intermittent fasting vs. daily caloric restriction', 'https://www.sciencedirect.com/science/article/pii/S2212267222009151', 'To systematically investigate the effects of isocaloric IF vs DCR on metabolic risk factors for noncommunicable chronic diseases in adults with overweight and obesity.', 'Systematic review'),
  source('E9', 'The Effect of 4:3 Intermittent Fasting on Weight Loss at 12 Months', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12863240/', 'Of the 165 (4:3 IMF, n=84; DCR, n=81) randomized participants (mean±SD; age 42±9 years, BMI 34.1±4.4 kg/m 2, 73.9% female), 125 completed the trial.', 'Randomized trial', 'search_hint'),
  source('E10', 'Fasting vs. calorie restriction for weight loss: Which one wins?', 'https://www.harvardhealth.org/healthy-aging-and-longevity/fasting-vs-calorie-restriction-for-weight-loss-which-one-wins', 'After one year, people in the 4:3 group had lost more weight - an average of about 6 more pounds - than people in the calorie restriction group.', 'Clinical commentary', 'search_hint'),
];
const claim = (id: string, text: string, status: ClaimStatus, evidenceIds: string[]): Claim => ({ id, text, status, evidenceIds, verification: { assessment: status, verified: status === 'supported', method: 'sample_assessment', note: 'Sample LLM verifier opinion, not proof. This assessment has not been generated live.' } });
export const sampleCase: Case = {
  id: 'RC-2026-001', question: sampleQuestion, mode: 'sample', decision: 'Inconclusive',
  verdict: 'Intermittent fasting does not consistently improve long-term weight loss compared to calorie restriction; most evidence shows equivalent outcomes.',
  prosecution: [
    claim('P1', 'Some fasting protocols produce modestly greater weight loss when paired with behavioral support.', 'supported', ['E9', 'E10']),
    claim('P2', 'Early time-restricted eating can add a small weight-loss benefit to calorie restriction.', 'supported', ['E5']),
    claim('P3', 'Fasting is inherently more sustainable than daily calorie restriction for everyone.', 'contested', ['E1', 'E6']),
  ],
  defense: [
    claim('D1', 'At 12 months, time-restricted eating does not significantly outperform calorie restriction alone.', 'supported', ['E3']),
    claim('D2', 'Across 28 trials, weight-loss outcomes were comparable between the two approaches.', 'supported', ['E4', 'E8']),
    claim('D3', 'Long-term follow-up finds no clear advantage for intermittent energy restriction.', 'supported', ['E2', 'E7']),
  ],
  evidence,
  revisions: [{ id: 1, timestamp, challenge: 'Does the newer 4:3 fasting trial change the conclusion?', target: 'Whole verdict', beforeDecision: 'Inconclusive', afterDecision: 'Inconclusive', beforeVerified: 4, afterVerified: 5, evidenceAdded: ['E9', 'E10'], explanation: 'The 2025 trial supports a modest benefit for the 4:3 protocol with intensive behavioral support. The broad verdict remains unchanged, but its reasoning now distinguishes protocol-specific results from general superiority. E10 reports the same trial as E9, not independent evidence.', status: 'sample' }],
};