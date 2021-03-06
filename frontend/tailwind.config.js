const defaultTheme = require('tailwindcss/defaultTheme')

/** @type {import("@types/tailwindcss/tailwind-config").TailwindConfig } */
module.exports = {
    content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
    theme: {
        colors: {
            transparent: 'transparent',
            current: 'currentColor',
            blue: {
                DEFAULT: '#0c86c6',
                dark: '#205692',
            },
            yellow: {
                DEFAULT: '#ffd85d',
                dark: '#f8bc2c',
            },
            grey: {
                lighter: '#f4f4f1',
                light: '#e9e8e3',
                DEFAULT: '#d9d9df',
                dark: '#b4b4bf',
                darker: '#868696',
            },
            white: '#ffffff',
            status: {
                new: '#10c1ff',
                handled: '#f7a112',
                approved: '#3dca77',
                denied: '#e74c3c',
                resolved: '#b4b4bf',
            },
            statusDark: {
                new: '#0c86c6',
                handled: '#de9110',
                approved: '#37b66b',
                denied: '#d04436',
                resolved: '#868696',
            }
        },
        extend: {
            fontFamily: {
                sans: [
                    '"Titillium Web"',
                    '"Open Sans"',
                    ...defaultTheme.fontFamily.sans],
            },
            backgroundImage: {
                'home-image': "url('/zdenek-machacek-HYTwWSE5ztw-unsplash.jpg')",
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
