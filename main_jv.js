function goToLevel(level) {
    alert(`Navigating to Level ${level}...`);
  }

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
      alert("You have been logged out.");
      // window.location.href = "/login"; // Optional redirect
    }
  }