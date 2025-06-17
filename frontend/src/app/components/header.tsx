'use client';
import UserProfile from './userProfile';
import NavLinks from './navLink';
import Logo from './logo';
import useScroll from '../hooks/useScroll';

const Header = () => {
  const isScrolled = useScroll();

  return (
    <header
      className={`${isScrolled && 'bg-black'} fixed top-0 z-50 flex w-full flex-row items-center bg-gradient-to-t from-transparent to-black justify-between p-2 px-4 transition-all lg:px-16 lg:py-6`}
    >
      <div className='flex items-center space-x-2 md:space-x-4'>
        <Logo />
        <NavLinks />
      </div>
      <UserProfile />
    </header>
  );
};

export default Header;
