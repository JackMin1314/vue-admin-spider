import router from './router'
// import { Message } from 'element-ui'
import NProgress from 'nprogress' // progress bar
import { getStorageExpire } from './utils/mycookie'
// import { getToken } from '@/utils/auth' // get token from cookie
// import getPageTitle from '@/utils/get-page-title'

// NProgress.configure({ showSpinner: false }) // NProgress Configuration

// const whiteList = ['/login'] // no redirect whitelist

router.beforeEach((to, from, next) => {
  // start progress bar
  NProgress.start()
  // 如果需要验证的话
  if (to.meta.requireAuth) {
      const username = getStorageExpire('username')
      const password = getStorageExpire('password')
    if (username != null && password != null) {
        next()
      NProgress.done()
    } else {
        next(`/login?redirect=${to.path}`)
    }
  } else {
    // 页面不需要验证
      next()
      NProgress.done()
  }
})

router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})
