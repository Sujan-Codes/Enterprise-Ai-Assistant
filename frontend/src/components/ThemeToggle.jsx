import { useEffect, useState } from "react";

function ThemeToggle() {
  const [theme, setTheme] = useState(localStorage.getItem("theme") || "system");

  useEffect(() => {
    const root = document.documentElement;

    const applyTheme = () => {
      root.classList.remove("light", "dark");
      if (theme === "system") {
        root.classList.add(window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      } else {
        root.classList.add(theme);
      }
    };

    applyTheme();
    localStorage.setItem("theme", theme);

    if (theme === "system") {
      const mq = window.matchMedia("(prefers-color-scheme: dark)");
      mq.addEventListener("change", applyTheme);
      return () => mq.removeEventListener("change", applyTheme);
    }
  }, [theme]);

  return (
    <div className="theme-toggle">
      <span>Theme</span>
      <select value={theme} onChange={(e) => setTheme(e.target.value)}>
        <option value="system">System</option>
        <option value="light">Light</option>
        <option value="dark">Dark</option>
      </select>
    </div>
  );
}

export default ThemeToggle;
