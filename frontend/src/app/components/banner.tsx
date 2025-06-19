'use client';

import Image from 'next/image';
import { InformationCircleIcon, PlayIcon } from '@heroicons/react/24/outline';
import { Movie } from '../types/movie';
import Link from 'next/link';

const Banner = ({ movie }: { movie: Movie }) => {
  return (
    <div className='mb-[10px]'>
      <div className='flex flex-col space-y-2 py-16 md:space-y-4 lg:h-[65vh] lg:justify-end lg:pb-12'>
        <div className='absolute top-0 left-0 -z-10 flex h-[95vh] w-screen flex-col bg-black'>
          <video autoPlay loop muted className='hidden z-20 h-full object-cover opacity-50 transition duration-1000 ease-in-out lg:block'
            poster={movie.bannerFileURL}
            src={movie.videoFileURL} />
          <Image
            src={movie.bannerFileURL}
            alt={movie.title}
            fill={true}
            className='h-[65vh] object-cover object-top opacity-30 filter lg:hidden'
          />
        </div>
        <h1 className='text-2xl font-bold md:text-4xl lg:text-7xl'>
          {movie.title}
        </h1>
        <p className='max-w-xs text-xs text-shadow-md md:max-w-lg md:text-lg lg:max-w-2xl'>
          {movie.description}
        </p>
      </div>
      <div className='flex space-x-3'>
        <Link href={`/watch/${movie.id}`}>
          <button className='flex cursor-pointer items-center gap-x-2 rounded bg-white px-5 py-1.5 font-semibold text-black transition hover:opacity-75 md:px-8 md:py-2.5 md:text-xl'>
            <PlayIcon className='h-6' /> Play
          </button>
        </Link>
        <button className='flex cursor-pointer items-center gap-x-2 rounded bg-gray-600 px-5 py-1.5 font-semibold text-black transition hover:opacity-75 md:px-8 md:py-2.5 md:text-xl'>
          <InformationCircleIcon
            className='h-6'
            onClick={() => {
              throw new Error('daskdajsdaski');
            }}
          />
          More Info
        </button>
      </div>
    </div>
  );
};

export default Banner;
