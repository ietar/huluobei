let app = new Vue({
    el: '#user_info_bar',
    delimiters: ['[[', ']]'],
    data:{
        username: '',
    },
    mounted(){
        let r = get_cookie('username');
        if(r){
            this.username = r;
        }
    }
});

let app2 = new Vue({
    el: '#search_bar',
    delimiters: ['[[', ']]'],
    data:{
        search_place_holder: '',
    },
    mounted(){
        this.get_anything()
    },
    methods:{
        get_anything(){
            axios.get('/api/anything/',{params:{},headers:{'X-CSRFToken': this.csrf}, responseType: 'json'})
            .then(res => {
                this.search_place_holder = res.data.data['search_place_holder'];
                // console.log(res.data);
            }).catch(e => {console.log(e)})
        }
    }
});
