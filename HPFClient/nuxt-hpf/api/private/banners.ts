import $AxiosWrapper from "~/utils/api";
import { IBannerData, IBannerFilters } from "~/types/images";

export const searchBanners = (filters: IBannerFilters | null): Promise<any> => $AxiosWrapper.get<IBannerData>(`/private/images/banners/`, filters);
