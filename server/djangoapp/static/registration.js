document.getElementById("cpsw").addEventListener("change", confirmPass);
var cpsw = document.getElementById("cpsw");
var psw = document.getElementById("psw");
var password = document.getElementById("password");
function confirmPass() {
    if(psw.value==cpsw.value){
        password.textContent=''
    }
    else{
        password.textContent='Passwords Do Not Match'
    }
}