  function openPopup() {
    document.getElementById("popup").style.display = "flex";
  }
  
  function closePopup() {
    document.getElementById("popup").style.display = "none";
  }

  function showLogoutPopup() {
    document.getElementById("logout-popup").style.display = "flex";
  }
  
  function confirmLogout(confirm) {
    const popup = document.getElementById("logout-popup");
    popup.style.display = "none";
  
    if (confirm) {
      // You can redirect or perform logout action here
      window.location.href = "http://127.0.0.1:5500/login.html";
      // window.location.href = "/login"; // Optional redirect
    }
  }