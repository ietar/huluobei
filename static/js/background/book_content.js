let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        book_contents: [],
        csrf: '',
        page_num: 1,
        total_pages: '',
        page_size: 15,

    },
    mounted(){
        this.csrf = $('input[name=csrfmiddlewaretoken]').val();
        this.get_book_content_info();
    },
    methods: {
        get_book_content_info(page=this.page_num){
            axios.get('/api/book_content/', {params: {'pagesize': this.page_size, 'page': page}}).then(response =>{
                this.book_contents = response.data['lists'];
                this.total_pages = response.data['pages'];
                this.page_num = response.data['page'];
            }).catch(e =>{console.log(e)});
        },
        to_page(page){
            if (page < 1 || page > this.total_pages){return false}
            this.get_book_content_info(page);
        },
        change_page_size(size){
            this.page_size = size;
            this.get_book_content_info();
        }
    },
    watch:{
        // 分页器
        total_pages:function(){
            this.$nextTick(e => {
                $('.page').removeClass('choosing');
                $(`#page_num_${this.page_num}`).addClass('choosing');
            });
        },
        page_num:function(){
            this.$nextTick(e => {
                $('.page').removeClass('choosing');
                $(`#page_num_${this.page_num}`).addClass('choosing');
            });
        },
    }
});

