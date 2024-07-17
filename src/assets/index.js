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
    if (theme === 'auto') {
    document.documentElement.setAttribute('data-bs-theme', (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'))
    } else {
    document.documentElement.setAttribute('data-bs-theme', theme)
    }
}

setTheme(getPreferredTheme())

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