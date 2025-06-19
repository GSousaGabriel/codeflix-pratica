import Image from 'next/image';
import { Movie } from "../types/movie";
import { MovieInfo } from './movieInfo';

const MovieCard = ({ movie }: {movie: Movie}) => {
  return (
    <div className='group relative min-h-[12vh] rounded bg-zinc-900 md:min-h-[12vw]'>
      <Image
        src={movie.bannerFileURL}
        alt={movie.title}
        width={600}
        height={400}
        className='rounded-md object-cover object-top transition'
      />

      <div className='invisible absolute top-0 z-10 w-full min-h-[20vw] scale-0 opacity-0 transition delay-300 duration-200 group-hover:-translate-y-[6vw] group-hover:scale-110 group-hover:opacity-100 sm:visible'>
        <Image
        src={movie.bannerFileURL}
        alt={movie.title}
        width={600}
        height={400}
        className='rounded-md object-cover object-top transition'
      />
      <MovieInfo movie={movie}/>
      </div>
    </div>
  );
};

export default MovieCard;