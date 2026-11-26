import Vue from "vue";
import Router from "vue-router";
import Home from "@/components/Home";
import About from "@/components/About";
import Approach from "@/components/Approach";
import Careers from "@/components/Careers";
import Vacancy from "@/components/Vacancy";
import Emotion from "@/components/Emotion";
import EmotionRnd from "@/components/EmotionRnd";
import EmotionPost from "@/components/EmotionPost";
import Work from "@/components/Work";
import Showcase from "@/components/Showcase";
import Project from "@/components/Project";
import ProjectInfo from "@/components/ProjectInfo";
import Signup from "@/components/Signup";
import Privacy from "@/components/Privacy";
import Type from "@/components/Type";
import NotFound from "@/components/NotFound";
import { updateMeta } from "@/seo";

Vue.use(Router);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/about",
    name: "About",
    component: About,
  },
  // Approach and Careers (incl. vacancies) are retired for now but may come
  // back. The server sends a temporary 302 to the homepage (public/.htaccess);
  // these cover in-app navigation. To restore, swap each redirect back to its
  // original route:
  //   { path: "/approach", name: "Approach", component: Approach, meta: { title: "Approach - Loaf" } }
  //   { path: "/careers", name: "Careers", component: Careers, meta: { title: "Careers - Loaf" } }
  //   { path: "/careers/:id", name: "Vacancy", component: Vacancy }
  { path: "/approach", redirect: "/" },
  { path: "/careers", redirect: "/" },
  { path: "/careers/:id", redirect: "/" },
  {
    path: "/emotion-lab",
    name: "Emotion",
    component: Emotion,
  },
  {
    path: "/emotion-lab/exploration",
    name: "EmotionRnd",
    component: EmotionRnd,
  },
  {
    path: "/emotion-lab/:id",
    name: "EmotionPost",
    component: EmotionPost,
  },
  {
    path: "/work",
    name: "Work",
    component: Work,
  },
  {
    path: "/work/:id",
    name: "Project",
    component: Project,
  },
  {
    path: "/work/:id/info",
    name: "ProjectInfo",
    component: ProjectInfo,
  },
  {
    path: "/showcase/:id",
    name: "Showcase",
    component: Showcase,
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup,
  },
  {
    path: "/privacy-policy",
    name: "Privacy",
    component: Privacy,
  },
  {
    path: "/type",
    name: "Type",
    component: Type,
  },
  {
    path: "*",
    name: "NotFound",
    component: NotFound,
  },
];

const router = new Router({
  routes,
  mode: "history",
  scrollBehavior(to, from, savedPosition) {
    return { x: 0, y: 0 };
  },
});

// Title, description, canonical, Open Graph and robots for every page come
// from src/seo.js (driven by WordPress settings). main.js runs it again once
// the WordPress data has loaded, since the first navigation happens before.
router.afterEach((to) => {
  updateMeta(to, router.app && router.app.content);
});

export default router;



// WEBPACK FOOTER //
// ./src/router/index.js