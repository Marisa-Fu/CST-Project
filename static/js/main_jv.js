  functi// Function to open the popup
  function openPopup() {
      const popup = document.getElementById('popup');
      popup.style.display = 'flex';
  
      // Fetch current balance (cash and lives) when popup is opened
      fetch('/get_balance', {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json'
          },
          credentials: 'include'
      })
      .then(response => response.json())
      .then(data => {
        console.log("Balance response:", data);

          // If user is logged in and data returned successfully
          if (data.cash !== undefined && data.lives !== undefined) {
              document.getElementById('cash-display').textContent = `Cash: $${data.cash}`;
              document.getElementById('lives-display').textContent = `Lives: ${data.lives}`;
          } else {
              alert("Error fetching balance. Please log in again.");
          }
      })
      .catch(error => {
          console.error("Error fetching balance:", error);
      });
  }
  
  // Function to close the popup
  function closePopup() {
      const popup = document.getElementById('popup');
      popup.style.display = 'none';
  }
  
  // Function to show the logout confirmation popup
  function showLogoutPopup() {
      document.getElementById("logout-popup").style.display = "flex";
  }
  
  // Function to confirm logout
  function confirmLogout(confirm) {
      const popup = document.getElementById("logout-popup");
      popup.style.display = "none";
  
      if (confirm) {
          // You can redirect or perform logout action here
          window.location.href = "/logout";
          // window.location.href = "/login"; // Optional redirect
      }
  }
  
  // Function to purchase a life
  function purchaseLife() {
      fetch('/purchase_life', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          credentials: 'include'
      })
      .then(response => response.json())
      .then(data => {
        console.log("Purchase response:", data);
          if (data.message) {
              // Update the display after a successful purchase
              openPopup(); // Re-fetch the balance to update the UI
          } else {
              alert(data.error || "Error purchasing life");
          }
      })
      .catch(error => {
          console.error("Error purchasing life:", error);
      });
  }
  