'use client';

import InputField from '../inputFields';

export default function ForgotPasswordForm() {
  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    alert('Forgot password form submitted!');
  };

  return (
    <form
      onSubmit={onSubmit}
      className='flex w-full max-w-md flex-col space-y-4 rounded bg-[#141414]/90 px-4 py-8 shadow-lg'
    >
      <div className='flex flex-col items-center space-y-4'>
        <h1 className='text-3xl'>Forgot password</h1>
        <p className='text-sm text-gray-400'>Enter your email to reset it</p>
      </div>
      <InputField
        type='email'
        id='email'
        placeholder='Enter yor email'
        label='Email'
      />
      <div className='flex flex-col-reverse space-y-2 pt-2 sm:flex-row sm:space-y-0 sm:space-x-2'>
        <button
          type='submit'
          className='flex w-full items-center justify-center space-y-2 rounded-lg bg-red-500 px-4 py-2 text-sm font-semibold hover:bg-red-600 sm:w-auto sm:px-8'
        >
          Submit
        </button>
      </div>
    </form>
  );
}
