import Image from 'next/image';
import Header from './components/header';

export default function Home() {
  return (
    <div className='relative h-screen overflow-hidden bg-gradient-to-b lg:h-[140vh]'>
      <Header />
      <main className='relative pb-24 pl-4 lg:pl-16'>
        <div className='flex flex-col space-y-2 py-16 md:space-y-4 lg:h-[65vh] lg:justify-end lg:pb-12'>
          <div className='absolute top-0 left-0 -z-10 flex h-[95vh] w-screen flex-col bg-black'></div>
          <Image
            src='/banner.png'
            alt='Maid'
            fill={true}
            className='h-[65vh] object-cover object-top lg:h-[95vh]'
          />
          <h1 className='text-2xl font-bold md:text-4xl lg:text-7xl'>
            The Witcher
          </h1>
          <p className='max-w-xs text-xs text-shadow-md md:max-w-lg md:text-lg lg:max-w-2xl'>
            Geralt of Rivia, a brooding professional monster hunter for hire
            also known as witcher, struggles to keep his humanity in a medieval
            dark fantasy world ruled by corrupt kings, queens and mages
          </p>
          <div className='flex space-x-3'>
            <button className='flex cursor-pointer items-center gap-x-2 rounded bg-white px-5 py-1.5 font-semibold text-black transition hover:opacity-75 md:px-8 md:py-2.5 md:text-xl'>
              Play
            </button>
            <button className='flex cursor-pointer items-center gap-x-2 rounded bg-gray-600 px-5 py-1.5 font-semibold text-black transition hover:opacity-75 md:px-8 md:py-2.5 md:text-xl'>
              More Info
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
