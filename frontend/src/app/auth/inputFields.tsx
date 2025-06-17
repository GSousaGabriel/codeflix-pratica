type InputFieldProps = {
  id: string;
  label: string;
  type: string;
  placeholder: string;
};

const InputField = ({ id, label, type, placeholder }: InputFieldProps) => (
  <div className='flex flex-col space-y-1'>
    <label className='text-sm font-semibold text-gray-500' htmlFor={id}>
      {label}
    </label>
    <input
      className='rounded-lg border-gray-600 bg-gray-700 px-4 py-2 focus:border-transparent focus:ring-2 focus:ring-red-500 focus:outline-none'
      placeholder={placeholder}
      type={type}
      name={id}
      id={id}
    />
  </div>
);

export default InputField;
