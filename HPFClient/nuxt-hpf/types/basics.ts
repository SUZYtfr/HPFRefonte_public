import { Transform } from "class-transformer";

export enum SortByEnum {
  Ascending = 0,
  Descending = 1,
}

export enum RecordStatusEnum {
  Unchanged = 1,
  Added = 2,
  Updated = 3,
  Deleted = 4,
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

export interface Paginated<T> {
  count: number;
  current: number;
  results: T;
}

// T | T[] => T
export type Flatten<T> = T extends any[] ? T[number] : T;

// T | T["results"] => T
export type Depaginate<T> = T extends Paginated<any> ? T["results"] : T;


export class BasicClass<T> {
  public id: number = 0;
  public recordStatus: RecordStatusEnum = RecordStatusEnum.Unchanged;
  public creation_user_id: number | null = null;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public creation_date: Date | null = null;

  public modification_user_id: number | null = null;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public modification_date: Date | null = null;

  constructor()

  constructor(basicClass?: T) {
    Object.assign(this, basicClass); // or set each prop individually
  }
  // constructor(basicClass?: Partial<T>) {
  //   Object.assign(this, basicClass); // or set each prop individually
  // }

  public toJSON(): any {
    return { ...this }; // POJO's copy of the class instance
  }
}
