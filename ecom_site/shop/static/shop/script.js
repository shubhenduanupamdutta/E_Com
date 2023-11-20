// console.log("This is working...");
let cart = {};
if (localStorage.getItem("cart") == null) {
  cart = {};
} else {
  cart = JSON.parse(localStorage.getItem("cart"));
}
(document.querySelectorAll(".atc")).forEach((button) => {
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
    });
});
