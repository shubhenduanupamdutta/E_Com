// console.log("This is working...");
let cart = {};
let item_name = {};
if (localStorage.getItem("cart") == null) {
  cart = {};
} else {
  cart = JSON.parse(localStorage.getItem("cart"));
}

document.getElementById("cart").innerHTML = "Cart(" + Object.keys(cart).length + ")";

DisplayCart(cart);

document.querySelectorAll(".atc").forEach((button) => {
  button.addEventListener("click", (event) => {
    let productId = event.target.id;
    let productName = document.getElementById("nm" + productId).innerHTML;
    let productPriceStr = document.getElementById("price" + productId).innerHTML;
    let productPrice = parseFloat(productPriceStr.split(" ")[1])
    console.log(productId + " clicked");
    console.log(productName, productPrice);
    if (cart[productId] != undefined) {
      cart[productId][0] += 1;
      cart[productId][2] += productPrice;
    } else {
      cart[productId] = [1, productName, productPrice];
    }
    console.log(cart);
    localStorage.setItem("cart", JSON.stringify(cart));
    console.log("cart updated");
    // console.log(productPrice, typeof productPrice);
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
    cartString += cart[x][1] + " Qty: " + cart[x][0] + "<br>";
    cartIndex++;
  }
  cartString += "<br><a href='/checkout' class='btn btn-success'>Checkout</a><br>";
  document.getElementById("cart").setAttribute("data-bs-content", cartString);
}

const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
const popoverList = [...popoverTriggerList].map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl);
});

function create_checkout_list_item(productName, quantity, price) {
  let item_str = `<span> <span class=""> ${quantity} </span> ${productName} </span>
  <span class="badge bg-primary">&#8377; ${price}</span>`;
  let list_item = document.createElement("li");
  list_item.classList.add(
    "list-group-item",
    "d-flex",
    "justify-content-between",
    "align-items-center"
  );

  list_item.innerHTML = item_str;
  document.getElementById("checkoutList").appendChild(list_item);
}

let total = 0;
for (item in cart) {
  let productName = cart[item][1];
  let quantity = cart[item][0];
  let price = cart[item][2];
  total += price;
  if (!(document.getElementById("checkoutList") == null)) {
    create_checkout_list_item("of " + productName, quantity, price);
  }
}
if (Object.keys(cart).length > 0) {
  create_checkout_list_item("Your Total Cart Value", "", total);
}


if (!(document.getElementById("items") == null)) {
  document.getElementById("items").value = JSON.stringify(cart);
}
