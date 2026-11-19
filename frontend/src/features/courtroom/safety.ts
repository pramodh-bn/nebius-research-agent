// Preliminary browser screening only. No URLs are fetched or admitted here.
export function screenSourceUrl(value: string): 'empty' | 'blocked' | 'invalid' | 'pending' {
  if (!value.trim()) return 'empty';
  try {
    const url = new URL(value.trim());
    const host = url.hostname.toLowerCase().replace(/^\[|\]$/g, '');
    if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password) return 'blocked';
    if (!host.includes('.') || host === 'localhost' || host.endsWith('.localhost') || host.endsWith('.local') || host.endsWith('.internal')) return 'blocked';
    if (host.includes(':')) return 'blocked';
    if (/^\d+\.\d+\.\d+\.\d+$/.test(host)) {
      const [a = 0, b = 0] = host.split('.').map(Number);
      if (a === 0 || a === 10 || a === 127 || a === 169 && b === 254 || a === 172 && b >= 16 && b <= 31 || a === 192 && b === 168 || a === 100 && b >= 64 && b <= 127 || a >= 224) return 'blocked';
    }
    return 'pending';
  } catch { return 'invalid'; }
}