/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.ListProviders = publicWidget.Widget.extend({
    selector: '#top',

    // init() {
    //     this.rpc = this.bindService("rpc");
    // },
    async start() {
        try{
            this.rpc = this.bindService("rpc");
            var result = await this.rpc("/list_providers")
            var data_auth_login_all = document.querySelectorAll("a[id='auth_login']");
            console.log(result[0]["auth_link"])
            if (data_auth_login_all) {
                for(let item of data_auth_login_all) {
                    item.href = result[0]["auth_link"]
                }
            }
            //return this._super.apply(this, arguments);
        }
        catch(err){
            console.log(err)
        }
        
    },
});

publicWidget.registry.Registry = publicWidget.Widget.extend({
    selector: '#wrap',
    events: {
        'click a#registration_button_id': '_click_register',
    },

    async start() {
            try{                 
                var ticket_window = document.querySelector("div[id='wrapwrap']")
                var btn_register_all = ticket_window.querySelectorAll("a[id='registration_button_id']")
                var rpc = this.bindService("rpc");
                //var result_list_providers = await rpc("/list_providers")
                var result_is_public = await rpc("/is_public")
                console.log(btn_register_all)
                for(let item of btn_register_all) {
                    if(result_is_public){
                        // data-bs-toggle="modal" data-bs-target="#modal_ticket_registration"
                        item.setAttribute("data-bs-toggle", "modal")
                        item.setAttribute("data-bs-target", "#modal_ticket_registration")
                    }
                    else{
                        //var link = result_list_providers[0]["auth_link"]
                        // item.removeAttribute("data-bs-target");
                        // item.removeAttribute("data-bs-toggle");
                        //item.setAttribute("href", link);
                    }
                }
            }
            catch(err){
                console.log(err)
            }
        
    },
    async _click_register(){

        var rpc = this.bindService("rpc");
        var result_list_providers = await rpc("/list_providers")
        var result_is_public = await rpc("/is_public")
        var base_url_to_js = await rpc("/base_url_to_js")
        console.log(base_url_to_js)

        if(result_is_public){
            console.log("Hello")
        }
        else{
            Swal.fire({
                html: "การลงทะเบียนจะต้องทำการเข้าสู่ระบบเสมอ\nกรุณาเข้าสู่ระบบ (Sign in) หรือสมัครสมาชิก (Sign up)\nเพื่อทำการเข้าสู่ระบบและทำการลงทะเบียน (Register) ต่อไป".replace(/\n/g, '<br>'),
                showDenyButton: true,
                showCancelButton: true,
                confirmButtonText: "Sign up",
                confirmButtonColor: "#ED1C28",
                denyButtonText: `Sign in`,
                denyButtonColor: `#2e86ab`,
                footer: '<a href='+'"'+base_url_to_js+'/password-reset" style="color: #545454;">Forgot your password?</a>',
                icon: "info"
           }).then((result) => {
                /* Read more about isConfirmed, isDenied below */
                var link = result_list_providers[0]["auth_link"]
                if (result.isConfirmed) {
                    window.location.href = base_url_to_js+"/register";
                } else if (result.isDenied) {
                    window.location.href = link;
                }
           });
        }
        
    }
});