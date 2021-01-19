
var initialize = function () {
    const input_text = document.getElementById("id_text");
    input_text.addEventListener("keydown",
        function (e) {
            const haserror = document.getElementById("has-error");
            haserror.style.visibility= "hidden";
    })
};