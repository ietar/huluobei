let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        image_code_url: '',
        uuid: '',
        img_code: '',

        error_img_code: true,
        error_password: true,

        error_img_message: '',

    },
    mounted(){
        this.csrf = $('input[name=csrfmiddlewaretoken]').val();
        this.generate_image_code();
    },
    methods: {
        generate_image_code(){
            this.uuid = guid();
            $('input#uuid').val(this.uuid);
            this.image_code_url = `/image_codes/${this.uuid}/`;
        },
        check_img_code(){
            if (this.img_code.length !== 4){
                this.error_img_message = "请输入图形验证码";
                this.error_img_code = true;
                return false
            }
            else{
                this.error_img_code = false;
            }
            let url = `/api/img_code/?uuid=${this.uuid}`
            axios.get(url)
                .then(response => {
                    if (response.data.result === true){
                        if (response.data.data === this.img_code){
                            this.error_img_code = false;
                        }
                        else{
                            this.error_img_code = true;
                            this.error_img_message = '请输入正确的图形验证码'
                        }
                    }
                    else{
                        this.error_img_code = true;
                        this.error_img_message = '图形验证码过期';
                    }
                }).catch(e => console.log(e))
        },
        check_password(){
            let re = /^[a-zA_Z0-9-_@]{8,20}$/;
            this.error_password = !re.test(this.password);
        },
        forget_password(){
            window.location = '/account/forget_password/';
        },
        on_submit(){
            this.check_img_code();

            if (this.error_password === true){
                // window.event.returnValue = false;
                this.event.preventDefault();
            }
        },

    }
});
