import React, { useMemo, useState } from "react";
import MeasurementGrid from "./MeasurementGrid";
import { createStudy, analyzeStudy } from "../api";

export default function StudyForm({ onAnalyzed }: { onAnalyzed: (res: any) => void }) {
  const [date, setDate] = useState<string>(new Date().toISOString().slice(0,10));
  const [partName, setPartName] = useState("");
  const [caliper, setCaliper] = useState("");
  const [nominal, setNominal] = useState<string>("");
  const [lsl, setLsl] = useState<string>("");
  const [usl, setUsl] = useState<string>("");
  const [lead, setLead] = useState("");
  const [op1, setOp1] = useState("");
  const [op2, setOp2] = useState("");
  const [op3, setOp3] = useState("");

  const numSamples = 10;
  const numSeries = 3;
  const operators = useMemo(() => [op1, op2, op3], [op1, op2, op3]);

  const [grid, setGrid] = useState<Record<string, string>>({});
  const [busy, setBusy] = useState(false);
  const [method, setMethod] = useState<"anova"|"range">("anova");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    try {
      const measurements: Array<{ sample_index:number; series_index:number; operator_name:string; value:number; }> = [];
      for (let s=1; s<=numSamples; s++) {
        for (let o=1; o<=operators.length; o++) {
          for (let r=1; r<=numSeries; r++) {
            const key = `${s}_${r}_${o}`;
            const v = grid[key];
            if (v !== undefined && v !== "") {
              measurements.push({ sample_index:s, series_index:r, operator_name: operators[o-1] || `Operator ${o}`, value: Number(v) });
            }
          }
        }
      }

      const payload = {
        date,
        part_name: partName,
        caliper_number: caliper,
        nominal_value: Number(nominal),
        lsl: lsl === "" ? null : Number(lsl),
        usl: usl === "" ? null : Number(usl),
        test_lead: lead,
        operator_a: operators[0] || "Operator 1",
        operator_b: operators[1] || "Operator 2",
        operator_c: operators[2] || "Operator 3",
        num_samples: numSamples,
        num_series: numSeries,
        measurements,
      };

      const study = await createStudy(payload as any);
      const result = await analyzeStudy((study as any).id, method);
      onAnalyzed({ study, result, method });
    } catch (err:any) {
      alert(err?.response?.data?.detail || err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid md:grid-cols-3 gap-3">
        <div>
          <label className="block text-sm mb-1">Data</label>
          <input type="date" className="w-full border rounded px-2 py-1" value={date} onChange={e=>setDate(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">Nazwa części</label>
          <input className="w-full border rounded px-2 py-1" value={partName} onChange={e=>setPartName(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">Numer suwmiarki</label>
          <input className="w-full border rounded px-2 py-1" value={caliper} onChange={e=>setCaliper(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">Wartość nominalna</label>
          <input inputMode="decimal" className="w-full border rounded px-2 py-1" value={nominal} onChange={e=>setNominal(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">Tolerancja dolna (LSL)</label>
          <input inputMode="decimal" className="w-full border rounded px-2 py-1" value={lsl} onChange={e=>setLsl(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">Tolerancja górna (USL)</label>
          <input inputMode="decimal" className="w-full border rounded px-2 py-1" value={usl} onChange={e=>setUsl(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">Lider testu</label>
          <input className="w-full border rounded px-2 py-1" value={lead} onChange={e=>setLead(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">Operator 1</label>
          <input className="w-full border rounded px-2 py-1" value={op1} onChange={e=>setOp1(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">Operator 2</label>
          <input className="w-full border rounded px-2 py-1" value={op2} onChange={e=>setOp2(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">Operator 3</label>
          <input className="w-full border rounded px-2 py-1" value={op3} onChange={e=>setOp3(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">Metoda</label>
          <select className="w-full border rounded px-2 py-1" value={method} onChange={e=>setMethod(e.target.value as any)}>
            <option value="anova">ANOVA</option>
            <option value="range">Average & Range</option>
          </select>
        </div>
      </div>

      <MeasurementGrid
        numSamples={numSamples}
        numSeries={numSeries}
        operators={[op1||"Operator 1", op2||"Operator 2", op3||"Operator 3"]}
        values={grid}
        setValues={setGrid}
      />

      <div className="flex gap-3">
        <button disabled={busy} className="px-4 py-2 rounded-2xl bg-blue-600 text-white shadow">
          {busy ? "Liczenie…" : "Zapisz i analizuj"}
        </button>
      </div>
    </form>
  );
}
