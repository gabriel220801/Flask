
const menuOpciones = document.querySelector(".menu-opciones");
const btnSignUp = document.getElementById("btn-sign-up");
const header = document.querySelector("header");
const controlesUsuario = document.querySelector(".controles-usuario");
const contenedor = document.querySelector(".contenedor");
const btnMenu = document.getElementById("btn-menu");

const responsiveY = ()=>{
    if(window.innerHeight<=362){
        if(menuOpciones.classList.contains("mostrar"))
            menuOpciones.classList.add("min");
        else
            menuOpciones.classList.remove("min");
    }
    else{
        menuOpciones.classList.remove("min");
    }
};
const responsive = ()=>{
    if(window.innerWidth<=865){
        menuOpciones.children[0].appendChild(btnSignUp);
        header.appendChild(menuOpciones);
    }else{
        controlesUsuario.appendChild(btnSignUp);
        contenedor.appendChild(menuOpciones);
    }

    responsiveY();
}

btnMenu.addEventListener("click",()=>{
    menuOpciones.classList.toggle("mostrar");
    responsiveY();
});
responsive();

window.addEventListener("resize",responsive);