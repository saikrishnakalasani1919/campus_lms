
function validateForm() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
  
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
  
    if (!passwordRegex.test(password)) {
      alert("Password must be at least 8 characters long and include uppercase, lowercase, number, and symbol.");
      return false;
    }
  
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return false;
    }
  
    return true;
  }
  