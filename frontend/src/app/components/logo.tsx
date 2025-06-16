import Image from 'next/image';

const Logo = () => {
  return (
    <Image
      src='/logo.svg'
      alt='Logo'
      width={90}
      height={90}
      className='cursor-pointer'
    />
  );
};

export default Logo;