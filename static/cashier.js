let basket = [];

function calculateTotal() {
  const itemType = document.getElementById("item-type").value;
  const itemSize = document.getElementById("item-size").value;
  const quantity = document.getElementById("quantity").value;
  let price;

  if (itemType === "pepperoni") {
    price = 10;
  } else if (itemType === "cheese") {
    price = 8;
  } else if (itemType === "veggie") {
    price = 12;
  } else if (itemType === "hawaiian") {
    price = 12;
  } else if (itemType === "meat-lovers") {
    price = 14;
  } else if (itemType === "cola") {
    price = 2.5;
  } else if (itemType === "fanta") {
    price = 2.5;
  } else if (itemType === "sprite") {
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

  let total;
  if (!quantity) {
    total = "";
  } else {
    total = `$${(price * quantity).toFixed(2)}`;
  }
  document.getElementById("total").value = total;
}

function addToBasket() {
  const itemType = document.getElementById("item-type").value;
  const itemSize = document.getElementById("item-size").value;
  const quantity = document.getElementById("quantity").value;
  const totalAmount = document.getElementById("total").value.slice(1);

  const item = {
    itemType,
    itemSize,
    quantity,
    totalAmount,
  };
  basket.push(item);
  renderBasket();
}

function removeFromBasket(index) {
  basket.splice(index, 1);
  renderBasket();
}

function renderBasket() {
  const basketTable = document.getElementById("basket").getElementsByTagName('tbody')[0];
  basketTable.innerHTML = "";
  let totalPrice = 0;

  for (let i = 0; i < basket.length; i++) {
    const item = basket[i];
    const row = basketTable.insertRow(i);
    const itemTypeCell = row.insertCell(0);
    const itemSizeCell = row.insertCell(1);
    const quantityCell = row.insertCell(2);
    const priceCell = row.insertCell(3);
    const actionsCell = row.insertCell(4);

    itemTypeCell.innerHTML = item.itemType;
    itemSizeCell.innerHTML = item.itemSize;
    quantityCell.innerHTML = item.quantity;
    priceCell.innerHTML = item.totalAmount;
    totalPrice += parseFloat(item.totalAmount);

    const removeButton = document.createElement("button");
    removeButton.innerText = "Remove";
    removeButton.addEventListener("click", () => removeFromBasket(i));
    actionsCell.appendChild(removeButton);
  }

  document.getElementById("total-price").innerText = `$${totalPrice.toFixed(2)}`;
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