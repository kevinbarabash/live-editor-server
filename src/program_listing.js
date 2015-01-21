var querySelector = document.querySelector.bind(document);

var [createButton, cancelButton] = ["#create", "#cancel"].map(querySelector);
var [newButton, dialog] = ["#new_button", "dialog"].map(querySelector);

var textBox = querySelector("#program_name");

newButton.onclick = e => {
    textBox.value = "New Program";
    dialog.showModal();
};

cancelButton.onclick = e => {
    dialog.close();
};

createButton.onclick = e => {
    var name = textBox.value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/create", false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onload = function () {
        if (xhr.status === 200) {
            console.log(`we're good to go`);
        } else {
            console.log(`something wen't wrong`);
        }
    };

    xhr.send(JSON.stringify({ name }));
};
