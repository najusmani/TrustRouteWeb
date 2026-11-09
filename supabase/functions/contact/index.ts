// Supabase Edge Function entry point: POST https://<project-ref>.supabase.co/functions/v1/contact
// All logic lives in handler.js. Secrets are read from the function's environment
// (set them with `supabase secrets set ...`; see SETUP.md).
import { createHandler } from './handler.js';

Deno.serve(createHandler({ env: (name: string) => Deno.env.get(name) }));
