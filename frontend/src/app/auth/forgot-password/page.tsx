export default function ForgotPassword() {
  return (
    <form className='flex w-full max-w-md flex-col space-y-4 rounded bg-[#141414]/90 px-4 py-8 shadow-lg'>
      <div className='mt-8 flex flex-col space-y-4'>
        <div className='flex flex-col space-y-1'>
          <label
            className='text-sm font-semibold text-gray-500'
            htmlFor='email'
          >
            Email
          </label>
          <input
            className='rounded-lg border-gray-600 bg-gray-700 px-4 py-2 focus:border-transparent focus:ring-2 focus:ring-red-500 focus:outline-none'
            placeholder='Enter yor email'
            type='email'
            name='email'
            id='email'
          />
        </div>
        <div className='flex flex-col space-y-1'>
          <label
            className='text-sm font-semibold text-gray-500'
            htmlFor='password'
          >
            Password
          </label>
          <input
            className='rounded-lg border-gray-600 bg-gray-700 px-4 py-2 focus:border-transparent focus:ring-2 focus:ring-red-500 focus:outline-none'
            placeholder='Enter yor password'
            type='password'
            name='password'
            id='password'
          />
        </div>
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
