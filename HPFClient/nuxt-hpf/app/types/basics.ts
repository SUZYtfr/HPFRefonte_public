import { Transform } from "class-transformer";
import "reflect-metadata";

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

export class BasicClass<T> {
  public id: string = "";
  public recordStatus: RecordStatusEnum = RecordStatusEnum.Unchanged;
  public creationUserId: number | null = null;

  @Transform(
    ({ value }) => {
      return value != null ? new Date(value) : null;
    },
    { toClassOnly: true },
  )
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public creationDate: Date | null = null;

  public modificationUserId: number | null = null;

  @Transform(
    ({ value }) => {
      return value != null ? new Date(value) : null;
    },
    { toClassOnly: true },
  )
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public modificationDate: Date | null = null;

  constructor();

  constructor(basicClass?: T) {
    Object.assign(this, basicClass); // or set each prop individually
  }
  // constructor(basicClass?: Partial<T>) {
  //   Object.assign(this, basicClass); // or set each prop individually
  // }

  public toJSON(): object {
    return { ...this }; // POJO's copy of the class instance
  }
}
