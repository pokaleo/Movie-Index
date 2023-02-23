import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"

const routes: Array<RouteRecordRaw> = [
  {
    path: "/search",
    name: "Results",
    component: () => import(/* webpackChunkName: "Index" */ "@/pages/Index/index.vue"),
    meta: {
      title: "Results",
    },
  },
  {
    path: "/detail/:id",
    name: "MovieDetail",
    component: () => import(/* webpackChunkName: "MovieDetail" */ "@/pages/MovieDetail/index.vue"),
    meta: {
      title: "Detail",
    },
  },
  {
    path: "/",
    name: "Start",
    component: () => import(/* webpackChunkName: "MovieDetail" */ "@/pages/MovieDetail/LoadingView.vue"),
    meta: {
      title: "Start",
    },
  },
]

// 创建路由
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // vite中使用 import.meta.env.BASE_URL
  routes,
})

/**
 * @description: 全局后置路由守卫————初始化的时候被调用、每次路由切换之后被调用
 * @param {*} to 进入到哪个路由去
 * @param {*} from 从哪个路由离开
 */
router.afterEach((to, from) => {
  // @ts-ignore
  document.title = to.meta.title
})

// 暴露路由
export default router
