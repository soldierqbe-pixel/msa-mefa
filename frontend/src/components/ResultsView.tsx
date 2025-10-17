import React from "react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

export default function ResultsView({ data }:{ data: any }) {
  if (!data) return null;
  const { result, method } = data;

  const components = result.components || result.range_table || [];
  const summary = result.summary || {};

  const chartData = (components || [])
    .filter((c:any) => c.Component ? ["Repeatability (Equipment)", "Reproducibility – Operator", "GRR (Total)", "Part-to-Part"].includes(c.Component) : ["EV","AV","GRR","PV"].includes(c.Metric))
    .map((c:any) => (c.Component ? ({ name: c.Component, value: Number(c.SD ?? 0) }) : ({ name: c.Metric, value: Number(c.Value ?? 0) })));

  const studyId = data?.study?.id;
  const pdfUrl = `${import.meta.env.VITE_API_BASE || window.location.origin}/studies/${studyId}/report.pdf?method=${method || "anova"}`;

  return (
    <div className="grid md:grid-cols-2 gap-6 mt-6">
      <div className="border rounded-2xl p-4">
        <h3 className="font-semibold mb-3">Podsumowanie</h3>
        <ul className="text-sm space-y-1">
          {Object.entries(summary).map(([k,v]) => (
            <li key={k} className="flex justify-between"><span>{k}</span><span className="font-medium">{String(v)}</span></li>
          ))}
        </ul>
        {studyId && (
          <a href={pdfUrl} target="_blank" className="mt-3 inline-block px-4 py-2 rounded-2xl bg-indigo-600 text-white">Pobierz PDF</a>
        )}
      </div>
      <div className="border rounded-2xl p-4">
        <h3 className="font-semibold mb-3">Wykres</h3>
        <div className="h-64">
          <ResponsiveContainer>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" tick={{fontSize: 12}} interval={0} angle={-10} height={60} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      {result.anova && (
        <div className="md:col-span-2 border rounded-2xl p-4 overflow-auto">
          <h3 className="font-semibold mb-3">ANOVA</h3>
          <table className="text-sm min-w-[700px] w-full">
            <thead>
              <tr>
                {result.anova.length>0 && Object.keys(result.anova[0]).map((h:string) => (
                  <th key={h} className="p-2 text-left">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {result.anova.map((row:any, i:number) => (
                <tr key={i} className="odd:bg-gray-50">
                  {Object.values(row).map((v:any, j:number) => (
                    <td key={j} className="p-2">{typeof v === 'number' ? v.toFixed(6) : String(v)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <div className="md:col-span-2 border rounded-2xl p-4 overflow-auto">
        <h3 className="font-semibold mb-3">Tabela</h3>
        <table className="text-sm min-w-[700px] w-full">
          <thead>
            <tr>
              {components.length>0 && Object.keys(components[0]).map((h:string) => (
                <th key={h} className="p-2 text-left">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {components.map((row:any, i:number) => (
              <tr key={i} className="odd:bg-gray-50">
                {Object.values(row).map((v:any, j:number) => (
                  <td key={j} className="p-2">{typeof v === 'number' ? (isFinite(v) ? v.toFixed(6) : '—') : (v ?? '—') }</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
