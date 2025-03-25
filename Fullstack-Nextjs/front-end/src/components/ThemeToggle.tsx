'use client';

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { Moon, Sun } from "lucide-react";

export default function ThemeToggle() {
    const { theme, setTheme } = useTheme();
    const [mounted, setMounted] = useState(false);
  
    // Avoid hydration mismatch
    useEffect(() => {
      setMounted(true);
    }, []);
  
    if (!mounted) return null;
  
    return (
      <button
        onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        className="p-2 rounded-lg bg-gray-200 dark:bg-gray-800 transition"
      >
        {theme === "dark" ? <Sun className="text-yellow-500" /> : <Moon className="text-gray-700" />}
      </button>
    );
  }