import { Movie, Movies } from '../types/movie';
import { APIRequest, RequestOptions } from './APIRequest';

export const getMovieById = async (id: string): Promise<Movie> => {
  return await APIRequest(`movies/${encodeURIComponent(id)}`);
};

export const getFeaturedMovie = async (id: string): Promise<Movie> => {
  return await APIRequest(`featured/${encodeURIComponent(id)}`);
};

export const getMoviesbyGenre = async (
  genre: string,
  options?: RequestOptions
): Promise<Movies> => {
  return await APIRequest(
    'movies',
    { genres_like: encodeURIComponent(genre) },
    options
  );
};

export const searchMovies = async (
  title: string,
  genre: string,
  options: RequestOptions ={
    _limit: 100
  }
): Promise<Movies> => {
  return await APIRequest(
    'movies',
    {
      genres_like: encodeURIComponent(genre),
      title_like: encodeURIComponent(title),
    },
    options
  );
};
