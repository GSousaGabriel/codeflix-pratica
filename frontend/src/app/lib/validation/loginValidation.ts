import { z } from 'zod';

export const loginFromSchema = z.object({
  email: z.string().email(),
  password: z.string().max(8),
});
