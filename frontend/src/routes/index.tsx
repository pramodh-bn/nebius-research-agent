import { createFileRoute } from "@tanstack/react-router";
import { Courtroom } from '@/features/courtroom/courtroom';

// The home route ships no og:image, so serve-time hosting can inject the
// project's social preview (explicit og:image or latest screenshot).
export const Route = createFileRoute("/")({
  head: () => ({ meta: [
    { title: 'Research Courtroom — The Evidence Trial' },
    { name: 'description', content: 'Examine both sides of a contested research question, inspect the evidence, and challenge a traceable judicial verdict.' },
    { property: 'og:title', content: 'Research Courtroom — The Evidence Trial' },
    { property: 'og:description', content: 'Two sides argue. Evidence decides. Explore an adversarial research trial with a transparent evidence ledger.' },
    { property: 'og:type', content: 'website' },
    { name: 'twitter:card', content: 'summary_large_image' },
  ] }),
  component: Index,
});

// IMPORTANT: Replace this placeholder. See ./README.md for routing conventions.
function Index() {
  return <Courtroom />;
}
