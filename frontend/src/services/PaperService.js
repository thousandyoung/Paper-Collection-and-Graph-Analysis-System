// services/PaperService.js

const API_BASE_URL = 'http://127.0.0.1:8000/search/';

export async function searchPapers(keyword, page = 1, pageSize = 10) {
  const response = await fetch(`${API_BASE_URL}paper_list/?keyword=${encodeURIComponent(keyword)}&page=${page}&page_size=${pageSize}`);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(`Failed to fetch papers: ${data.detail}`);
  }
  return data;
}

export async function getPaper(uid) {
  console.log(`${API_BASE_URL}paper_detail/?uid=${uid}`)
  const response = await fetch(`${API_BASE_URL}paper_detail/?uid=${uid}`);
  const data = await response.json();
  return data;
}
