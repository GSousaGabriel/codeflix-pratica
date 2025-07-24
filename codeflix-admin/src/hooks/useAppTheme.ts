import { useEffect, useState } from "react";
import { useLocalStorage } from "./useLocalStorage";
import { darkTheme, lightTheme } from "../config/theme";

export const useAppTheme = () => {
  const [theme, setTheme] = useState(darkTheme);
  const [storedThemeMode, setStoredThemeMode] = useLocalStorage<
    "dark" | "light"
  >("themeMode", "dark");

  const toggleTheme = () => {
    const currentTheme = theme.palette.mode === "dark" ? lightTheme : darkTheme;
    setTheme(currentTheme);
    setStoredThemeMode(currentTheme.palette.mode);
  };

  useEffect(() => {
    const currentTheme = theme.palette.mode === "dark" ? lightTheme : darkTheme;
    if (currentTheme) {
      setTheme(currentTheme);
    }
  }, [storedThemeMode]);

  return [
    theme,
    toggleTheme,
  ] as const;
};
