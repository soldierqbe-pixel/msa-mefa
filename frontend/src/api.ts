import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || window.location.origin;
export const api = axios.create({ baseURL: API_BASE });

export async function createStudy(payload: any) {
  const res = await api.post("/studies", payload);
  return res.data;
}

export async function analyzeStudy(studyId: number, method: "anova"|"range" = "anova") {
  const res = await api.post(`/studies/${studyId}/analyze`, {}, { params: { method } });
  return res.data;
}

export async function listStudies() {
  const res = await api.get("/studies");
  return res.data;
}
