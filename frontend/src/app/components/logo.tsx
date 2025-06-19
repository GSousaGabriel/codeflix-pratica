import Image from 'next/image';
import Link from 'next/link';

const Logo = () => {
  return (
    <Link href="/">
    <Image
      src='/logo.svg'
      alt='Logo'
      width={90}
      height={90}
      className='cursor-pointer'
    />
    </Link>
  );
};

export default Logo;
