document.addEventListener('DOMContentLoaded', () => {
    const themeToggleButton = document.getElementById('theme-toggle-btn');
    const themeIcon = document.getElementById('theme-icon');
    
    // Check local store for theme caching preference
    const activeTheme = localStorage.getItem('study-companion-theme') || 'dark';
    applyTheme(activeTheme);

    themeToggleButton.addEventListener('click', () => {
        const targetTheme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
        applyTheme(targetTheme);
    });

    function applyTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.remove('light-theme');
            document.body.classList.add('dark-theme');
            if(themeIcon) {
                themeIcon.classList.remove('bi-moon-fill');
                themeIcon.classList.add('bi-sun-fill');
            }
            localStorage.setItem('study-companion-theme', 'dark');
        } else {
            document.body.classList.remove('dark-theme');
            document.body.classList.add('light-theme');
            if(themeIcon) {
                themeIcon.classList.remove('bi-sun-fill');
                themeIcon.classList.add('bi-moon-fill');
            }
            localStorage.setItem('study-companion-theme', 'light');
        }
    }
});