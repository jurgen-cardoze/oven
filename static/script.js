let basket = [];

function calculateTotal() {
  const pizzaType = document.getElementById("pizza-type").value;
  const pizzaSize = document.getElementById("pizza-size").value;
  const quantity = document.getElementById("quantity").value;
  let price;

  if (pizzaType === "pepperoni") {
    price = 10;
  } else if (pizzaType === "cheese") {
    price = 8;
  } else if (pizzaType === "veggie") {
    price = 12;
  } else if (pizzaType === "hawaiian") {
    price = 12;
  } else if (pizzaType === "meat-lovers") {
    price = 14;
  }

  if (pizzaSize === "normal") {
    // no additional cost
  } else if (pizzaSize === "large") {
    price += 5;
  } else if (pizzaSize === "family-sized") {
    price += 11;
  }

  let total;
  if (!quantity) {
    total = "";
  } else {
    total = `$${price * quantity}`;
  }
  document.getElementById("total").value = total;
}

function addToBasket() {
  const pizzaType = document.getElementById("pizza-type").value;
  const pizzaSize = document.getElementById("pizza-size").value;
  const quantity = document.getElementById("quantity").value;
  const totalAmount = document.getElementById("total").value.slice(1);

  const item = {
    pizzaType,
    pizzaSize,
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
  const basketContainer = document.getElementById("basket");
  let html = "<ul>";
  let totalAmount = 0;
  basket.forEach((item, index) => {
    html += `<li>${item.pizzaType} (${item.pizzaSize}), Quantity: ${item.quantity}, Price: ${item.totalAmount} <button onclick="removeFromBasket(${index})">Remove</button></li>`;
    totalAmount += parseFloat(item.totalAmount);
  });
  html += "</ul>";
  html += `<p>Total: $${totalAmount.toFixed(2)}</p>`;
  basketContainer.innerHTML = html;
}

function placeOrder() {
  const form = new FormData();
  basket.forEach((item) => {
    form.append("pizza_type", item.pizzaType);
    form.append("pizza_size", item.pizzaSize);
    form.append("quantity", item.quantity);
    form.append("total_amount", item.totalAmount);
    
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

document.getElementById("add-to-basket").addEventListener("click", addToBasket);
document.getElementById("submit-order").addEventListener("click", placeOrder);
