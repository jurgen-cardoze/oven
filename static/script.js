let basket = [];

function calculateTotal(id) {
  const itemType = document.getElementById("item-type" + id).value;
  const itemSize = document.getElementById("item-size" + id).value;
  const quantity = document.getElementById("quantity" + id).value;
  let price;
  
  if (itemType === "pepperoni") {
    price = 10;
  } else if (itemType === "cheese") {
    price = 8; 
  } else if (itemType === "veggie" || itemType === "hawaiian") {
    price = 12;
  } else if (itemType === "meat-lovers") {
    price = 14;
  } else if (itemType === "cola" || itemType === "fanta" || itemType === "sprite") {
    price = 2.5;
  }

  if (itemSize === "normal") {
    // no additional cost
  } else if (itemSize === "large") {
    if (["cola", "fanta", "sprite"].includes(itemType)) {
      price += 1;
    } else {
      price += 5;
    }
  } else if (itemSize === "extra-large") {
    if (["cola", "fanta", "sprite"].includes(itemType)) {
      price += 2.5;
    } else {
      price += 11;
    }
  }

  let total = price * quantity;
  document.getElementById("total" + id).value = "$" + total.toFixed(2);
}
function updateImage(id) {
  const select = document.getElementById(`item-type${id}`);
  const card = document.querySelector(`#item-type${id}`).closest('.card');
  const img = card.querySelector('img');

  select.addEventListener('change', function() {
    const value = this.value;
    const imagename = value + '.png';
    const url = "/static/" + imagename;
    img.src = url;
  });
}

function addToBasket(id) {
  const itemType = document.getElementById("item-type" + id).value;
  const itemSize = document.getElementById("item-size" + id).value;
  const quantity = document.getElementById("quantity" + id).value;
  const price = document.getElementById("total" + id).value;

  const item = {
    itemType,
    itemSize,
    quantity,
    price,
    totalAmount: parseFloat(price.substring(1)) // set totalAmount to the calculated value
  };
  basket.push(item);

  const basketTable = document.getElementById("basket").getElementsByTagName('tbody')[0];
  const newRow = basketTable.insertRow();

  const typeCell = newRow.insertCell(0);
  const sizeCell = newRow.insertCell(1);
  const quantityCell = newRow.insertCell(2);
  const priceCell = newRow.insertCell(3);
  const actionsCell = newRow.insertCell(4);

  typeCell.innerHTML = item.itemType;
  sizeCell.innerHTML = item.itemSize;
  quantityCell.innerHTML = item.quantity;
  priceCell.innerHTML = item.price;

  const removeBtn = document.createElement("button");
  removeBtn.innerHTML = "Remove";
  removeBtn.addEventListener('click', () => {
    const index = basket.indexOf(item);
    basket.splice(index, 1);
    newRow.remove();
    updateTotalPrice();
  });
  actionsCell.appendChild(removeBtn);

  updateTotalPrice();
}

function updateTotalPrice() {
  let totalPrice = 0;
  for (let i = 0; i < basket.length; i++) {
    const item = basket[i];
    totalPrice += parseFloat(item.price.substring(1));
  }
  document.getElementById("total-price").innerHTML = "$" + totalPrice.toFixed(2);
}

function placeOrder() {
  const form = new FormData();
  basket.forEach((item) => {
  form.append("itemType", item.itemType);
  form.append("itemSize", item.itemSize);
  form.append("quantity", item.quantity);
  form.append("totalAmount", item.totalAmount);
  
  });
  
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/submit-order", true);
  xhr.onload = function () {
  if (this.status === 200) {
  alert("Order placed successfully!");
  basket = [];
  renderBasket();
  } else {
  alert("There was an error while placing your order.");
  }
  };
  xhr.send(form);
  }
  
  // Add event listener to the 'Place Order' button
document.getElementById("submit-order").addEventListener("click", placeOrder);

document.getElementById("add-to-basket").addEventListener("click", addToBasket);
document.getElementById("submit-order").addEventListener("click", placeOrder);