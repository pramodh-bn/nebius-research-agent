import { describe, expect, it } from 'vitest';
import { screenSourceUrl } from '@/features/courtroom/safety';
import { sampleCase } from '@/features/courtroom/sample-case';

describe('Source admission safety', () => {
  it('blocks the metadata service address specified in the brief', () => {
    expect(screenSourceUrl('http://169.254.169.254/latest/meta-data')).toBe('blocked');
  });
  it('blocks localhost before any fetch', () => {
    expect(screenSourceUrl('http://localhost:8080/private')).toBe('blocked');
  });
  it('never treats a public URL as verified evidence', () => {
    expect(screenSourceUrl('https://www.nature.com/articles/example')).toBe('pending');
  });
  it('blocks alternative loopback encodings', () => {
    expect(screenSourceUrl('http://2130706433')).toBe('blocked');
    expect(screenSourceUrl('http://[::1]')).toBe('blocked');
  });
});
describe('Sample case evidence', () => {
  it('includes original E1–E8 plus E9 and E10 in the sample revision', () => {
    expect(sampleCase.evidence.map(item => item.id)).toEqual(['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10']);
    expect(sampleCase.revisions[0]?.evidenceAdded).toEqual(['E9', 'E10']);
  });
});