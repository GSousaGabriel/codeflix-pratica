import Banner from './components/banner';
import Header from './components/header';
import MovieRow from './components/movieRow';
import { getFeaturedMovie, getMoviesbyGenre } from './service/movieService';

export default async function Home() {
  const featuredMovie = await getFeaturedMovie("101")
  const genres = ["Drama", "Action", "Comedy", "Animation"];
  const movies = await Promise.all(genres.map(async (genre)=>{
    const movies = await getMoviesbyGenre(genre, { _limit: 8 })
    return {sectionTitle: genre, movies}
  }));
  
  return (
    <div className='relative h-screen overflow-hidden bg-gradient-to-b lg:h-[140vh]'>
      <Header />
      <main className='scrollbar-hide relative pb-24 pl-4 lg:pl-16'>
        <Banner movie={featuredMovie}/>
        {movies.map(section=> <MovieRow key={section.sectionTitle} sectionTitle={section.sectionTitle} movies={section.movies} />)}
      </main>
    </div>
  );
}
