import React from "react";

type Props = {
  numSamples: number; // 10
  numSeries: number; // 3
  operators: string[]; // [op1, op2, op3]
  values: Record<string, string>; // key: `${sample}_${series}_${opIndex}`
  setValues: (updater: (prev: Record<string, string>) => Record<string, string>) => void;
};

export default function MeasurementGrid({ numSamples, numSeries, operators, values, setValues }: Props) {
  const handleChange = (key: string, val: string) => {
    setValues(prev => ({ ...prev, [key]: val }));
  };

  return (
    <div className="overflow-auto border rounded-2xl p-3">
      <table className="min-w-[800px] w-full text-sm">
        <thead>
          <tr>
            <th className="p-2 text-left">No.</th>
            {operators.map((op, oi) => (
              <th key={oi} className="p-2 text-center" colSpan={numSeries}>{op || `Operator ${oi+1}`}</th>
            ))}
          </tr>
          <tr>
            <th></th>
            {operators.map((_, oi) => (
              Array.from({ length: numSeries }).map((__, si) => (
                <th key={`${oi}-${si}`} className="p-1 text-center">{si+1}st</th>
              ))
            ))}
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: numSamples }).map((_, sampleIdx) => (
            <tr key={sampleIdx} className="odd:bg-gray-50">
              <td className="p-2 font-medium">{sampleIdx + 1}</td>
              {operators.map((_, oi) => (
                Array.from({ length: numSeries }).map((__, si) => {
                  const key = `${sampleIdx+1}_${si+1}_${oi+1}`;
                  return (
                    <td key={key} className="p-1">
                      <input
                        value={values[key] ?? ""}
                        onChange={e => handleChange(key, e.target.value)}
                        className="w-full border rounded px-2 py-1 focus:outline-none focus:ring"
                        inputMode="decimal"
                        placeholder=""
                      />
                    </td>
                  );
                })
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
