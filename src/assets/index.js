(() => {
'use strict'

const getStoredTheme = () => localStorage.getItem('theme')
const setStoredTheme = theme => localStorage.setItem('theme', theme)

const getPreferredTheme = () => {
    const storedTheme = getStoredTheme()
    if (storedTheme) {
    return storedTheme
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

const setTheme = theme => {
    document.documentElement.setAttribute('data-bs-theme', theme);

    let opposite = (theme == 'dark') ? 'light' : 'dark';
    $("#themeSwitch").addClass('btn-' + opposite).removeClass('btn-' + theme);
    let icon = (theme == 'dark') ? 'sun' : 'moon';
    let oppositeIcon = (theme == 'dark') ? 'moon' : 'sun';
    $("#themeSwitch > i").addClass('bi-' + icon).removeClass('bi-' + oppositeIcon)
}

window.addEventListener('DOMContentLoaded', () => {
    setTheme(getPreferredTheme())
});

document.getElementById("themeSwitch").addEventListener("click", () => {
    if (document.documentElement.getAttribute('data-bs-theme') == 'dark') {
        setTheme("light")
        setStoredTheme("light")
    }
    else {
        setTheme("dark")
        setStoredTheme("dark")
    }
});

})();