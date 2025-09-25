 const form = document.getElementById("emailForm");

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const emailText = document.getElementById("emailText").value;
      if (!emailText) {
        alert("Por favor, insira o texto do email ou envie um arquivo.");
        return;
      }
    });