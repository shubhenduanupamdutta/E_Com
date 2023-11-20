// console.log("This is working...");
let cart = {};
if (localStorage.getItem("cart") == null) {
  cart = {};
} else {
  cart = JSON.parse(localStorage.getItem("cart"));
}
document.getElementById("cart").innerHTML = "Cart(" + Object.keys(cart).length + ")";

document.querySelectorAll(".atc").forEach((button) => {
  button.addEventListener("click", (event) => {
    var productId = event.target.id;
    console.log(productId + " clicked");
    if (cart[productId] != undefined) {
      cart[productId] += 1;
    } else {
      cart[productId] = 1;
    }
    console.log(cart);
    localStorage.setItem("cart", JSON.stringify(cart));
    console.log("cart updated");
    document.getElementById("cart").innerHTML = "Cart(" + Object.keys(cart).length + ")";
    // console.log(Object.keys(cart).length);
  });
});
