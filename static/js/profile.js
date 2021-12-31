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
        mobile: '',
        email: '',
        last_login: '',
        login_ip: '',
        csrf: '',
        email_msg: '',
        mobile_msg: '',
        all_history: '',

        show_email_msg: false,
        show_mobile_msg: false,

    },
    mounted(){
        this.csrf = $('input[name=csrfmiddlewaretoken]').val();
        this.get_user_info();
        // this.get_history();
    },
    methods: {
        delete_history(sku_id, index){
            axios.delete('/api/browse_history/',{data: {'sku_id': sku_id}, headers: {'X-CSRFToken': this.csrf}, responseType: 'json'})
              .then(res => {
                  this.all_history.splice(index, 1);
              }).catch(e => console.log(e))
        },
        // get_history(){
        //   axios.get('/api/browse_history/', {params:{'full': 1}, headers: {'X-CSRFToken': this.csrf}, responseType: 'json'})
        //       .then(res => {this.all_history = res.data.data}).catch(e => console.log(e))
        // },
        get_user_info(){
            axios.get('/api/user/').then(response =>{
                let user_info = response.data.data;
                this.username = user_info.username;
                // this.mobile = user_info.mobile;
                this.email = user_info.email;
                this.login_ip = int2ip(user_info.login_ip);
                this.last_login = user_info.last_login;
            }).catch(e =>{console.log(e)});
        },
        edit_email(){
            $('#email').attr('disabled', false);
        },
        save_email(){
            $('#email').attr('disabled', true);
            let url = '/api/email/';
            axios.put(url, {email:this.email}, {headers: {'X-CSRFToken': this.csrf}, responseType: 'json'})
                .then(response => {
                    if(response.data.result === true){
                        this.email_msg = '修改邮箱成功';
                        this.show_email_msg = true;
                        $('#email_msg').removeClass('error_tip').addClass('error_free_tip')
                    }
                    else{
                        console.log('false', response.data);
                        this.email_msg = response.data.msg;
                        this.show_email_msg = true;
                        $('#email_msg').removeClass('error_free_tip').addClass('error_tip')
                    }
                })
                .catch(e =>{
                console.log(e)
            })
        },
        edit_mobile(){
            $('#mobile').attr('disabled', false);
        },
        save_mobile(){
            $('#mobile').attr('disabled', true);
            let url = '/api/mobile/';
            axios.put(url, {mobile:this.mobile}, {headers: {'X-CSRFToken': this.csrf}, responseType: 'json'})
                .then(response => {
                    if(response.data.result === true){
                        this.mobile_msg = '修改手机号成功';
                        this.show_mobile_msg = true;
                        $('#mobile_msg').removeClass('error_tip').addClass('error_free_tip')
                    }
                    else{
                        this.mobile_msg = response.data.msg;
                        this.show_mobile_msg = true;
                        $('#mobile_msg').removeClass('error_free_tip').addClass('error_tip')
                    }
                })
                .catch(e =>{
                console.log(e)
            })
        },
    }
});

