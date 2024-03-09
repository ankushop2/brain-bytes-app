tailwind.config = {
    darkMode: "class",
};
function toggleTheme() {
    const html = document.documentElement;
    html.classList.toggle("dark");
}
