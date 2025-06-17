'use client';

import { FormEvent } from 'react';
import InputField from '../auth/inputFields';

type AuthFormProps = {
  formType: 'login' | 'register';
  onSubmit: (e: FormEvent<HTMLFormElement>) => void;
};

export default function AuthForm({ formType, onSubmit }: AuthFormProps) {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
  };

  return (
    <form
      onSubmit={handleSubmit}
      className='flex w-full max-w-md flex-col space-y-4 rounded bg-[#141414]/90 px-4 py-8 shadow-lg'
    >
      <div className='flex flex-col items-center space-y-4'>
        <h1 className='text-3xl'>
          {formType === 'login' ? 'Login' : 'Register'}
        </h1>
        <p className='text-sm text-gray-400'>
          {formType === 'login'
            ? 'Alterady have an account?'
            : 'New to the app?'}{' '}
          <a
            href={formType === 'login' ? '/register' : '/login'}
            className='text-red-500 hover:underline'
          >
            {formType === 'login' ? 'Register' : 'Log in'}
          </a>
        </p>
      </div>
      <div className='mt-8 flex flex-col space-y-4'>
        <InputField
          label='Email'
          type='email'
          id='email'
          placeholder='Enter your email'
        />
        <InputField
          id='Password'
          label='Password'
          type='password'
          placeholder='Enter your password'
        />
        {formType === 'register' && (
          <InputField
            id='Password'
            label='Password'
            type='password'
            placeholder='Confirm your password'
          />
        )}
      </div>
      <div className='flex flex-col-reverse space-y-2 pt-2 sm:flex-row sm:space-y-0 sm:space-x-2'>
        <button
          type='submit'
          className='flex w-full items-center justify-center space-y-2 rounded-lg bg-red-500 px-4 py-2 text-sm font-semibold hover:bg-red-600 sm:w-auto sm:px-8'
        >
          {formType === 'login' ? 'Login' : 'Register'}
        </button>
      </div>
    </form>
  );
}
