// pages/api/analyze-file.js
import { createClient } from '@supabase/supabase-js';
import OpenAI from 'openai';

const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY);
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  try {
    const { path } = req.body;
    if (!path) return res.status(400).json({ error: 'path required' });

    // Download file from Supabase storage
    const { data, error } = await supabase.storage.from('uploads').download(path);
    if (error || !data) {
      console.error(error);
      return res.status(500).json({ error: 'Failed to download file' });
    }

    // Read text (works for text/* files). Convert to string.
    const arrayBuffer = await data.arrayBuffer();
    const text = new TextDecoder().decode(arrayBuffer);

    // Call OpenAI to summarize
    const prompt = `Summarize the following text in 5-8 bullet points and give a 1-line title:\n\n${text}`;

    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 500
    });

    const summary = response.choices?.[0]?.message?.content || 'No summary generated';
    return res.status(200).json({ summary });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: err.message || 'internal error' });
  }
}
