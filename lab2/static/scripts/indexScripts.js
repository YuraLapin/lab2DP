function autoGrow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight) + "px";
}


document.getElementById("generate").addEventListener(
    "click",
    async function() {
        await $.ajax({
            method: "POST",
            url: "/generate_keys",            
            success: function(result){
                document.getElementById("p").innerHTML = result[0];
                document.getElementById("q").innerHTML = result[1];
                document.getElementById("phi").innerHTML = result[2];
                document.getElementById("n1").innerHTML = result[3];
                document.getElementById("n2").innerHTML = result[3];
                document.getElementById("e").innerHTML = result[4];
                document.getElementById("d").innerHTML = result[5];
            }
        });
    }    
);


document.getElementById("confirm").addEventListener(
    "click",
    async function() {
        var userPhrase = document.getElementById("phrase").value;

        if (userPhrase == "") {
            document.getElementById("errorMessage").hidden = false;
            document.getElementById("resultMessage").hidden = true;
            document.getElementById("errorMessage").innerHTML = "Введите сообщение"
            return;
        }

        var keyE = document.getElementById("e").innerHTML;
        var keyN = document.getElementById("n1").innerHTML;
        if (keyE == "" || keyN == "") {
            document.getElementById("errorMessage").hidden = false;
            document.getElementById("resultMessage").hidden = true;
            document.getElementById("errorMessage").innerHTML = "Сначала сгенерируйте ключи"
            return;
        }

        await $.ajax({
            method: "POST",
            url: "/cipher",  
            data: {
                phrase: userPhrase,
                e: parseInt(keyE),
                n: parseInt(keyN)
            },
            success: function(result) {
                document.getElementById("errorMessage").hidden = true;
                document.getElementById("resultMessage").hidden = false;
                document.getElementById("resultMessage").innerHTML = result;
            }
        });
    }    
);