import { Exclude } from "class-transformer";
import { BasicClass } from "./basics";

// Motifs d'invalidation
export class InvalidationReasonData extends BasicClass<InvalidationReasonData> {
  @Exclude()
  public get invalidationReasonId(): number {
    return Number(this.id);
  }

  // Libelle du motif d'invalidation
  public reason: string = "Motif par défaut";

  constructor(init?: Partial<InvalidationReasonData>) {
    super();
    Object.assign(this, init);
  }
}
