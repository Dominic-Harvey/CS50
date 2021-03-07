function moveInputTitle(o) {
    o.className += " active";
  }
  
document.getElementById("name").onclick = function () {
moveInputTitle(document.getElementById("nameBox"));
};
document.getElementById("subject").onclick = function () {
moveInputTitle(document.getElementById("subjectBox"));
};
document.getElementById("message").onclick = function () {
moveInputTitle(document.getElementById("messageBox"));
};
document.getElementById("email").onclick = function () {
moveInputTitle(document.getElementById("emailBox"));
};

function showAlert() {
document.getElementById("messageSentAlert").className += "show";
};
