import { Transform } from "class-transformer";

export enum SortByEnum {
  Ascending = 0,
  Descending = 1,
}

export interface IBasicQuery {
  page: number,
  totalPages: boolean,
  pageSize: number,
  sortOn: string,
  sortBy: SortByEnum
}

export interface BasicResponse {
  currentPage: number,
  totalPages: number,
  pageSize: number
}

export class BasicClass<T> {
  public id: number = 0;
  public creation_user_id: number | null = null;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => (value?.toISOString() ?? ""), { toPlainOnly: true })
  public creation_date: Date | null = null;

  public modification_user_id: number | null = null;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => (value?.toISOString() ?? ""), { toPlainOnly: true })
  public modification_date: Date | null = null;

  constructor(basicClass: T) {
    Object.assign(this, basicClass); // or set each prop individually
  }

  public toJSON (): any {
    return { ...this }; // POJO's copy of the class instance
  }
}
