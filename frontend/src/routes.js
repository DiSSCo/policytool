import Home from '@/views/Home.vue'
import InstitutionHome from '@/views/InstitutionHome.vue'
import NotFound from '@/views/NotFound.vue'
import Login from '@/views/auth/Login.vue'
import Logout from '@/views/auth/Logout.vue'
import RequestAccount from '@/views/auth/RequestAccount.vue'
import ResetPassword from '@/views/auth/ResetPassword.vue'
import Pack from '@/views/Pack.vue'
import MaturityHome from '@/views/maturity/Home.vue'
import ResponderHome from '@/views/maturity/ResponderHome.vue'

/** @type {import('vue-router').RouterOptions['routes']} */
export const routes = [
    {path: '/', component: Home, name: 'home', meta: {title: 'Home'}},
    {
        path: '/policy',
        component: InstitutionHome,
        name: 'policy',
        meta: {title: 'Policy', auth: true}
    },
    {
        path: '/maturity',
        component: MaturityHome,
        name: 'maturity',
        meta: {title: 'Maturity Home', auth: true}
    },
    {
        path: '/maturity/:id',
        component: ResponderHome,
        name: 'maturity_responder_home',
        meta: {title: 'Maturity Home', auth: true},
        props: true
    },
    {
        path: '/pack/:responderId/:type/:id',
        component: Pack,
        name: 'pack',
        meta: {title: 'Question Pack', auth: true},
        props: true
    },
    {path: '/login', component: Login, name: 'login', meta: {title: 'Login'}},
    {path: '/logout', component: Logout, name: 'logout', meta: {title: 'Logout'}},
    {
        path: '/register',
        component: RequestAccount,
        name: 'requestAccount',
        meta: {title: 'Request Account'}
    },
    {
        path: '/reset',
        component: ResetPassword,
        name: 'resetPassword',
        meta: {title: 'Reset Password'}
    },
    {path: '/:path(.*)', component: NotFound, meta: {title: 'Page not found'}},
]
