const form = document.getElementById("emailForm");
const loading = document.getElementById("loading");
const resultDiv = document.getElementById("result");
const categorySpan = document.getElementById("category");
const responseText = document.getElementById("responseText");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const emailText = document.getElementById("emailText").value;
  if (!emailText) {
    alert("Por favor, insira o texto do email ou envie um arquivo.");
    return;
  }

  loading.classList.remove("hidden");
  resultDiv.classList.add("hidden");

  try {
    const response = await fetch("http://localhost:5000/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: emailText }),
    });

    const data = await response.json();
    categorySpan.textContent = data.categoria;
    responseText.textContent = data.resposta;

    resultDiv.classList.remove("hidden");
  } catch (error) {
    alert("Erro ao processar email: " + error);
  } finally {
    loading.classList.add("hidden");
  }
});
