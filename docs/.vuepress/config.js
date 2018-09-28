module.exports = {
    title: 'Contest Server Suite',
    description: "For running Fall & Spring Programming Contests",
    base: "/Contest-Server/",
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
