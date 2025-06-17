'use client'
import InputField from "../inputFields";

export default function LoginForm() {
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
    }

  return (
    <form onSubmit={handleSubmit} className='flex w-full max-w-md flex-col space-y-4 rounded bg-[#141414]/90 px-4 py-8 shadow-lg'>
      <div className='flex flex-col items-center space-y-4'>
        <h1 className='text-3xl'>Login</h1>
        <p className='text-sm text-gray-400'>
          New to the app?{' '}
          <a href='#' className='text-red-500 hover:underline'>
            Register
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
      </div>
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
