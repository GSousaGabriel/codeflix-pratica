import { configDefaults, defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

const excludeFiles = [
  "**/public/**",
  "**/node_modules/**",
  "**/dist/**",
  "**/html/**",
  "**/docker/**",
  "**/src/main.tsx",
  "**/src/App.tsx",
  "**/hooks/**",
  "**/types/**",
  "**/interfaces/**",
  "**/schema.tsx",
  "**/assets",
  "vite.config.ts",
  "vitest.config.ts",
];

export default defineConfig({
  plugins: [react()],
  test: {
    ...configDefaults,
    environment: "jsdom",
    globals: true,
    css: true,
    reporters: ["html"],
    exclude: excludeFiles,
    coverage: {
      exclude: [
        ...excludeFiles,
        "**/tests/**",
        "**/*.test.tsx",
        "**/*.test.ts",
      ],
      enabled: true,
    },
    server: {
      deps: {
        inline: ["@mui/x-data-grid"],
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
