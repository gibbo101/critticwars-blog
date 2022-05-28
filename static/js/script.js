setTimeout(function() {
    let messages = document.getElementById("msg");
    let alert = new bootstrap.Alert(messages);
    alert.close();
}, 2000);

function deleteAccount() {
    alert("This action can't be undone! Do you really want to delete your account?");
}

function deleteComment() {
    alert("This action can't be undone! Do you really want to delete this comment?");
}