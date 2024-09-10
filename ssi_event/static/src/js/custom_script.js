function is_duplicate(array, x, y){
    if( (array[x].value != "" || array[y].value != "") && x!=y && array[x].value == array[y].value){
        return true
    }
}

function add_validate(dom_obj, items){
    dom_obj.classList.add("is-invalid");
    var para = document.createElement("div");
    para.setAttribute("class", "invalid-feedback")
    
    var _str_index = ""
    for(let i=0 ;i<items.length ;i++){
        if(i==items.length-1){
            _str_index = _str_index + "#" +(items[i]+1)
        }
        else{
            _str_index = _str_index + "#" +(items[i]+1) + ", "
        }

    }
    console.log(_str_index)

    para.appendChild(document.createTextNode('This email are already used in in Ticket '+_str_index));
    
    var self = dom_obj.parentNode
    try{
        self.querySelector(".invalid-feedback").replaceChildren(para, self.querySelector(".invalid-feedback"))
    }
    catch(err){
        console.log(err)
        self.appendChild(para)
    }
    var active_window = document.querySelector("div[role='dialog'][id='modal_attendees_registration']");
    var summit_button = active_window.querySelector('button[type="submit"]:not([type=""])')
    summit_button.disabled = true;
    if(summit_button){
        summit_button.disabled = false;
    }
}

function remove_validate_all(array){
    try{
        for(let x = 0; x < array.length; x++){
            array[x].classList.remove("is-invalid");
            for(let itme of array[x].parentNode.querySelectorAll(".invalid-feedback")){
                itme.remove()
            }

        }
    }
    catch(err){
        console.log(err)
    }
}

function duplicate_check(array){
    _array = {}
    for(let x = 0; x < array.length; x++){
        _array[x] = []
    }

    remove_validate_all(array)
    for(let x = 0; x < array.length; x++){
        for(let y = x+1; y < array.length; y++){
            if(is_duplicate(array, x, y)){
                _array[x].push(y)
                _array[y].push(x)
            }
        }
    }
    for(let x = 0; x < array.length; x++){
        for(let _x of _array[x]){
            console.log(_array, x, _array[x], array[_x])
            add_validate(array[_x], _array[_x])
        }
    }
}

function only_one_type(self, type){
    var input_element = self.querySelectorAll("input#form-control-id")
    var array = []
    for(let item of input_element) {
        if(item.type == type){
            array.push(item)
        }
    }

    return array
}

function main(){
    try{
        var active_window = document.querySelector("div[role='dialog'][id='modal_attendees_registration']");
        var summit_button = active_window.querySelector('button[type="submit"]:not([type=""])')

        var _check_email = only_one_type(active_window, "email")
        duplicate_check(_check_email);

        var input_element = active_window.querySelectorAll("input#form-control-id")
        for(let item of input_element){
            item.addEventListener("change", function(){
                if(summit_button){
                    summit_button.disabled = false;
                }
                var _check_email = only_one_type(active_window, "email")
                duplicate_check(_check_email);
            });   
        }

        // var attendee_registration = active_window.querySelector('form[id="attendee_registration"]')
        // attendee_registration.addEventListener("submit", function(){
        //     summit_button.disabled = false;
        //     var _check_email = only_one_type(active_window, "email")
        //     duplicate_check(_check_email);
        // });
    }
    catch(err){
        console.log(err)
    }
}

main()