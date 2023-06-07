export interface SearchResult {
  id: number
  title: string
  year: number
  note_name: string
  judge_prop: string
  case_reason: string
  content: string
}

export interface SearchData {
  code: number
  results: SearchResult[]
  total_objects: number
  time: number
  split_words: string[]
}
