import Banner from './components/banner';
import Header from './components/header';
import MovieRow from './components/movieRow';

export default function Home() {
  return (
    <div className='relative h-screen overflow-hidden bg-gradient-to-b lg:h-[140vh]'>
      <Header />
      <main className='scrollbar-hide relative pb-24 pl-4 lg:pl-16'>
        <Banner />
        <MovieRow sectionTitle='Trendind Now'/>
        <MovieRow sectionTitle='Top Rated'/>
        <MovieRow sectionTitle='Action Movies'/>
      </main>
    </div>
  );
}
