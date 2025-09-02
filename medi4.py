// pages/ai.js
import { useState } from 'react';
import Nav from '../components/Nav';

export default function AIPage() {
  const [messages, setMessages] = useState([{ role: 'system', content: 'You are a helpful assistant for a hackathon demo.' }]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  async function sendMessage(e) {
    e?.preventDefault();
    if (!input.trim()) return;
    const userMsg = { role: 'user', content: input.trim() };
    const nextMessages = [...messages, userMsg];
    setMessages(nextMessages);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: nextMessages })
      });
      const data = await res.json();
      if (data.message) {
        setMessages((m) => [...m, data.message]);
      } else {
        setMessages((m) => [...m, { role: 'assistant', content: 'No response from AI' }]);
      }
    } catch (err) {
      setMessages((m) => [...m, { role: 'assistant', content: 'Error talking to AI: ' + String(err) }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Nav />
      <main className="max-w-3xl mx-auto py-12 px-4">
        <h1 className="text-2xl font-semibold mb-4">AI Assistant (Demo)</h1>

        <div className="mb-4 space-y-2">
          {messages.filter(m => m.role !== 'system').map((m, i) => (
            <div key={i} className={`p-3 rounded ${m.role === 'user' ? 'bg-indigo-50 self-end' : 'bg-gray-100'}`}>
              <div className="text-sm text-gray-600">{m.role}</div>
              <div className="mt-1 whitespace-pre-wrap">{m.content}</div>
            </div>
          ))}
        </div>

        <form onSubmit={sendMessage} className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask something..."
            className="flex-1 p-2 border rounded"
            disabled={loading}
          />
          <button className="px-4 py-2 bg-indigo-600 text-white rounded" disabled={loading}>
            {loading ? 'Thinking...' : 'Send'}
          </button>
        </form>
      </main>
    </>
  );
}
