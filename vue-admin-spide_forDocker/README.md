# vue-admin-spider
**KEYWORLDS:** 
  Back-end uses the `Python Flask` framework to provide data and *permission verification*, *database backup*, *logging*, *timing tasks* and *email sending* etc. Front-end both focus on *UI and Service* used `Vue`、`Vue router`、`element-ui` 、`axios`, etc.

The project adopts the front-end and back-end separation design pattern. The server is written in the Python flask framework to provide data and permission verification, database backup and timing tasks, etc. The front end is written in vue, introducing element-ui and vue-admin.

### build

> here are some config files you may  edit when you need to modify to build.
>
> * vue.config.js
>
> in module.exports ={}
>
> ```js
> ...
> lintOnSave: process.env.NODE_ENV === 'production',
> ...
> proxy: {
>       '/api': {
>         target: 'http://127.0.0.1:9999/',
>         changeOrigin: true,
>         // pathRewrite: {
>         //   '^/api': '' // 将main.js设置的每次请求头/api拦截，并替换成上面target内容http://127.0.0.1:9999/
>         // }
>       }
>     }
> ```
>
> * src\router\index.js 
>
> in createRouter function
>
> ```js
> const createRouter = () => new Router({
>   mode: 'history', // require service support.
>   scrollBehavior: () => ({
>     y: 0
>   }),
>   routes: constantRoutes
> })
> ```

