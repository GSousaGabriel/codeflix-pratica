import React from 'react';

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div
      className='h-screen w-screen bg-cover bg-center bg-no-repeat text-white opacity-90'
      style={{ backgroundImage: 'url(/background.jpg' }}
    >
      <div className='flex min-h-screen flex-col items-center justify-center py-2'>
        {children}
      </div>
    </div>
  );
};

export default Layout;
