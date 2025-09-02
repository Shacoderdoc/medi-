// pages/upload.js
import { useState } from 'react';
import Nav from '../components/Nav';
import { supabase } from '../lib/supabaseClient';

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [analysis, setAnalysis] = useState('');

  async function handleUpload(e) {
    e.preventDefault();
    if (!file) return alert('Choose a file');
    setStatus('Uploading...');
    const fileName = `${Date.now()}_${file.name}`;
    const { data, error } = await supabase.storage.from('uploads').upload(fileName, file, {
      cacheControl: '3600',
      upsert: false
    });
    if (error) {
      setStatus('Upload error: ' + error.message);
      return;
    }
    setStatus('Uploaded. Analyzing...');
    // Call server analyze
    const res = await fetch('/api/analyze-file', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: data.path })
    });
    const json = await res.json();
    if (json.summary) {
      setAnalysis(json.summary);
      setStatus('Analysis complete');
    } else {
      setStatus('Analysis failed');
    }
  }

  return (
    <>
      <Nav />
      <main className="max-w-3xl mx-auto py-12 px-4">
        <h1 className="text-2xl font-semibold mb-4">File Upload & Analysis</h1>

        <form onSubmit={handleUpload} className="space-y-3">
          <input type="file" onChange={(e) => setFile(e.target.files?.[0])} />
          <div>
            <button className="px-4 py-2 bg-indigo-600 text-white rounded">Upload & Analyze</button>
          </div>
        </form>

        <div className="mt-6">
          <div className="text-sm text-gray-500 mb-2">Status: {status}</div>
          {analysis && (
            <div className="p-3 bg-white rounded shadow-sm">
              <h3 className="font-medium mb-2">Summary / Analysis</h3>
              <div className="whitespace-pre-wrap">{analysis}</div>
            </div>
          )}
        </div>
      </main>
    </>
  );
}
