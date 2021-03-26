import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '*',
      redirect: '/'
    },
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login-page', 
      component: require('@/components/login').default
    },
    {
      path: '/main_page',
      name: 'main_page',
      component: require('@/components/main_page').default,
      redirect: '/welcome',
      children:[
        {
          path: '/welcome',
          name: 'welcome',
          component: require('@/components/welcome').default
        },
        {
          path: '/welcome2',
          name: 'welcome2',
          component: require('@/components/welcome2').default
        },
        {
          path: '/select-database',
          name: 'select-database',
          component: require('@/components/select-database').default
        }
      ]
    },
    {
      path: '/data_home',
      name: 'data_home',
      component: require('@/components/data_manager/data_home').default,
      children: [
        {
          path: '/display_graphics',
          name: 'display_graphics',
          component: require('@/components/data_manager/display_graphics').default,
          children: [
            {
              path: '/bar',
              name: 'bar',
              component: require('@/components/data_manager/display_table/bar').default
            }
          ]
        }
      ]
    },
    {
      path: '/register',
      name: 'register-page',
      component: require('@/components/register').default
    }
  ]
})

const originalPush = Router.prototype.push
Router.prototype.push = function push (location) {
  return originalPush.call(this, location).catch(err => err)
}
