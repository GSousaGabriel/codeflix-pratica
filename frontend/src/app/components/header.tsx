'use client';
import UserProfile from './userProfile';
import NavLinks from './navLink';
import Logo from './logo';
import useScroll from '../hooks/useScroll';
import SearchForm from './searchForm';
import { useRouter, useSearchParams } from 'next/navigation';
import { ChangeEvent, FormEvent, useState } from 'react';

const Header = () => {
  const isScrolled = useScroll();
  const router = useRouter()
  const params = useSearchParams()
  const initialSearchTerm = params.get('title') || ''
  const [searchTerm, setSearchTerm] = useState<string>(initialSearchTerm)

  const handleSearchParamChange = (event: ChangeEvent<HTMLInputElement>)=>{
     setSearchTerm(event.target.value);
  }

  const handleSearch = (event: FormEvent<HTMLFormElement>) =>{
    event.preventDefault()
    const newParams = new URLSearchParams(params.toString())
    newParams.set('title', searchTerm)
    router.push(`/search?${newParams.toString()}`)
  }

  return (
    <header
      className={`${isScrolled && 'bg-black'} fixed top-0 z-50 flex w-full flex-row items-center justify-between bg-gradient-to-t from-transparent to-black p-2 px-4 transition-all lg:px-16 lg:py-6`}
    >
      <div className='flex items-center space-x-2 md:space-x-4'>
        <Logo />
        <NavLinks />
      </div>
      <SearchForm searchTerm={searchTerm} onSearch={handleSearch} onSearchTermChange={handleSearchParamChange}/>
      <UserProfile />
    </header>
  );
};

export default Header;
