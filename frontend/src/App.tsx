import React, { useState } from "react";
import StudyForm from "./components/StudyForm";
import ResultsView from "./components/ResultsView";

export default function App() {
  const [analysis, setAnalysis] = useState<any|null>(null);

  return (
    <div className="max-w-6xl mx-auto p-4 space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">MSA – msa-mefa</h1>
        <div className="text-sm text-gray-500">React + FastAPI</div>
      </header>

      <div className="border rounded-2xl p-4 shadow-sm">
        <h2 className="font-semibold mb-3">Dane wejściowe</h2>
        <StudyForm onAnalyzed={({ result, study, method }) => setAnalysis({ result, study, method })} />
      </div>

      <div className="border rounded-2xl p-4 shadow-sm">
        <h2 className="font-semibold mb-3">Wyniki</h2>
        {analysis ? <ResultsView data={analysis} /> : <p className="text-sm text-gray-600">Wprowadź dane i uruchom analizę.</p>}
      </div>
    </div>
  );
}
