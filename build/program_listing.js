"use strict";

var _slicedToArray = function (arr, i) {
  if (Array.isArray(arr)) {
    return arr;
  } else {
    var _arr = [];

    for (var _iterator = arr[Symbol.iterator](), _step; !(_step = _iterator.next()).done;) {
      _arr.push(_step.value);

      if (i && _arr.length === i) break;
    }

    return _arr;
  }
};

var querySelector = document.querySelector.bind(document);

var _map = ["#create", "#cancel"].map(querySelector);

var _map2 = _slicedToArray(_map, 2);

var createButton = _map2[0];
var cancelButton = _map2[1];
var _map3 = ["#new_button", "dialog"].map(querySelector);

var _map3 = _slicedToArray(_map3, 2);

var newButton = _map3[0];
var dialog = _map3[1];


var textBox = querySelector("#program_name");

newButton.onclick = function (e) {
  textBox.value = "New Program";
  dialog.showModal();
};

cancelButton.onclick = function (e) {
  dialog.close();
};

createButton.onclick = function (e) {
  var name = textBox.value;

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/create", false);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.onload = function () {
    if (xhr.status === 200) {
      console.log("we're good to go");
      var pid = xhr.responseText;
      window.location.href = "/editor?pid=" + pid;
    } else {
      console.log("something wen't wrong");
    }
  };

  xhr.send(JSON.stringify({ name: name }));
};
