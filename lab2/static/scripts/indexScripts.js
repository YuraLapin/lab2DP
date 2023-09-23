const russianAlphabet = "абвгдежзийклмнопрстуфхцчшщыъьэюя";
const maxPhraseSize = 100;
const maxKeySize = 100;

function checkLine(line, alphabet){
    for (var i = 0; i < line.length; ++i) {
        if (alphabet.search(line.charAt(i)) == -1){
            return false;
        }
    }
    return true;
}

function getNewChar(oldChar, table, tableHeight, tableWidth){
    var oldI = 0;
    var oldJ = 0;
    for (var i = 0; i < tableHeight; ++i){
        for (var j = 0; j < tableWidth; ++j){
            if (table[i][j] == oldChar){
                oldI = i;
                oldJ = j;
                break;
            }
        }
    }
    var newChar = "";
    if (oldI == tableHeight - 1){
        newChar = table[0][oldJ];
    }
    else {
        newChar = table[oldI + 1][oldJ];
    }
    return newChar;
}

function generateTable(key, alphabet){
    var table = [];
    const height = 4;
    const width = 8;
    for (var i = 0; i < height; ++i){
        var currentLine = [];
        for (var j = 0; j < width; ++j){
            currentLine.push("");
        }
        table.push(currentLine);
    }

    var row = key + alphabet;
    var uniqueRow = "";
    for (var i = 0; i < row.length; ++i){
        var curChar = row.charAt(i);
        if (uniqueRow.search(curChar) == -1){
            uniqueRow += curChar;
        }
    }

    for (var i = 0; i < height; ++i){
        for (var j = 0; j < width; ++j){
            table[i][j] = uniqueRow[i * width + j];
        }
    }

    return table
}

function trisemusEncode(table, phrase, alphabet){
    var ans = "";

    for (var i = 0; i < phrase.length; ++i){
        ans += getNewChar(phrase[i], table, table.length, table[0].length);
    }

    return ans
}

function convertToTableText(list){
    var result = "";
    for (var i = 0; i < list.length; ++i){
        var currentRow = "<tr>";
        for (var j = 0; j < list[i].length; ++j){
            currentRow += "<td>" + list[i][j] + "</td>";
        }  
        currentRow += "</tr>";    
        result += currentRow;
    }
    return result;                
}

document.getElementById("confirm").addEventListener(
    "click",
    async function() {
        var phrase = document.getElementById("phrase").value;

        document.getElementById("errorMessage").hidden = true;
        document.getElementById("resultMessage").hidden = true;


        if (phrase.length >= maxPhraseSize){
            document.getElementById("errorMessage").innerHTML = `Фраза не должна быть длиннее ${maxPhraseSize} символов`;
            document.getElementById("errorMessage").hidden = false;
            return;
        }

        if (!checkLine(phrase, russianAlphabet)){
            document.getElementById("errorMessage").innerHTML = "Фраза должна состоять только из строчных букв русского алфавита";
            document.getElementById("errorMessage").hidden = false;
            return;
        }        

        document.getElementById("resultMessage").hidden = false;
        document.getElementById("resultMessage").innerHTML = trisemusEncode(table, phrase, russianAlphabet);

    }    
);

document.getElementById("generate").addEventListener(
    "click",
    async function() {
        await $.ajax({
            method: "POST",
            url: "/generate_keys",            
            success: function(result){
                document.getElementById("p").innerHTML = result[0];
                document.getElementById("q").innerHTML = result[1];
                document.getElementById("m").innerHTML = result[2];
                document.getElementById("n").innerHTML = result[3];
                document.getElementById("e").innerHTML = result[4];
                document.getElementById("d").innerHTML = result[5];
                document.getElementById("y").innerHTML = -1;
            }
        });
    }    
);