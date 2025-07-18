import type { Video, VideoPayload } from "../../../types/videos";

export const mapVideoToForm = (video: Video): VideoPayload => {
  return {
    id: video.id,
    title: video.title,
    rating: video.rating,
    opened: video.opened,
    duration: video.duration,
    description: video.description,
    year_launched: video.year_launched,
    categories_id: video.categories?.map((category) => category.id),
    genres_id: video.genres?.map((genre) => genre.id),
    cast_members_id: video.cast_members?.map((cast) => cast.id),
  };
};
