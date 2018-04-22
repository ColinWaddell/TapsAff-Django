
Vue.config.delimiters = ['[[', ']]'];

var map = new Vue({
    el: '#map',
    data: {
        show_clothing: true
    },
    methods: {
        hey: function(){
            console.log("he")
        },
        hey2: function(){
            console.log("he22")
        }
    }
});