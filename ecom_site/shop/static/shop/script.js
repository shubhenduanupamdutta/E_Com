// console.log("This is working...");
let cart = {};
let item_name = {};
if (localStorage.getItem("cart") == null) {
  cart = {};
  item_name = {};
} else {
  cart = JSON.parse(localStorage.getItem("cart"));
  item_name = JSON.parse(localStorage.getItem("item_name"));
}

document.getElementById("cart").innerHTML = "Cart(" + Object.keys(cart).length + ")";

DisplayCart(cart);

document.querySelectorAll(".atc").forEach((button) => {
  button.addEventListener("click", (event) => {
    let productId = event.target.id;
    let productName = document.getElementById("nm" + productId).innerHTML;
    console.log(productId + " clicked");
    if (cart[productId] != undefined) {
      cart[productId] += 1;
      item_name[productId] = productName;
    } else {
      cart[productId] = 1;
      if (!item_name.hasOwnProperty(productId)) item_name[productId] = productName;
    }
    console.log(cart);
    localStorage.setItem("cart", JSON.stringify(cart));
    localStorage.setItem("item_name", JSON.stringify(item_name));
    console.log("cart updated");
    document.getElementById("cart").innerHTML = "Cart(" + Object.keys(cart).length + ")";
    DisplayCart(cart);
    // console.log(Object.keys(cart).length);
  });
});

function DisplayCart(cart) {
  let cartString = "";
  cartString += "<h5>This is your cart</h5>";
  var cartIndex = 1;
  for (let x in cart) {
    cartString += cartIndex + ". ";
    cartString += item_name[x] + " Qty: " + cart[x] + "<br>";
    cartIndex++;
  }
  cartString += "<br><a href='/checkout' class='btn btn-success'>Checkout</a><br>";
  document.getElementById("cart").setAttribute("data-bs-content", cartString);
}

const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
const popoverList = [...popoverTriggerList].map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl);
});

for (item in cart) {
  let productName = item_name[item];
  let quantity = cart[item];
  let list = document.getElementById("checkoutList");
  if (!(list == null)) {
    let item_str = `${productName}
  <span class="badge bg-primary rounded-pill">${quantity}</span>`;
    let list_item = document.createElement("li");
    list_item.classList.add(
      "list-group-item",
      "d-flex",
      "justify-content-between",
      "align-items-center"
    );

    list_item.innerHTML = item_str;
    list.appendChild(list_item);
  }
}
