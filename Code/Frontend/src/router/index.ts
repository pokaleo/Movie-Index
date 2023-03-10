import { before } from "node:test"
import { createRouter, createWebHistory, onBeforeRouteUpdate, RouteRecordRaw } from "vue-router"

const routes: Array<RouteRecordRaw> = [
  {
    path: "/search",
    name: "Results",
    component: () => import(/* webpackChunkName: "Index" */ "@/pages/Index/index.vue"),
    meta: {
      title: "Results",
      keepAlive:true,
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

// create router
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // use import.meta.env.BASE_URL in vite
  routes,
})

/**
 * @description: called when router change
 * @param {*} to 
 * @param {*} from 
 */
router.afterEach((to, from) => {
  // @ts-ignore
  document.title = to.meta.title
})

export default router
