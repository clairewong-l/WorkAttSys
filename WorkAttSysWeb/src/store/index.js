import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    state:{
        companyName:'',
        hrName:'',
        logo: '',
},

    //JSON.parse(window.sessionStorage.getItem('hrName'))
    getters:{
        companyName:state =>{
            let companyName = state.companyName
            if(!companyName){
                companyName = JSON.parse(window.sessionStorage.getItem('companyName'))
            }
            return companyName
        },
        hrName:state =>{
            let hrName = state.hrName
            if(!hrName){
                hrName = JSON.parse(window.sessionStorage.getItem('hrName'))
            }
            return hrName
        },
        logo:state =>{
            let logo = state.logo
            if(!logo){
                logo = JSON.parse(window.sessionStorage.getItem('logo'))
            }
            return logo
        }
    },
    mutations:{
        setCompanyName: (state,companyName) =>{
            state.companyName = companyName
            window.sessionStorage.setItem('companyName',JSON.stringify(companyName))
        },
        hrName: (state,hrName) =>{
            state.hrName = hrName
            window.sessionStorage.setItem('hrName',JSON.stringify(hrName))
        },
        setLogo: (state,logo) =>{
            state.logo = logo
            window.sessionStorage.setItem('logo',JSON.stringify(logo))
        }
    }
})

export default store