postButton = document.getElementById("post-btn");

function myFunction(x) {
  if (x.matches) {
    // If media query matches
    postButton.classList.add("order-first");
  }
}

var x = window.matchMedia("(max-width: 1000px)");
myFunction(x); // Call listener function at run time
x.addListener(myFunction); // Attach listener function on state changes
