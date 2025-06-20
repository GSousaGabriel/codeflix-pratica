import { Movies } from '../types/movie';
import MovieCard from './movieCard';

type MovieRowProps = {
  sectionTitle: string;
  movies: Movies
};

const MovieRow = ({ sectionTitle, movies }: MovieRowProps) => {
  return (
    <div className='flex-col space-y-4 pl-2'>
      <div className='flex'>
        <h2 className='inline-text -ml-2 items-center text-2xl font-bold'>
          {sectionTitle}
        </h2>
      </div>
      <div className='grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-8'>
        {movies.map((movie) => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </div>
    </div>
  );
};

export default MovieRow;
