function addToCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    cart[productId] = (cart[productId] || 0) + 1;
    localStorage.setItem('cart', JSON.stringify(cart));
    alert("Added to cart!");
}

function checkout() {
    const cart = JSON.parse(localStorage.getItem('cart'));
    if (!cart || Object.keys(cart).length === 0) {
        alert("Your cart is empty.");
        return;
    }
    // Process cart data (could be sent to backend for processing)
    localStorage.removeItem('cart');
    alert("Checkout complete!");
}
