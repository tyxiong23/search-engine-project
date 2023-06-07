import { SearchResult } from "."

export interface Law {
  id: number
  name: string
}

export interface CaseDetail {
    id: number
    qw_value: string
    head: string
    related_people: string
    judicial_record: string
    basic_info: string
    judgement_process: string
    result: string
    tail: string

    note_name: string
    case_reason: string
    judge_prop: string
    court: string
    year: number
    laws: Law[]
    related_cases: SearchResult[]
  }
