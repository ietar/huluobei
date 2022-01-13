let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        books: [],
        csrf: '',
    },
    mounted(){
        this.csrf = $('input[name=csrfmiddlewaretoken]').val();
        this.get_books_info();
    },
    methods: {
        get_books_info(){
            axios.get('/api/books/').then(response =>{
                this.books = response.data.data;
                this.books.forEach(book => {
                    book.target = 1;
                })
            }).catch(e =>{console.log(e)});
        },
        get_content(bid, b_target){
            axios.get('/api/crawl/get_content/', {params: {'id': bid, 'target': b_target}})
                .then(response =>{
                    alert(response.data['msg'])
                }).catch(e => {console.log(e)})
        }
    }
});

