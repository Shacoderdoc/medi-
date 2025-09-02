// pages/api/chat.js
import { NextResponse } from 'next/server';
import OpenAI from 'openai';

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { messages } = req.body; // [{ role: 'user', content: '...'}]
    if (!messages) return res.status(400).json({ error: 'messages required' });

    const response = await client.chat.completions.create({
      model: 'gpt-4o-mini', // change model as you prefer
      messages,
      max_tokens: 700
    });

    const assistantMsg = response.choices?.[0]?.message || { role: 'assistant', content: '' };
    return res.status(200).json({ message: assistantMsg });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: err.message || 'AI error' });
  }
}
