import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    // {
    //   path: '/',
    //   name: 'landing-page',
    //   component: require('@/components/LandingPage').default
    // },
    {
      path: '/',
      name: 'login-page', 
      component: require('@/components/login').default
    },
    {
      path: '/register',
      name: 'register-page',
      component: require('@/components/register').default
    },
    {
      path: '*',
      redirect: '/'
    }  //重定向规则
  ]
})
