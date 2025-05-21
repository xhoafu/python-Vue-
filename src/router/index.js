import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: "/",
    name: "homepage",
    component : () => import("@/views/Homepage/home.vue"),
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('@/views/Home/index.vue'),
        children: [
        {   path: "",
          name: "last",
          component: () => import("@/views/Home/homepage.vue")
        },
        {
          path: "/author",
          name: "author",
          component: () => import("@/views/Author/author.vue")
        },
        {
          path: "/playlist",
          name: "platlist",
          component: () => import("@/views/Playlist/playlist.vue")
        },
        {
          path: "/ranking",
          name: "ranking",
          component: () => import("@/views/Ranking/ranking.vue")
        },
        ],
      },
      {
        path: '/mine',
        name: 'mine',
        component: () => import('@/views/Mine/mine.vue')
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import("@/views/login/login.vue"),
  },
  {
    path: '/register',
    name: 'logout',
    component: () => import("@/views/logout/logout.vue")
  },
  {
    path: '/playlist/:playlistId',
    name: 'playlistDetail',
    component: () => import("@/views/Playlist/PlaylistDetailView.vue"),
  },
  {
    path: '/author/:id',
    name: 'authorDeta',
    component: () => import("@/views/Author/authorDeta.vue")
  },
  {
    path: '/player/:id',
    name: 'player',
    component: () => import("@/components/player.vue")
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import("@/views/Search/Search.vue")
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
