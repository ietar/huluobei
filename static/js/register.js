function timerInt(interval){
    let send_button = $("span.send_sms_code");
    send_button.text(`重新发送: (${interval})`);
    let timer = setInterval(function(){
        interval--;
        if(interval < 0){
            interval = 0;
            clearInterval(timer);
            send_button.text("发送短信验证码").css("pointer-events", 'auto');
            return 1
        }
        else{
            send_button.text(`重新发送: (${interval})`).css("pointer-events", 'none');
        }
    },1000);
}

let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        username: '',
        password: '',
        password2: '',
        email: '',
        allow: '',
        image_code_url: '',
        uuid: '',
        img_code: '',
        csrf: '',

        error_name: false,
        error_password: false,
        error_password2: false,
        error_email: false,
        error_allow: true,
        error_img_code: false,
        error_sms_code: false,

        error_name_message: '',
        error_email_message: '',
        error_img_message: '',
        error_sms_code_message: '请输入短信验证码',

    },
    mounted(){
        this.generate_image_code();
        this.csrf = $('input[name=csrfmiddlewaretoken]').val();
    },
    methods: {
        generate_image_code(){
            this.uuid = guid();
            $('#uuid').val(this.uuid);
            this.image_code_url = `/image_codes/${this.uuid}/`;
        },
        check_username() {
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)){
                this.error_name = false;
            }
            else{
                this.error_name = true;
                this.error_name_message = '请输入5-20个字符的用户名';
            }
            if (!this.error_name){
                let url = `/api/user_exist/`;
                axios.get(url, {responseType: 'json', params: {'username': this.username}})
                    .then(response => {
                        if (response.data['result'] !== true){
                            this.error_name_message = response.data['msg'];
                            this.error_name = true;
                            console.log(this.error_name_message);
                        }
                        else{
                            this.error_name = false;

                        }
                    })
                    .catch(error => {
                        console.log(error);
                    })
            }
        },
        check_password(){
            let re = /^[a-zA_Z0-9-_@]{8,20}$/;
            this.error_password = !re.test(this.password);

        },
        check_password2(){
            this.error_password2 = Boolean(this.password !== this.password2);
        },
        check_email(){
            // let re = /^1[3-9]\d{9}$/;
            let re = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            if (re.test(this.email)){
                this.error_email = false;
                return true
            }
            else{
                this.error_email = true;
                this.error_email_message = '请输入正确的邮箱';
                return false
            }
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
            let url = `/api_v1/img_code/?uuid=${this.uuid}`
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
        check_allow(){
            this.error_allow = !this.allow;
        },
        send_sms_code(){
            if (this.error_mobile){
                this.error_sms_code = true;
                this.error_sms_code_message = '请先输入正确的11位手机号';
                return false
            }
            if (this.error_img_code){
                this.error_sms_code = true;
                this.error_sms_code_message = '请先输入正确的图形验证码';
                return false
            }
            let url = `/api/sms_code/`;
            axios({
                url: url,
                method: 'post',
                // data: JSON.stringify({'uuid': self.uuid, 'mobile': self.mobile}),
                data: {'uuid': this.uuid, 'mobile': this.mobile},
                headers: {
                    'Content-Type':'application/json',
                    // 'Content-Type':'application/x-www-form-urlencoded',
                    // 'X-CSRFToken': window.sessionStorage.getItem("csrf_token")
                    'X-CSRFToken': this.csrf,
                }})
                .then(response => {
                    if (response.data.result === true){
                        this.error_sms_code_message = '短信验证码发送成功';
                        $('#sms_code_error_status_code_rel').hide();
                        timerInt(60);
                    }
                    else{
                        this.error_sms_code = true;
                        this.error_sms_code_message = response.data.msg;
                        $('#sms_code_error_status_code_rel').show();
                    }
                }).catch(e => this.error_sms_code_message=e);
        },
        on_submit(e){
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_email();
            this.check_img_code();
            this.check_allow();

            if (this.error_name || this.error_password || this.error_password2 || this.error_email || this.error_allow || this.error_img_code || this.error_sms_code)
            {
                e.preventDefault();
            }
        },

    }
});

