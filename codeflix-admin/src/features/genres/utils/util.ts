import type { Genre } from "../../../types/genre";

export const mapGenreToForm = (genre: Genre) => {
  return {
    id: genre.id,
    name: genre.name,
    categories_id: genre.categories?.map((category) => category.id),
  };
};
