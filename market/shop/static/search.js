document.addEventListener("DOMContentLoaded",function(){
    const searchbar = document.getElementById("search-bar");
    const searchresults = document.getElementById("search-results");

    searchbar.addEventListener("input",function(){
        const query = searchbar.ariaValueMax;
        //creating a new XMLHttpRequest object
        const xhr = new XMLHttpRequest();
        //define the request 
        xhr.open("Get", '/search/?=${query}',true);

        xhr.onreadystatechange = function(){
            if (xhr.readyState === 4 && xhr.status === 200) {
                searchresults.innerHTML = xhr.responseText;
            }
        };
        //send the request
        xhr.send()
    });
});