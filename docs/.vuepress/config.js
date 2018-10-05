// URLBASE needs to be set for the push to Github Pages, but otherwise
// it can be empty for local, now.sh, or netlify.
const urlBase = process.env.URLBASE || "/";

module.exports = {
    title: 'Contest Server Suite',
    description: "For running Fall & Spring Programming Contests",
    base: urlBase,
    themeConfig: {
        repo: 'fsu-acm/contest-server',
        docsDir: 'docs',
        editLinks: true,
        editLinkText: 'Edit this page on Github',
        nav: [
            { text: 'Home', link: '/' },
            { text: 'Guide', link: '/guide/' },
            { text: 'Contributing', link: '/contributing/' },
        ],
        sidebar: {
            '/guide/': [
                {
                    title: 'Running the Software',
                    collapsable: false,
                    children: [
                        '',
                        'getting_started',
                        'configuration',
                        'deployment',
                    ]
                },
            ],
        }
    }
}
