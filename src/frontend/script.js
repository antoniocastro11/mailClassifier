const form = document.getElementById("emailForm");
const loading = document.getElementById("loading");
const resultDiv = document.getElementById("result");
const categorySpan = document.getElementById("category");
const responseText = document.getElementById("responseText");
const errorMsg = document.getElementById("errorMsg");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorMsg.classList.add("hidden");
  resultDiv.classList.add("hidden");

  const emailText = document.getElementById("emailText").value.trim();
  const fileInput = document.getElementById("fileUpload");
  let fileContent = "";

  try {
    if (fileInput.files.length > 0) {
      const file = fileInput.files[0];

      const allowedTypes = ["text/plain", "application/pdf"];
      if (!allowedTypes.includes(file.type)) {
        throw new Error("Formato inválido! Apenas .txt ou .pdf são permitidos.");
      }

      if (file.size > 2 * 1024 * 1024) {
        throw new Error("Arquivo muito grande! Máximo permitido é 2MB.");
      }

      if (file.type === "text/plain") {
        fileContent = await file.text();
      } else if (file.type === "application/pdf") {
        fileContent = null;
      }
    }

    if (!emailText && !fileContent && fileInput.files.length === 0) {
      throw new Error("Por favor, insira o texto do email ou envie um arquivo.");
    }

    loading.classList.remove("hidden");

    const payload = new FormData();
    payload.append("email", emailText);
    if (fileInput.files.length > 0) {
      payload.append("file", fileInput.files[0]);
    }

    const response = await fetch("http://localhost:5000/classify", {
      method: "POST",
      body: payload,
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error || "Erro no servidor");
    }

    const data = await response.json();

    categorySpan.textContent = data.categoria;
    responseText.textContent = data.resposta;
    resultDiv.classList.remove("hidden");

  } catch (error) {
    errorMsg.textContent = error.message;
    errorMsg.classList.remove("hidden");
  } finally {
    loading.classList.add("hidden");
  }
});
