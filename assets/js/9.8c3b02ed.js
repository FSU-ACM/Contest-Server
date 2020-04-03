(window.webpackJsonp=window.webpackJsonp||[]).push([[9],{167:function(e,t,n){"use strict";n.r(t);var s=n(0),r=Object(s.a)({},function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"content"},[e._m(0),e._v(" "),n("p",[e._v("This section will explain how to set up the project on your machine for development/testing.")]),e._v(" "),e._m(1),e._v(" "),n("p",[e._v("This project relies heavily on "),n("a",{attrs:{href:"https://docs.docker.com/",target:"_blank",rel:"noopener noreferrer"}},[e._v("Docker"),n("OutboundLink")],1),e._v(" and "),n("a",{attrs:{href:"https://docs.docker.com/compose/",target:"_blank",rel:"noopener noreferrer"}},[e._v("Docker Compose"),n("OutboundLink")],1),e._v(". While not "),n("em",[e._v("strictly required")]),e._v(" for development, it is "),n("em",[e._v("highly recommended")]),e._v(".")]),e._v(" "),n("p",[e._v("The registration webapp uses "),n("a",{attrs:{href:"https://www.mongodb.com/",target:"_blank",rel:"noopener noreferrer"}},[e._v("MongoDB"),n("OutboundLink")],1),e._v(" as the database. You can either "),n("a",{attrs:{href:"https://docs.mongodb.com/manual/installation/",target:"_blank",rel:"noopener noreferrer"}},[e._v("install MongoDB"),n("OutboundLink")],1),e._v(" on your host machine or deploy a MongoDB container inside Docker using this project's Docker Compose config.")]),e._v(" "),n("p",[e._v("This project also has some dependency on "),n("a",{attrs:{href:"https://nodejs.org/en/",target:"_blank",rel:"noopener noreferrer"}},[e._v("Node.js"),n("OutboundLink")],1),e._v(", "),n("a",{attrs:{href:"https://www.npmjs.com/",target:"_blank",rel:"noopener noreferrer"}},[e._v("npm"),n("OutboundLink")],1),e._v(", "),n("a",{attrs:{href:"https://gulpjs.com/",target:"_blank",rel:"noopener noreferrer"}},[e._v("Gulp"),n("OutboundLink")],1),e._v(", and "),n("a",{attrs:{href:"http://sass-lang.com/",target:"_blank",rel:"noopener noreferrer"}},[e._v("Sass"),n("OutboundLink")],1),e._v(" for managing/building styles. Currently the project includes pre-built stylesheets, but if you wish to recomplile them you will need these dependencies.")]),e._v(" "),e._m(2),e._v(" "),e._m(3),e._v(" "),e._m(4),e._v(" "),n("p",[e._v("To manage the dependencies of the webapp, we "),n("em",[e._v("strongly recommend")]),e._v(" using a "),n("a",{attrs:{href:"https://virtualenv.pypa.io/en/stable/",target:"_blank",rel:"noopener noreferrer"}},[e._v("virtualenv"),n("OutboundLink")],1),e._v(". You may also be interested in "),n("a",{attrs:{href:"https://virtualenvwrapper.readthedocs.io/",target:"_blank",rel:"noopener noreferrer"}},[e._v("virtualenvwrapper"),n("OutboundLink")],1),e._v(".")]),e._v(" "),n("p",[e._v("Install Python the requirements:")]),e._v(" "),e._m(5),e._m(6),e._v(" "),e._m(7),e._v(" "),e._m(8),e._m(9),e._v(" "),e._m(10),e._v(" "),n("p",[e._v("Once everything is installed, make sure your MongoDB instance is running. Here's out to launch the Dockerized MongoDB instance:")]),e._v(" "),e._m(11),e._m(12),e._v(" "),n("p",[e._v("Specify config and launch in one line:")]),e._v(" "),e._m(13),n("div",{staticClass:"tip custom-block"},[n("p",{staticClass:"custom-block-title"},[e._v("TIP")]),e._v(" "),n("p",[e._v("Be sure your config is right before launching. You can the config docs "),n("router-link",{attrs:{to:"/guide/configuration.html"}},[e._v("here")]),e._v(".")],1)]),e._v(" "),e._m(14),e._v(" "),n("p",[e._v("Before making changes, be sure to read our "),n("router-link",{attrs:{to:"/contributing/"}},[e._v("Contributing Guidelines")]),e._v(" to make sure your changes stay within our recommended practices.")],1)])},[function(){var e=this.$createElement,t=this._self._c||e;return t("h1",{attrs:{id:"getting-started"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#getting-started","aria-hidden":"true"}},[this._v("#")]),this._v(" Getting Started")])},function(){var e=this.$createElement,t=this._self._c||e;return t("h2",{attrs:{id:"prerequisites"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#prerequisites","aria-hidden":"true"}},[this._v("#")]),this._v(" Prerequisites")])},function(){var e=this.$createElement,t=this._self._c||e;return t("h2",{attrs:{id:"installation"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#installation","aria-hidden":"true"}},[this._v("#")]),this._v(" Installation")])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"tip custom-block"},[t("p",{staticClass:"custom-block-title"},[this._v("TIP")]),this._v(" "),t("p",[this._v("If you choose to install the webapp on your host system, follow these steps to setup the webapp. If using Docker for webapp development, you can skip this.")])])},function(){var e=this.$createElement,t=this._self._c||e;return t("h4",{attrs:{id:"python-dependencies"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#python-dependencies","aria-hidden":"true"}},[this._v("#")]),this._v(" Python Dependencies")])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"language-bash extra-class"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[this._v("pip "),t("span",{attrs:{class:"token function"}},[this._v("install")]),this._v(" -r requirements.txt\n")])])])},function(){var e=this.$createElement,t=this._self._c||e;return t("h4",{attrs:{id:"node-js-dependencies"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#node-js-dependencies","aria-hidden":"true"}},[this._v("#")]),this._v(" Node.js Dependencies")])},function(){var e=this.$createElement,t=this._self._c||e;return t("p",[this._v("For building the Sass, install the dependencies from "),t("code",[this._v("package.json")]),this._v(":")])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"language-bash extra-class"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[t("span",{attrs:{class:"token function"}},[this._v("npm")]),this._v(" "),t("span",{attrs:{class:"token function"}},[this._v("install")]),this._v("\n")])])])},function(){var e=this.$createElement,t=this._self._c||e;return t("h2",{attrs:{id:"running-the-webapp"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#running-the-webapp","aria-hidden":"true"}},[this._v("#")]),this._v(" Running the webapp")])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"tip custom-block"},[t("p",{staticClass:"custom-block-title"},[this._v("TIP")]),this._v(" "),t("p",[this._v("This section is for running the webapp on your host system (not using Docker)")])])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"language-bash extra-class"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[this._v("docker-compose up -d db\n")])])])},function(){var e=this.$createElement,t=this._self._c||e;return t("p",[this._v("You must specify a config via environmental variable to launch the server. The config path is relative to the main "),t("code",[this._v("__init__.py")]),this._v(".")])},function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"language-bash extra-class"},[n("pre",{pre:!0,attrs:{class:"language-bash"}},[n("code",[e._v("FLASK_CONFIG"),n("span",{attrs:{class:"token operator"}},[e._v("=")]),n("span",{attrs:{class:"token punctuation"}},[e._v("..")]),e._v("/config/development.py python start.py\n\n"),n("span",{attrs:{class:"token comment"}},[e._v("# Alternatively, use the npm script")]),e._v("\n"),n("span",{attrs:{class:"token function"}},[e._v("npm")]),e._v(" run dev\n")])])])},function(){var e=this.$createElement,t=this._self._c||e;return t("h2",{attrs:{id:"contributing"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#contributing","aria-hidden":"true"}},[this._v("#")]),this._v(" Contributing")])}],!1,null,null,null);r.options.__file="getting_started.md";t.default=r.exports}}]);