'use client';

import AuthForm from '@/app/components/authForm';

export default function RegisterForm() {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
  };

  return <AuthForm formType='register' onSubmit={handleSubmit} />;
}
