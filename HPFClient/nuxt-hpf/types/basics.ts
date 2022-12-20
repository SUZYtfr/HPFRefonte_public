export interface QueryParams {
  page?: number;
  page_size?: number;
}

export interface PaginatedResponse {
  count: number;
  current: number;
  previous?: string;
  next?: string;
  results: any;
}