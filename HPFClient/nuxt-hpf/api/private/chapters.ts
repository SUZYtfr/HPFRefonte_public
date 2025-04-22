/* eslint-disable @typescript-eslint/explicit-function-return-type */

import fetchController from "~/utils/api";
import type { Paginated } from "@/types/basics";
import type { UseFetchOptions } from "nuxt/app";
import { ChapterModel, type BatchChapterFilters } from "~/models";

// TODO Routes à voir avec Pierre
export const getChapters = (
  filters: BatchChapterFilters | null | undefined,
  options?: UseFetchOptions<Paginated<ChapterModel[]>>,
) => fetchController.get<Paginated<ChapterModel[]>>("/private/chapter/todo", filters, ChapterModel, options);
