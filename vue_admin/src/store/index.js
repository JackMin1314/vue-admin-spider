import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import user from './modules/user'
// 这里添加为了tagsview
import tagsView from './modules/tagsView'
Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    tagsView,
    user
  },
  getters,

  state: {
    userlistMsg: ''
  },
  mutations: {
    set_userlistMsg(state, data) {
      state.userlistMsg = data;
    }
  }
})

export default store
