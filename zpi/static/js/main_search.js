function searchApplications() {
    var val = document.getElementById("input").value;
    var url = document.getElementById("search").href;
    url = url + val;
    document.getElementById("search").href = url;
 }
