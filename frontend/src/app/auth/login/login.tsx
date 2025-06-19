'use client';
import AuthForm from '@/app/components/authForm';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

type ServerError = {
  message: string;
};

export default function LoginForm() {
  const router = useRouter();
  const [errors, setErrors] = useState<string[]>([]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const formData = new FormData(event.currentTarget);
    const email = formData.get('email');
    const password = formData.get('password');

    try {
      const response = await fetch('/auth/login/api', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (response.ok) {
        router.push('/');
        return;
      }

      const payload: ServerError[] = await response.json();

      setErrors(payload.map((error) => error.message) || []);
      console.log(errors);
    } catch (e) {
      console.error('Login failed:', e);

      setErrors(['An unexpected error occurred. Please try again later.']);
    }
  };

  return <AuthForm formType='login' onSubmit={handleSubmit} />;
}
